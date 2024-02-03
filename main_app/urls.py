from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('subjects/', views.subjects_index, name='index'),
  path('subjects/<int:assignments_id>/', views.subjects_detail, name='subjects_detail'),
  path('subjects/create', views.subjects_create, name='subjects_create'),
  path('subjects/<int:subjects_id>/update/', views.subjects_update, name='subjects_update'),
  path('subjects/<int:subjects_id>/delete/', views.subjects_delete, name='subjects_delete'),
]
