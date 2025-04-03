from django.urls import path
from .views import TrainingListViewEN, TrainingListViewRU, TrainingListViewUZ, TrainingDetailViewRU, TrainingDetailViewEN, TrainingDetailViewUZ

urlpatterns = [
    path('uz/', TrainingListViewUZ.as_view()),
    path('ru/', TrainingListViewRU.as_view()),
    path('en/', TrainingListViewEN.as_view()),
    path('uz/<int:pk>/', TrainingDetailViewUZ.as_view()),
    path('ru/<int:pk>/', TrainingDetailViewRU.as_view()),
    path('en/<int:pk>/', TrainingDetailViewEN.as_view()),
]
