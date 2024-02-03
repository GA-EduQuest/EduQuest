from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #About User
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('user/<int:user_id>/update/', views.user_update, name='user_update'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    #About Quest
    path('user/<int:user_id>/unfinishedquest/<int:quest_id>/', views.unfinished_quest, name='unfinished_quest'),
    path('user/<int:user_id>/finishedquest/<int:quest_id>/', views.finished_quest, name='finished_quest'),
    #About user earning badges
    path('user/<int:user_id>/unfinishedquest/<int:quest_id>/notownedbadges/<int:badge_id>', views.not_owned_badges, name='not_owned_badges'),
    path('user/<int:user_id>/finishedquest/<int:quest_id>/ownedbadges/<int:badge_id>', views.owned_badges, name='owned_badges'),
    #About Badges
    path('badges/', views.badges_list, name='badges_list'),
    path('badges/<int:badges_id>/', views.badges_detail, name='subjects_detail'),
    # ---Admin Only--- #
    path('badges/create', views.badges_create, name='badges_create'),
    path('badges/<int:badges_id>/update/', views.badges_update, name='badges_update'),
    path('badges/<int:badges>_id/delete/', views.badges_delete, name='badges_delete'),
    #About Subjects, main index is also here
    path('subjects/', views.subjects_index, name='index'),
    path('subjects/<int:assignments_id>/', views.subjects_detail, name='subjects_detail'),
    path('subjects/create', views.subjects_create, name='subjects_create'),
    path('subjects/<int:subjects_id>/update/', views.subjects_update, name='subjects_update'),
    path('subjects/<int:subjects_id>/delete/', views.subjects_delete, name='subjects_delete'),
    #About Assignment
    path('assignments/', views.AssignmentList.as_view(), name='assignments_list'),
    path('assignments/create/', views.AssignmentCreate.as_view(), name='assignments_create'),
    path('assignments/<int:pk>/update/', views.AssignmentUpdate.as_view(), name='assignments_update'),
    path('assignments/<int:pk>/delete/', views.AssignmentsDelete.as_view(), name='assignments_delete'),
    #About Leaderboards
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    #Signup
    path('accounts/signup/', views.signup, name='signup'),
]
