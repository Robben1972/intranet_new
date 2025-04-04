from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Selection():
    class DepartmentsEN(models.TextChoices):
        IT = "IT", "IT"
        HR = "HR", "HR"
        MARKETING = "MARKETING", "Marketing"
        SALES = "SALES", "Sales"
        MANAGEMENT = "MANAGEMENT", "Management"
        ALL_Departments = "ALL", "All Departments"

    class DepartmentsRU(models.TextChoices):
        IT = "ИТ", "ИТ"
        HR = "HR", "HR"
        MARKETING = "МАРКЕТИНГ", "Маркетинг"
        SALES = "ПРОДАЖИ", "Продажи"
        MANAGEMENT = "УПРАВЛЕНИЕ", "Управление"
        ALL_Departments = "ВСЕ", "Все отделы"
    
    class DepartmentsUZ(models.TextChoices):
        IT = "IT", "IT"
        HR = "HR", "HR"
        MARKETING = "MARKETING", "Marketing"
        SALES = "SOTUV", "Sotuv"
        MANAGEMENT = "BOSHQARUV", "Boshqaruv"
        ALL_Departments = "BARCHA", "Barcha bo'limlar"
    
    class CategoryEN(models.TextChoices):
        MANDATORY = "Mandatory corporate trainings",
        PROFESSIONAL = "Professional development",
        LEADERSHIP = 'Leadership and Management',
        PERSONAL = 'Personal growth',
        TRAININGS = 'Trainings on company products',
        EXTERNAL = 'External courses and certifications'
    
    class CategoryRU(models.TextChoices):
        MANDATORY = "Требовательные корпоративные тренинги",
        PROFESSIONAL = "Профессиональное развитие",
        LEADERSHIP = 'Лидерство и управление',
        PERSONAL = 'Персональное рост',
        TRAININGS = 'Обучение на компанионных продуктах', 

    class CategoryUZ(models.TextChoices):
        MANDATORY = "Talabkor korporativ treninglar",
        PROFESSIONAL = "Kasbiy rivojlanish",
        LEADERSHIP = 'Etakchilik va boshqaruv',
        PERSONAL = 'Shaxsiy o\'sish',
        TRAININGS = 'Kompaniya mahsulotlari bo\'yicha trening',

class TrainingModel(models.Model):
    title_uz = models.CharField(max_length=255, blank=True)
    title_ru = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)
    description_uz = RichTextUploadingField(blank=True)
    description_ru = RichTextUploadingField(blank=True)
    description_en = RichTextUploadingField(blank=True)
    department_uz = models.CharField(max_length=255, blank=True, choices=Selection.DepartmentsUZ.choices)
    department_ru = models.CharField(max_length=255, blank=True, choices=Selection.DepartmentsRU.choices)
    department_en = models.CharField(max_length=255, blank=True, choices=Selection.DepartmentsEN.choices)
    location_uz = models.CharField(max_length=255, blank=True)
    location_ru = models.CharField(max_length=255, blank=True)
    location_en = models.CharField(max_length=255, blank=True)
    speaker_uz = models.CharField(max_length=255, blank=True)
    speaker_ru = models.CharField(max_length=255, blank=True)
    speaker_en = models.CharField(max_length=255, blank=True)
    category_uz = models.CharField(max_length=255, blank=True, choices=Selection.CategoryUZ.choices)
    category_ru = models.CharField(max_length=255, blank=True, choices=Selection.CategoryRU.choices)
    category_en = models.CharField(max_length=255, blank=True, choices=Selection.CategoryEN.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    image = models.CharField(max_length=255)
    video = models.CharField(max_length=255, blank=True)
    attachments = models.CharField(max_length=255, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title_uz or self.title_ru or self.title_en 

