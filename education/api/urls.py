from django.urls import path, include
from .views import LessonsView, StaticsView, LessonsProductView

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('lessons/', LessonsView.as_view()),
    path('lessons/<int:pk>/', LessonsProductView.as_view()),
    path('static/', StaticsView.as_view()),
]