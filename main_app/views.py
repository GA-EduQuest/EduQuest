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



#Create your views here.

#Basic Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

#User Views
@login_required
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
@login_required
def quests_index(request):
    user = request.user
    all_quests = Quest.objects.all()

    if Quest.objects.exists():  # Check if there are any quests in the database
        # Check Grandmaster of EduQuest achievement
        grandmaster_quest_name = 'Grandmaster of EduQuest'
        is_grandmaster = Quest.is_grandmaster(user)
        if is_grandmaster and not ProfileAchievement.has_quest_achievement(user, grandmaster_quest_name):
            grandmaster_quest = Quest.objects.get(name=grandmaster_quest_name)
            ProfileAchievement.objects.create(user=user, quest=grandmaster_quest)
            user.profile.xp += ProfileAchievement.get_quest_xp(grandmaster_quest_name)
            user.profile.save()

        # Filter ProfileAchievement objects for the current user
        achieved_quests = ProfileAchievement.objects.filter(user=user)
        achieved_quest_ids = list(achieved_quests.values_list('quest__id', flat=True))
        uncompleted_quests = all_quests.exclude(id__in=achieved_quests.values_list('quest', flat=True))

    return render(request, 'quests/quests_index.html', {'all_quests': all_quests, 'achieved_quest_ids': achieved_quest_ids, 'uncompleted_quests': uncompleted_quests })

