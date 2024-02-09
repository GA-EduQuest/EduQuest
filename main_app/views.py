import os
import uuid
import json
# import boto3
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Subject, Assignment, Quest, ProfileAchievement, User
from .forms import SubjectForm
from datetime import date, datetime
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import F
from .quests import grant_name_to_face_quest, grant_grandmaster_quest, grant_exam_slayer_quest, grant_getting_started_quest, grant_subject_explorer_quest, grant_multitasking_maven_quest, grant_elite_leaderboard_quest, grant_master_the_basics_quest, grant_time_management_pro_quest, grant_assignment_conqueror_quest


# Basic Views #
def home(request):
    return render(request, 'home.html')

# def about(request):
#     return render(request, 'about.html')

#User Views #

@login_required
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile
    achievements = ProfileAchievement.objects.filter(user=user)
    return render(request, 'user/user_detail.html', {
       'user': user, 'profile': profile, 'achievements': achievements
    })

# Profile Views #

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['email', 'first_name', 'last_name', 'school_year']

    def form_valid(self, form):
        # Check if the first name and last name have been changed
        if set(form.changed_data).intersection({'first_name', 'last_name'}):
            grant_name_to_face_quest(form.instance.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_detail', kwargs={'user_id': self.object.user.id})



# Quest Views #

@login_required
def quests_index(request):
    user = request.user
    all_quests = Quest.objects.all()

    if Quest.objects.exists():  # Check if there are any quests in the database - to avoid errors if it is an empty database
        # Check & Grant (if eligible) Grandmaster of EduQuest achievement
        grant_grandmaster_quest(user)

        # Filter ProfileAchievement objects for the current user
        achieved_quests = ProfileAchievement.objects.filter(user=user)
        achieved_quest_ids = list(achieved_quests.values_list('quest__id', flat=True))
        uncompleted_quests = all_quests.exclude(id__in=achieved_quests.values_list('quest', flat=True))

    return render(request, 'quests/quests_index.html', {'all_quests': all_quests, 'achieved_quest_ids': achieved_quest_ids, 'uncompleted_quests': uncompleted_quests })

@login_required
def quests_detail(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    user = request.user
    if Quest.objects.exists():
        # Check if the user has achieved the quest - returns a true or false
        achieved_quest = ProfileAchievement.objects.filter(user=user, quest=quest).exists()
    return render(request, 'quests/quests_detail.html', {'quest': quest, 'achieved_quest': achieved_quest })

#Subjects Views
@login_required
def subjects_index(request):
    subjects = Subject.objects.filter(user=request.user)
    upcoming_exams = subjects.filter(exam_date__gte=date.today()).order_by('exam_date')
    if Quest.objects.exists():
        # Check & Grant Exam Slayer quest
        grant_exam_slayer_quest(request.user)

    subjects_data = json.dumps([
        {'name': subject.name, 'progress': subject.progress} for subject in subjects
    ])
    upcoming_exams_data = json.dumps([
        {'name': exam.name, 'exam_date': exam.exam_date.strftime('%d-%m-%Y')} for exam in upcoming_exams
    ])
    all_quests = Quest.objects.all()

    return render(request, 'subjects/index.html', {'subjects': subjects, 'upcoming_exams_data': upcoming_exams_data, 'all_quests': all_quests, 'subjects_json': subjects_data})

@login_required
def subjects_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    current_date = datetime.now().date()
    exam_date = subject.exam_date
    exam_has_passed = exam_date < current_date

    return render(request, 'subjects/subject_detail.html', {'subject': subject, 'current_date': current_date, 'exam_has_passed': exam_has_passed })

@login_required
def subjects_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            if Quest.objects.exists():
                # Quest checks for Getting Started, Exam Slayer & Subject Explorer
                grant_getting_started_quest(request.user, subject)
                grant_exam_slayer_quest(request.user)
                grant_subject_explorer_quest(request.user)
            return redirect('subjects_detail', pk=subject.pk)
    else:
        form = SubjectForm()

    return render(request, 'subjects/subject_form.html', {'form': form, 'subject': None})

@login_required
def subjects_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()

            if Quest.objects.exists():
                # Quest checks Subject Explorer & Multitasking Maven
                grant_subject_explorer_quest(request.user)
                grant_multitasking_maven_quest(request.user)

            return redirect('subjects_detail', pk=pk)
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'subjects/subject_form.html', {'form': form, 'subject': subject})

@login_required
def subjects_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':

        subject.delete()
        return redirect('index')

    return render(request, 'subjects/subject_delete.html', {'subject': subject})

#About Leaderboards
def leaderboard(request):
    leaderboard_data = Profile.objects.all().order_by('-xp')
    current_user = request.user

    if current_user.is_authenticated:
        if Quest.objects.exists():
            grant_elite_leaderboard_quest()

    context = {
        'leaderboard_data': leaderboard_data,
    }
    return render(request, 'main_app/leaderboard.html', context)


# Assignments Views
class AssignmentDetail(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'

class AssignmentCreate(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = 'assignments/assignment_form.html'
    context_object_name = 'subjects'
    fields = ['name', 'description', 'due_date', 'status', 'subject']

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Checks if the status is 'completed', if so, sets the complete_date to today
        if form.cleaned_data['status'] == 'CM':
            form.instance.complete_date = timezone.now().date()

        response = super().form_valid(form)

        # Quest check for Master the Basics
        grant_master_the_basics_quest(self.request.user)

        return response

    def get_success_url(self):
        # Access the newly created assignment object and then its subject
        assignment = self.object
        return reverse('subjects_detail', kwargs={'pk': assignment.subject.pk})

class AssignmentUpdate(LoginRequiredMixin, UpdateView):
    model = Assignment
    template_name = 'assignments/assignment_form.html'
    context_object_name = 'assignment'
    fields = ['name', 'description', 'due_date', 'status', 'subject']

    # Overriding the form_valid to quest elibibility and add complete date (if they change the status)
    def form_valid(self, form):
        if form.cleaned_data['status'] == 'CM':
            # Checks if the status is 'completed', if so, sets the complete_date to today
            form.instance.complete_date = timezone.now().date()

        response = super().form_valid(form)

        # Quest Checks for Time Management Pro, Assignment Conqueror
        grant_time_management_pro_quest(self.request.user)
        grant_assignment_conqueror_quest(self.request.user)

        return response

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('assignments_detail', kwargs={'pk': pk})

class AssignmentDelete(LoginRequiredMixin, DeleteView):
    model = Assignment
    template_name = 'assignments/assignment_delete.html'
    context_object_name = 'assignment'

    def get_success_url(self):
        # Get the subject's pk from the created assignment instance
        subject_pk = self.object.subject.pk
        # Redirect to the subjects_detail page
        return reverse_lazy('subjects_detail', kwargs={'pk': subject_pk})


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
