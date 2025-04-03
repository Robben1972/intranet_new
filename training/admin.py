from django.contrib import admin
from .models import TrainingModel
# Register your models here.


@admin.register(TrainingModel)
class TrainingModelAdmin(admin.ModelAdmin):
    pass
