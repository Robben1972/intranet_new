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


class News(models.Model):
    title_uz = models.CharField(max_length=200, blank=True)
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    description_uz = RichTextUploadingField(blank=True)
    description_ru = RichTextUploadingField(blank=True)
    description_en = RichTextUploadingField(blank=True)
    department_uz = models.CharField(max_length=200, blank=True, choices=Selection.DepartmentsUZ.choices)
    department_ru = models.CharField(max_length=200, blank=True, choices=Selection.DepartmentsRU.choices)
    department_en = models.CharField(max_length=200, blank=True, choices=Selection.DepartmentsEN.choices)
    image = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_uz or self.title_en or self.title_ru or "No Title"