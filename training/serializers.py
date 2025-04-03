from rest_framework import serializers
from .models import TrainingModel

class TrainingSerializerEN(serializers.ModelSerializer):
    class Meta:
        model = TrainingModel
        fields = ('id', 'title_en', 'description_en', 'department_en', 'location_en', 'category_en', 'image', 'video', 'attachments', 'start_time', 'end_time', 'date')

class TrainingSerializerRU(serializers.ModelSerializer):
    class Meta:
        model = TrainingModel
        fields = ('id', 'title_ru', 'description_ru', 'department_ru', 'location_ru', 'category_ru', 'image', 'video', 'attachments', 'start_time', 'end_time', 'date')

class TrainingSerializerUZ(serializers.ModelSerializer):
    class Meta:
        model = TrainingModel
        fields = ('id', 'title_uz', 'description_uz', 'department_uz', 'location_uz', 'category_uz', 'image', 'video', 'attachments', 'start_time', 'end_time', 'date')
