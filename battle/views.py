from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from tasks.models import Task
from .models import BattleLog


def _has_access(task, user):
    return task.owner == user or task.shared_with.filter(pk=user.pk).exists()


@login_required
def start_battle(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not _has_access(task, request.user):
        return redirect('tasks:board')

    if task.status == 'pending':
        task.status = 'in_progress'
        task.started_at = timezone.now()
        task.save()
        BattleLog.objects.create(task=task, user=request.user)

    return render(request, 'battle/arena.html', {
        'task': task,
        'monster_hp': task.monster_hp,
    })


@login_required
def finish_battle(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not _has_access(task, request.user):
        return JsonResponse({'error': 'forbidden'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    task.status = 'completed'
    task.completed_at = timezone.now()
    task.save()

    character = request.user.character_or_create
    exp = task.exp_reward
    character.add_experience(exp)

    battle = task.battles.filter(user=request.user, victory=False).first()
    if battle:
        battle.finished_at = timezone.now()
        battle.victory = True
        battle.exp_gained = exp
        battle.save()

    return JsonResponse({
        'success': True,
        'exp_gained': exp,
        'new_level': character.level,
        'character_exp': character.experience,
        'exp_to_next': character.exp_to_next_level,
    })
