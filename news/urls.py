from django.urls import path
from .views import NewsListViewEN, NewsListViewRU, NewsListViewUZ, NewsDetailViewEN, NewsDetailViewUZ, NewsDetailViewRU

urlpatterns = [
    path('uz/', NewsListViewUZ.as_view()),
    path('ru/', NewsListViewRU.as_view()),
    path('en/', NewsListViewEN.as_view()),
    path('uz/<int:pk>/', NewsDetailViewUZ.as_view()),
    path('ru/<int:pk>/', NewsDetailViewRU.as_view()),
    path('en/<int:pk>/', NewsDetailViewEN.as_view()),
]
