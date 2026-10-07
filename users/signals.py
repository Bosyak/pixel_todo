from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Character


@receiver(post_save, sender=CustomUser)
def create_character_for_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'character'):
        Character.objects.create(
            user=instance,
            name=instance.username,
            class_type='warrior',
        )
