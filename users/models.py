from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    @property
    def character_or_create(self):
        from .models import Character
        char, _ = Character.objects.get_or_create(
            user=self,
            defaults={'name': self.username, 'class_type': 'warrior'},
        )
        return char


class Character(models.Model):
    CLASS_CHOICES = [
        ('warrior', 'Воин'),
        ('mage', 'Маг'),
        ('archer', 'Лучник'),
    ]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='character'
    )
    name = models.CharField(max_length=50)
    class_type = models.CharField(max_length=20, choices=CLASS_CHOICES)
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    sprite = models.CharField(max_length=100, default='warrior')

    @property
    def exp_to_next_level(self):
        return self.level * 100

    @property
    def exp_percent(self):
        if self.exp_to_next_level == 0:
            return 0
        return min(100, int(self.experience / self.exp_to_next_level * 100))

    @property
    def avatar_url(self):
        return f'https://api.dicebear.com/7.x/pixel-art/svg?seed={self.name}'

    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
        self.save()

    def __str__(self):
        return f'{self.name} (Ур. {self.level})'
