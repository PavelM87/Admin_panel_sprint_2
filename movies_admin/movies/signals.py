import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from movies.models import Person

@receiver(post_save, sender=Person)
def congratulatory(sender, instance, created, **kwargs):
    if created and instance.birth_date == datetime.date.today():
        print(f"У {instance.full_name} сегодня день рождения! 🥳")
