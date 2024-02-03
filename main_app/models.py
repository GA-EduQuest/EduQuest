from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    school_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    xp = models.IntegerField(
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    name = models.CharField(max_length=100)
    field = models.CharField(
        max_length=2,
        choices=FIELD,
        default=FIELD[4][0]
    )
    start_date = models.DateField
    end_date = models.DateField
    progress = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    exam_date = models.DateField
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

# The avatar photo for each profile/user
class Avatar(models.Model):
    url = models.URLField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.profile_id} @{self.url}"

class Quest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    xp_earned = models.IntegerField(
        validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200)
    quest = models.OneToOneField(Quest, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProfileAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    date_achieved = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.quest.name} - {self.date_achieved}"