@login_required
def quests_detail(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    user = request.user
    if Quest.objects.exists():  # Check if there are any quests in the database
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
@login_required
def subjects_index(request):
    subjects = Subject.objects.filter(user=request.user)
    upcoming_exams = subjects.filter(exam_date__gte=date.today()).order_by('exam_date')
    if Quest.objects.exists():  # Check if there are any quests in the database
        # Exam Slayer Quest Check
        exam_slayer_quest_name = 'Exam Slayer'
        if not ProfileAchievement.has_quest_achievement(request.user, exam_slayer_quest_name):
            subjects_with_passed_exams = Subject.objects.filter(user=request.user, exam_date__lt=date.today())
            if subjects_with_passed_exams.exists():
                exam_slayer_quest = Quest.objects.get(name=exam_slayer_quest_name)
                ProfileAchievement.objects.create(user=request.user, quest=exam_slayer_quest)
                request.user.profile.xp += ProfileAchievement.get_quest_xp(exam_slayer_quest_name)
                request.user.profile.save()

    upcoming_exams_data = json.dumps([
        {'name': exam.name, 'exam_date': exam.exam_date.strftime('%d-%m-%Y')} for exam in upcoming_exams
    ])
    all_quests = Quest.objects.all()

    return render(request, 'subjects/index.html', {'subjects': subjects, 'upcoming_exams_data': upcoming_exams_data, 'all_quests': all_quests})

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
            if Quest.objects.exists():  # Check if there are any quests in the database
                # Getting Started Quest Check
                getting_started_quest_name = 'Getting Started'
                if not ProfileAchievement.has_quest_achievement(request.user, getting_started_quest_name):
                    existing_subjects_count = Subject.objects.filter(user=request.user).exclude(pk=subject.pk).count()
                    if existing_subjects_count == 0:
                        getting_started_quest = Quest.objects.get(name=getting_started_quest_name)
                        ProfileAchievement.objects.create(user=request.user, quest=getting_started_quest)
                        request.user.profile.xp += ProfileAchievement.get_quest_xp(getting_started_quest_name)
                        request.user.profile.save()
                # Exam Slayer Quest Check
                exam_slayer_quest_name = 'Exam Slayer'
                if not ProfileAchievement.has_quest_achievement(request.user, exam_slayer_quest_name):
                    subjects_with_passed_exams = Subject.objects.filter(user=request.user, exam_date__lt=date.today())
                    if subjects_with_passed_exams.exists():
                        exam_slayer_quest = Quest.objects.get(name=exam_slayer_quest_name)
                        ProfileAchievement.objects.create(user=request.user, quest=exam_slayer_quest)
                        request.user.profile.xp += ProfileAchievement.get_quest_xp(exam_slayer_quest_name)
                        request.user.profile.save()
                # Subject Explorer Quest Check
                subject_explorer_quest_name = 'Subject Explorer'
                subjects_count_by_field = Subject.objects.filter(user=request.user).values('field').distinct().count()
                if subjects_count_by_field >= 4 and not ProfileAchievement.has_quest_achievement(request.user, subject_explorer_quest_name):
                    subject_explorer_quest = Quest.objects.get(name=subject_explorer_quest_name)
                    ProfileAchievement.objects.create(user=request.user, quest=subject_explorer_quest)
                    request.user.profile.xp += ProfileAchievement.get_quest_xp(subject_explorer_quest_name)
                    request.user.profile.save()
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

            if Quest.objects.exists():  # Check if there are any quests in the database
                # Subject Explorer Quest Check
                subject_explorer_quest_name = 'Subject Explorer'
                subjects_count_by_field = Subject.objects.filter(user=request.user).values('field').distinct().count()
                if subjects_count_by_field >= 4 and not ProfileAchievement.has_quest_achievement(request.user, subject_explorer_quest_name):
                    subject_explorer_quest = Quest.objects.get(name=subject_explorer_quest_name)
                    ProfileAchievement.objects.create(user=request.user, quest=subject_explorer_quest)
                    request.user.profile.xp += ProfileAchievement.get_quest_xp(subject_explorer_quest_name)
                    request.user.profile.save()

                # Check Multitasking Maven achievement after subject update
                multitasking_maven_quest_name = 'Multitasking Maven'
                if Quest.is_multitasking_maven(request.user) and not ProfileAchievement.has_quest_achievement(request.user, multitasking_maven_quest_name):
                    multitasking_maven_quest = Quest.objects.get(name=multitasking_maven_quest_name)
                    ProfileAchievement.objects.create(user=request.user, quest=multitasking_maven_quest)
                    request.user.profile.xp += ProfileAchievement.get_quest_xp(multitasking_maven_quest_name)
                    request.user.profile.save()

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
        if Quest.objects.exists():  # Check if there are any quests in the database
            # Check if the current user is at the top of the leaderboard for Elite Leaderboard Champion Quest
            is_elite_champion = leaderboard_data.first() == current_user.profile
            elite_champion_quest_name = 'Elite Leaderboard Champion'
            if is_elite_champion and not ProfileAchievement.has_quest_achievement(current_user, elite_champion_quest_name):
                elite_champion_quest = Quest.objects.get(name=elite_champion_quest_name)
                ProfileAchievement.objects.create(user=current_user, quest=elite_champion_quest)
                current_user.profile.xp += ProfileAchievement.get_quest_xp(elite_champion_quest_name)
                current_user.profile.save()

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

        # Check Master the basics quest
        if self.check_master_the_basics():
            self.grant_master_the_basics_quest()

        return response

    def check_master_the_basics(self):
        # Count the number of subjects created by the user
        subject_count = Subject.objects.filter(user=self.request.user).count()
        return subject_count >= 4

    def grant_master_the_basics_quest(self):
        master_the_basics_quest_name = 'Master the Basics'
        if not ProfileAchievement.has_quest_achievement(self.request.user, master_the_basics_quest_name):
            master_the_basics_quest = Quest.objects.get(name=master_the_basics_quest_name)
            ProfileAchievement.objects.create(user=self.request.user, quest=master_the_basics_quest)
            self.request.user.profile.xp += ProfileAchievement.get_quest_xp(master_the_basics_quest_name)
            self.request.user.profile.save()

    def check_time_management_pro(self):
        # Count the number of completed assignments before their due date
        completed_assignments = Assignment.objects.filter(
            user=self.request.user,
            status='CM',
            complete_date__lte=F('due_date')
        ).count()
        return completed_assignments >= 2

    def get_success_url(self):
        # Access the newly created assignment object and then its subject
        assignment = self.object
        return reverse('subjects_detail', kwargs={'pk': assignment.subject.pk})

class AssignmentUpdate(LoginRequiredMixin, UpdateView):
    model = Assignment
    template_name = 'assignments/assignment_form.html'
    context_object_name = 'assignment'
    fields = ['name', 'description', 'due_date', 'status', 'subject']

    # Overriding the form_valid to check if they qualify for the Assignment Conqueror quest (1 assignment complete)
    def form_valid(self, form):
        if form.cleaned_data['status'] == 'CM':
            # Checks if the status is 'completed', if so, sets the complete_date to today
            form.instance.complete_date = timezone.now().date()

            # Check if the user qualifies for the Time Management Pro quest
            if self.check_time_management_pro():
                self.grant_time_management_pro_quest()

            # Check if the user qualifies for the Assignment Conqueror quest
            user = self.request.user
            quest_name = 'Assignment Conqueror'
            if not ProfileAchievement.has_quest_achievement(user, quest_name):
                quest = Quest.objects.get(name=quest_name)
                ProfileAchievement.objects.create(user=user, quest=quest)
                user.profile.xp += ProfileAchievement.get_quest_xp(quest_name)
                user.profile.save()

        return super().form_valid(form)

    def check_time_management_pro(self):
        # Count the number of completed assignments before their due date for the current user
        completed_assignments = Assignment.objects.filter(
            status='CM',
            complete_date__lte=F('due_date'),
            subject__user=self.request.user  # Filter assignments by subject user
        ).count()
        print(completed_assignments)
        return completed_assignments >= 2

    def grant_time_management_pro_quest(self):
        time_management_pro_quest_name = 'Time Management Pro'
        if not ProfileAchievement.has_quest_achievement(self.request.user, time_management_pro_quest_name):
            time_management_pro_quest = Quest.objects.get(name=time_management_pro_quest_name)
            ProfileAchievement.objects.create(user=self.request.user, quest=time_management_pro_quest)
            self.request.user.profile.xp += ProfileAchievement.get_quest_xp(time_management_pro_quest_name)
            self.request.user.profile.save()

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
