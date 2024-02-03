import os
import uuid
# import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Subject, Assignment, Avatar, Quest, Badge, ProfileAchievement

#Create your views here.

#Basic Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#User Views
def user_detail(request):
    pass

def user_update(request):
    pass

def user_delete(request):
    pass

#Quest Views
def unfinished_quest(request, user_id, quest_id):
   pass

def finished_quest(request, user_id, quest_id):
   pass

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
    pass

def subjects_detail(request):
    pass

def subjects_create(request):
    pass

def subjects_update(request):
    pass

def subjects_delete(request):
    pass

#About Leaderboards
def leaderboard(request):
    pass

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
