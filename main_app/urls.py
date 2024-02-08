from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #About User
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    #About Profile
    path('user/<int:pk>/update', views.ProfileUpdate.as_view(), name='profile_update'),
    #About Quest
    path('quests/', views.quests_index, name='quests_index'),
    path('quests/<int:pk>/', views.quests_detail, name='quests_detail'),
    # ---Admin Only--- #
    #About Subjects, main index is also here
    path('subjects/', views.subjects_index, name='index'),
    path('subjects/create', views.subjects_create, name='subjects_create'),
    path('subjects/<int:pk>/', views.subjects_detail, name='subjects_detail'),
    path('subjects/<int:pk>/update/', views.subjects_update, name='subjects_update'),
    path('subjects/<int:pk>/delete/', views.subjects_delete, name='subjects_delete'),
    #About Assignment
    path('assignments/create/', views.AssignmentCreate.as_view(), name='assignments_create'),
    path('assignments/<int:pk>', views.AssignmentDetail.as_view(), name='assignments_detail'),
    path('assignments/<int:pk>/update/', views.AssignmentUpdate.as_view(), name='assignments_update'),
    path('assignments/<int:pk>/delete/', views.AssignmentDelete.as_view(), name='assignments_delete'),
    #About Leaderboards
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    #Signup
    path('accounts/signup/', views.signup, name='signup'),
]
