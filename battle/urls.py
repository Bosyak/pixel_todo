from django.urls import path
from . import views

app_name = 'battle'

urlpatterns = [
    path('start/<int:task_id>/', views.start_battle, name='start'),
    path('finish/<int:task_id>/', views.finish_battle, name='finish'),
]
