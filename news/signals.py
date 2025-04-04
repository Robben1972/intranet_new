from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News

@receiver(post_save, sender=News)
def print_news_data(sender, instance, created, **kwargs):
    if created:
        print(f"New News Created: {instance}")