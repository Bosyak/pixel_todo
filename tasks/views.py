from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Task, Tag
from .forms import TaskForm


def _user_tasks(user):
    owned = Task.objects.filter(owner=user)
    shared = Task.objects.filter(shared_with=user)
    return (owned | shared).distinct()


@login_required
def board_view(request):
    tasks = _user_tasks(request.user)

    weekdays = {i: {'name': name, 'tasks': []} for i, name in Task.WEEKDAY_CHOICES}
    for task in tasks:
        for day in (task.weekdays or []):
            if day in weekdays:
                weekdays[day]['tasks'].append(task)

    return render(request, 'tasks/board.html', {
        'weekdays': weekdays,
        'character': request.user.character_or_create,
    })


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'Монстр создан!')
            return redirect('tasks:board')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {
        'form': form, 'title': 'Создать задание',
    })


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        messages.error(request, 'Нет доступа')
        return redirect('tasks:board')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задание обновлено!')
            return redirect('tasks:board')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {
        'form': form, 'title': 'Редактировать задание',
    })


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        messages.error(request, 'Нет доступа')
        return redirect('tasks:board')
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задание удалено')
    return redirect('tasks:board')


@login_required
def calendar_view(request):
    return render(request, 'tasks/calendar.html')


@login_required
def calendar_events(request):
    tasks = _user_tasks(request.user)

    start_param = request.GET.get('start')
    end_param = request.GET.get('end')

    if start_param:
        start_date = datetime.fromisoformat(start_param.replace('Z', '')).date()
    else:
        start_date = timezone.now().date().replace(day=1)

    if end_param:
        end_date = datetime.fromisoformat(end_param.replace('Z', '')).date()
    else:
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)

    events = []
    current = start_date
    while current <= end_date:
        wd = current.weekday()
        for task in tasks:
            if wd in (task.weekdays or []):
                color = {
                    'easy': '#4CAF50',
                    'medium': '#FF9800',
                    'hard': '#F44336',
                }.get(task.difficulty, '#2196F3')
                time_str = task.scheduled_time.strftime('%H:%M') if task.scheduled_time else '09:00'
                events.append({
                    'id': f'{task.id}-{current.isoformat()}',
                    'title': task.title,
                    'start': f'{current.isoformat()}T{time_str}:00',
                    'color': color,
                    'textColor': '#fff',
                    'extendedProps': {
                        'taskId': task.id,
                        'difficulty': task.get_difficulty_display(),
                        'tags': [t.name for t in task.tags.all()],
                        'duration': task.duration_minutes,
                        'status': task.get_status_display(),
                        'exp': task.exp_reward,
                        'monster': task.monster_sprite,
                    },
                })
        current += timedelta(days=1)
    return JsonResponse(events, safe=False)
