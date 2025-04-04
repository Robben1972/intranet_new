import asyncio
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from asgiref.sync import sync_to_async
from training.models import TrainingModel  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Checks and archives past trainings every hour'

    # Make these methods async-compatible
    @sync_to_async
    def get_trainings(self):
        return list(TrainingModel.objects.filter(archived=False))

    @sync_to_async
    def save_training(self, training):
        training.save()
        return training

    async def archive_past_trainings(self):
        while True:
            try:
                now = timezone.now()
                # Get trainings using async-compatible method
                trainings = await self.get_trainings()
                archived_count = 0
                
                for training in trainings:
                    # Combine date and end_time to create a full datetime
                    training_end = timezone.make_aware(
                        datetime.combine(training.date, training.end_time)
                    )
                    
                    # If training has ended, archive it
                    if training_end < now:
                        training.archived = True
                        await self.save_training(training)
                        archived_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Archived training: {training}')
                        )
                
                if archived_count == 0:
                    self.stdout.write(
                        self.style.SUCCESS('No trainings needed archiving')
                    )
                
                # Wait for 1 hour (3600 seconds)
                await asyncio.sleep(60)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error in archive task: {str(e)}')
                )
                # Wait 5 minutes before retrying if there's an error
                await asyncio.sleep(300)

    def handle(self, *args, **options):
        self.stdout.write('Starting training archive task...')
        asyncio.run(self.archive_past_trainings())