from django.contrib import admin
from .models import Profile, Subject, Assignment, Quest, Badge, ProfileAchievement

# Register your models here.
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Quest)
admin.site.register(Badge)
admin.site.register(ProfileAchievement)
