from rest_framework import serializers
from .models import News

class NewsSerializerUZ(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title_uz', 'description_uz', 'department_uz', 'image', 'created_at')

class NewsSerializerRU(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title_ru', 'description_ru', 'department_ru', 'image', 'created_at')

class NewsSerializerEN(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title_en', 'description_en', 'department_en', 'image', 'created_at')