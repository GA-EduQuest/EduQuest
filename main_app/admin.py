from django.contrib import admin
from .models import Profile, Subject, Assignment, Quest, Badge, ProfileAchievement
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Adding in code to extend the Django default user model to include the fields in the 'Profile' model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Your usual admin models
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Quest)
admin.site.register(Badge)
admin.site.register(ProfileAchievement)
