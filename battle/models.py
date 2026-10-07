from django.db import models
from django.conf import settings


class BattleLog(models.Model):
    task = models.ForeignKey(
        'tasks.Task', on_delete=models.CASCADE, related_name='battles'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    damage_dealt = models.PositiveIntegerField(default=0)
    victory = models.BooleanField(default=False)
    exp_gained = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Битва: {self.task.title}'
