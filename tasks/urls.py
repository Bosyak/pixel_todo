from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('board/', views.board_view, name='board'),
    path('create/', views.create_task, name='create'),
    path('<int:pk>/edit/', views.edit_task, name='edit'),
    path('<int:pk>/delete/', views.delete_task, name='delete'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/calendar/events/', views.calendar_events, name='calendar_events'),
]
