from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #About User
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('user/<int:user_id>/update/', views.user_update, name='user_update'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    #About Subjects
    path('subjects/', views.subjects_index, name='index'),
    path('subjects/<int:assignments_id>/', views.subjects_detail, name='subjects_detail'),
    path('subjects/create', views.subjects_create, name='subjects_create'),
    path('subjects/<int:subjects_id>/update/', views.subjects_update, name='subjects_update'),
    path('subjects/<int:subjects_id>/delete/', views.subjects_delete, name='subjects_delete'),
    #About Assignment
    path('assignments/<int:pk>/', views.AssignmentDetail.as_view(), name='assignments_detail'),
    path('assignments/create/', views.AssignmentCreate.as_view(), name='assignments_create'),
    path('assignments/<int:pk>/update/', views.AssignmentUpdate.as_view(), name='assignments_update'),
    path('assignments/<int:pk>/delete/', views.AssignmentsDelete.as_view(), name='assignments_delete'),
    #Signup
    path('accounts/signup/', views.signup, name='signup'),
]
