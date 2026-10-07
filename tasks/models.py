from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=7, default='#FFD700')

    def __str__(self):
        return self.name


class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]

    WEEKDAY_CHOICES = [
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
    ]

    MONSTER_CHOICES = [
        ('slime', 'Слизень'),
        ('bat', 'Летучая мышь'),
        ('skeleton', 'Скелет'),
        ('orc', 'Орк'),
        ('dragon', 'Дракон'),
        ('goblin', 'Гоблин'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default='easy'
    )
    tags = models.ManyToManyField(Tag, blank=True)
    weekdays = models.JSONField(default=list)

    duration_minutes = models.PositiveIntegerField(default=30)
    scheduled_time = models.TimeField(null=True, blank=True)
    repeat = models.CharField(
        max_length=20,
        choices=[
            ('none', 'Без повтора'),
            ('daily', 'Ежедневно'),
            ('weekly', 'Еженедельно'),
            ('monthly', 'Ежемесячно'),
        ],
        default='none',
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_tasks',
    )
    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='shared_tasks',
    )
    is_group = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    monster_sprite = models.CharField(
        max_length=100, default='slime', choices=MONSTER_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_time', 'difficulty']

    @property
    def exp_reward(self):
        return {'easy': 10, 'medium': 25, 'hard': 50}.get(self.difficulty, 10)

    @property
    def monster_hp(self):
        return {'easy': 30, 'medium': 60, 'hard': 100}.get(self.difficulty, 30)

    @property
    def monster_cdn_url(self):
        codes = {
            'slime': '1f47e',
            'bat': '1f987',
            'skeleton': '1f480',
            'orc': '1f479',
            'dragon': '1f409',
            'goblin': '1f47a',
        }
        code = codes.get(self.monster_sprite, '1f47e')
        return f'https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/72x72/{code}.png'

    def get_weekday_display(self):
        return [dict(self.WEEKDAY_CHOICES).get(d) for d in (self.weekdays or [])]

    def __str__(self):
        return self.title
