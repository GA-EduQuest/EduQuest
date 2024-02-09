from .models import Profile, Subject, Assignment, Quest, ProfileAchievement, User
from datetime import date, datetime
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models import F

# Functions that check & grant quests based on user actions. Note, some logic also sits on the models where relevant.

def grant_name_to_face_quest(user):
        name_to_face_quest_name = 'A Name to a Face'
        if Quest.objects.exists():
            if not ProfileAchievement.has_quest_achievement(user, name_to_face_quest_name):
                name_to_face_quest = Quest.objects.get(name=name_to_face_quest_name)
                ProfileAchievement.objects.create(user=user, quest=name_to_face_quest)
                user.profile.xp += ProfileAchievement.get_quest_xp(name_to_face_quest_name)
                user.profile.save()

def grant_getting_started_quest(user, subject):
    getting_started_quest_name = 'Getting Started'
    if not ProfileAchievement.has_quest_achievement(user, getting_started_quest_name):
        existing_subjects_count = Subject.objects.filter(user=user).exclude(pk=subject.pk).count()
        if existing_subjects_count == 0:
            getting_started_quest = Quest.objects.get(name=getting_started_quest_name)
            ProfileAchievement.objects.create(user=user, quest=getting_started_quest)
            user.profile.xp += ProfileAchievement.get_quest_xp(getting_started_quest_name)
            user.profile.save()

def grant_subject_explorer_quest(user):
    subject_explorer_quest_name = 'Subject Explorer'
    subjects_count_by_field = Subject.objects.filter(user=user).values('field').distinct().count()
    if subjects_count_by_field >= 4 and not ProfileAchievement.has_quest_achievement(user, subject_explorer_quest_name):
        subject_explorer_quest = Quest.objects.get(name=subject_explorer_quest_name)
        ProfileAchievement.objects.create(user=user, quest=subject_explorer_quest)
        user.profile.xp += ProfileAchievement.get_quest_xp(subject_explorer_quest_name)
        user.profile.save()

def grant_exam_slayer_quest(user):
    exam_slayer_quest_name = 'Exam Slayer'
    if not ProfileAchievement.has_quest_achievement(user, exam_slayer_quest_name):
        subjects_with_passed_exams = Subject.objects.filter(user=user, exam_date__lt=date.today())
        if subjects_with_passed_exams.exists():
            exam_slayer_quest = Quest.objects.get(name=exam_slayer_quest_name)
            ProfileAchievement.objects.create(user=user, quest=exam_slayer_quest)
            user.profile.xp += ProfileAchievement.get_quest_xp(exam_slayer_quest_name)
            user.profile.save()

def grant_multitasking_maven_quest(user):
    multitasking_maven_quest_name = 'Multitasking Maven'
    completed_subjects = Subject.objects.filter(user=user, progress=100, grade__in=['A', 'B']).count()
    if completed_subjects >= 2 and not ProfileAchievement.has_quest_achievement(user, multitasking_maven_quest_name):
        multitasking_maven_quest = Quest.objects.get(name=multitasking_maven_quest_name)
        ProfileAchievement.objects.create(user=user, quest=multitasking_maven_quest)
        user.profile.xp += ProfileAchievement.get_quest_xp(multitasking_maven_quest_name)
        user.profile.save()

def grant_elite_leaderboard_quest():
    leaderboard_data = Profile.objects.all().order_by('-xp')
    if Quest.objects.exists():
        elite_champion_quest_name = 'Elite Leaderboard Champion'
        top_profile = leaderboard_data.first()
        if top_profile:
            elite_champion_quest = Quest.objects.get(name=elite_champion_quest_name)
            if not ProfileAchievement.has_quest_achievement(top_profile.user, elite_champion_quest_name):
                ProfileAchievement.objects.create(user=top_profile.user, quest=elite_champion_quest)
                top_profile.user.profile.xp += ProfileAchievement.get_quest_xp(elite_champion_quest_name)
                top_profile.user.profile.save()

def grant_master_the_basics_quest(user):
    master_the_basics_quest_name = 'Master the Basics'
    if not ProfileAchievement.has_quest_achievement(user, master_the_basics_quest_name):
        subject_count = Subject.objects.filter(user=user).count()
        if subject_count >= 4:
            subjects_with_assignments = Subject.objects.filter(user=user, assignment__isnull=False).distinct()
            if subjects_with_assignments.count() >= 4:
                master_the_basics_quest = Quest.objects.get(name=master_the_basics_quest_name)
                ProfileAchievement.objects.create(user=user, quest=master_the_basics_quest)
                user.profile.xp += ProfileAchievement.get_quest_xp(master_the_basics_quest_name)
                user.profile.save()

def grant_time_management_pro_quest(user):
    time_management_pro_quest_name = 'Time Management Pro'
    if not ProfileAchievement.has_quest_achievement(user, time_management_pro_quest_name):
        # Count the number of completed assignments before or on their due date for the current user
        completed_assignments = Assignment.objects.filter(
            status='CM',
            complete_date__lte=F('due_date'),
            subject__user=user
        ).count()
        print(completed_assignments)
        if completed_assignments >= 2:
            time_management_pro_quest = Quest.objects.get(name=time_management_pro_quest_name)
            ProfileAchievement.objects.create(user=user, quest=time_management_pro_quest)
            user.profile.xp += ProfileAchievement.get_quest_xp(time_management_pro_quest_name)
            user.profile.save()

def grant_assignment_conqueror_quest(user):
    quest_name = 'Assignment Conqueror'
    if not ProfileAchievement.has_quest_achievement(user, quest_name):
        quest = Quest.objects.get(name=quest_name)
        ProfileAchievement.objects.create(user=user, quest=quest)
        user.profile.xp += ProfileAchievement.get_quest_xp(quest_name)
        user.profile.save()

def grant_grandmaster_quest(user):
    grandmaster_quest_name = 'Grandmaster of EduQuest'
    if Quest.is_grandmaster(user) and not ProfileAchievement.has_quest_achievement(user, grandmaster_quest_name):
        grandmaster_quest = Quest.objects.get(name=grandmaster_quest_name)
        ProfileAchievement.objects.create(user=user, quest=grandmaster_quest)
        user.profile.xp += ProfileAchievement.get_quest_xp(grandmaster_quest_name)
        user.profile.save()



# Checking Some Quests on Login (ones where something could happen in your absence, e.g. time passing, leaderboard changes etc.) #
@receiver(user_logged_in, sender=User)
def check_achievements_on_login(sender, request, user, **kwargs):
    if Quest.objects.exists():
        # Checks for some Quest achievements on login: Exam Slayer, Elite Leaderboard Champion, Grandmaster & Multitasking Maven
        grant_exam_slayer_quest(user)
        grant_grandmaster_quest(user)
        grant_multitasking_maven_quest(user)
        grant_elite_leaderboard_quest()
