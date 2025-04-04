from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TrainingModel

@receiver(post_save, sender=TrainingModel)
def print_news_data(sender, instance, created, **kwargs):
    if created:
        print(f"New Training Created: {instance}")