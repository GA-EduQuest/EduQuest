from django.contrib import admin
from .models import Profile, Subject, Assignment, Quest, ProfileAchievement
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Quest)
admin.site.register(ProfileAchievement)
