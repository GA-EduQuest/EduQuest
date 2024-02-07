from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from datetime import date, timedelta

FIELD = (
    ('MA', 'Maths'),
    ('SS', 'Social Science'),
    ('SC', 'Science'),
    ('AR', 'Arts'),
    ('HU', 'Humanities')
)

GRADE = (
    ('A', 'A - Excellent'),
    ('B', 'B - Good'),
    ('C', 'C - Satisfactory'),
    ('D', 'D - Limited'),
    ('E', 'E - Very Low'),
    ('F', 'F - Failed/Incomplete')
)

STATUS = (
    ('NS', 'Not Started'),
    ('IP', 'In Progress'),
    ('CM', 'Completed')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    school_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        null=True, blank=True
    )
    xp = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    avatar_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'user_id': self.user.id})

# Automatically add a profile for the user when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def one_day_after():
    date.today() + timedelta(days=1)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    field = models.CharField(
        max_length=2,
        choices=FIELD,
        default=FIELD[4][0]
    )
    start_date = models.DateField(("Date"), default=date.today)
    end_date = models.DateField(("Date"), default=date.today)
    progress = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=1
    )
    exam_date = models.DateField(("Date"), default=date.today() + timedelta(days=1))
    grade = models.CharField(
        max_length=1,
        choices=GRADE,
        default=GRADE[2][0]
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # need to confirm the view to send people to
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # Calculate progress based on the proximity of today's date to start and end dates
        today = date.today()
        # Handling case where start and end dates are the same
        if self.start_date == self.end_date:
            self.progress = 100
        else:
            days_total = (self.end_date - self.start_date).days
            days_passed = (today - self.start_date).days
            progress = min(100, max(0, int((days_passed / days_total) * 100)))

            self.progress = progress

        super().save(*args, **kwargs)

class Assignment(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date = models.DateField
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=STATUS[0][0]
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Quest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    xp_earned = models.IntegerField(
        validators=[MinValueValidator(1)])
    badge_image_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name

    @staticmethod
    def is_grandmaster(user):
        # Check if the user has achieved all quests except 'Grandmaster of EduQuest' (to be eligible for the Grandmaster quest)
        all_quests_except_grandmaster = Quest.objects.exclude(name='Grandmaster of EduQuest')
        return all(ProfileAchievement.has_quest_achievement(user, quest.name) for quest in all_quests_except_grandmaster)

    @staticmethod
    def is_multitasking_maven(user):
        # Check if the user has finished two subjects with grades A or B
        completed_subjects = Subject.objects.filter(user=user, progress=100, grade__in=['A', 'B']).count()
        return completed_subjects >= 2

class ProfileAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    date_achieved = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.quest.name} - {self.date_achieved}"

    @staticmethod
    def has_quest_achievement(user, quest_name):
        # Check if the user has achieved a specific quest
        return ProfileAchievement.objects.filter(user=user, quest__name=quest_name).exists()

    @staticmethod
    def get_quest_xp(quest_name):
        # Get the XP earned for a specific quest
        return Quest.objects.get(name=quest_name).xp_earned


# On login - check if user has achieved any quests
@receiver(user_logged_in, sender=User)
def check_achievements_on_login(sender, request, user, **kwargs):
    if Quest.objects.exists():  # Check if there are any quests in the database
        # Check Exam Slayer achievement
        exam_slayer_quest_name = 'Exam Slayer'
        if not ProfileAchievement.has_quest_achievement(user, exam_slayer_quest_name):
            subjects_with_passed_exams = Subject.objects.filter(user=user, exam_date__lt=date.today())
            if subjects_with_passed_exams.exists():
                exam_slayer_quest = Quest.objects.get(name=exam_slayer_quest_name)
                ProfileAchievement.objects.create(user=user, quest=exam_slayer_quest)
                user.profile.xp += ProfileAchievement.get_quest_xp(exam_slayer_quest_name)
                user.profile.save()

        # Check Elite Leaderboard Champion achievement
        leaderboard_data = Profile.objects.all().order_by('-xp')
        is_elite_champion = leaderboard_data.first() == user.profile
        elite_champion_quest_name = 'Elite Leaderboard Champion'
        if is_elite_champion and not ProfileAchievement.has_quest_achievement(user, elite_champion_quest_name):
            elite_champion_quest = Quest.objects.get(name=elite_champion_quest_name)
            ProfileAchievement.objects.create(user=user, quest=elite_champion_quest)
            user.profile.xp += ProfileAchievement.get_quest_xp(elite_champion_quest_name)
            user.profile.save()

        # Check Grandmaster of EduQuest achievement
        grandmaster_quest_name = 'Grandmaster of EduQuest'
        if Quest.is_grandmaster(user) and not ProfileAchievement.has_quest_achievement(user, grandmaster_quest_name):
            grandmaster_quest = Quest.objects.get(name=grandmaster_quest_name)
            ProfileAchievement.objects.create(user=user, quest=grandmaster_quest)
            user.profile.xp += ProfileAchievement.get_quest_xp(grandmaster_quest_name)
            user.profile.save()

        # Check Multitasking Maven achievement
        multitasking_maven_quest_name = 'Multitasking Maven'
        if Quest.is_multitasking_maven(user) and not ProfileAchievement.has_quest_achievement(user, multitasking_maven_quest_name):
            multitasking_maven_quest = Quest.objects.get(name=multitasking_maven_quest_name)
            ProfileAchievement.objects.create(user=user, quest=multitasking_maven_quest)
            user.profile.xp += ProfileAchievement.get_quest_xp(multitasking_maven_quest_name)
            user.profile.save()
