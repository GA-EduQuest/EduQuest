import os
import uuid
# import boto3
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Subject, Assignment, Avatar, Quest, ProfileAchievement, User
from .forms import SubjectForm
from datetime import date

#Create your views here.

#Basic Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#User Views
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile
    achievements = ProfileAchievement.objects.filter(user=user)
    return render(request, 'user/user_detail.html', {
       'user': user, 'profile': profile, 'achievements': achievements
    })

# def user_update(request):
#     pass

# def user_delete(request):
#     pass

# Profile Views
class ProfileUpdate(LoginRequiredMixin, UpdateView):
   model = Profile
   fields = ['email', 'first_name', 'last_name', 'school_year']



#Quest Views
def quests_index(request):
    user = request.user
    all_quests = Quest.objects.all()
    # Filter ProfileAchievement objects for the current user
    achieved_quests = ProfileAchievement.objects.filter(user=user)
    achieved_quest_ids = list(achieved_quests.values_list('quest__id', flat=True))
    uncompleted_quests = all_quests.exclude(id__in=achieved_quests.values_list('quest', flat=True))
    return render(request, 'quests/quests_index.html', {'all_quests': all_quests, 'achieved_quest_ids': achieved_quest_ids, 'uncompleted_quests': uncompleted_quests })

def quests_detail(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    user = request.user
    # Check if the user has achieved the quest - returns a true or false
    achieved_quest = ProfileAchievement.objects.filter(user=user, quest=quest).exists()
    return render(request, 'quests/quests_detail.html', {'quest': quest, 'achieved_quest': achieved_quest })

#Badges Views
def badges_list(request):
    pass

def badges_detail(request):
    pass
# ---Admin Only Views--- #
def badges_create(request):
    pass

def badges_update(request):
    pass

def badges_delete(request):
    pass

def not_owned_badges(request, user_id, quest_id, badge_id):
   pass

def owned_badges(request, user_id, quest_id, badge_id):
   pass


#Subjects Views
def subjects_index(request):
    subjects = Subject.objects.filter(user=request.user)
    upcoming_exam = subjects.filter(exam_date__gte=date.today()).order_by('exam_date').first()
    all_quests = Quest.objects.all()
    return render(request, 'subjects/index.html', {'subjects': subjects, 'upcoming_exam': upcoming_exam, 'all_quests': all_quests})

def subjects_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'subjects/subject_detail.html', {'subject': subject })

def subjects_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            # Check if the user has created any subjects before
            existing_subjects_count = Subject.objects.filter(user=request.user).exclude(pk=subject.pk).count()
            # Check if 'Getting Started' quest is not already in achievements
            getting_started_quest = Quest.objects.get(name='Getting Started')
            if existing_subjects_count == 0 and not ProfileAchievement.objects.filter(user=request.user, quest=getting_started_quest).exists():
                # Add 'Getting Started' quest and update XP
                ProfileAchievement.objects.create(user=request.user, quest=getting_started_quest)
                request.user.profile.xp += getting_started_quest.xp_earned
                request.user.profile.save()
            return redirect('subjects_detail', pk=subject.pk)
    else:
        form = SubjectForm()

    return render(request, 'subjects/subject_form.html', {'form': form, 'subject': None})

def subjects_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subjects_detail', pk=pk)
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'subjects/subject_form.html', {'form': form, 'subject': subject})

def subjects_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':

        subject.delete()
        return redirect('index')

    return render(request, 'subjects/subject_delete.html', {'subject': subject})

#About Leaderboards
def leaderboard(request):
    leaderboard_data = Profile.objects.all().order_by('-xp')
    context = {
        'leaderboard_data': leaderboard_data,
    }
    return render(request, 'main_app/leaderboard.html', context)

#Assignments Views
class AssignmentList(DetailView):
  model = Assignment

class AssignmentCreate(CreateView):
  model = Assignment
  fields = '__all__'

class AssignmentUpdate(UpdateView):
  model = Assignment
  fields = '__all__'

class AssignmentsDelete(DeleteView):
  model = Assignment
  success_url = '/assignment'

#Signup Views
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
