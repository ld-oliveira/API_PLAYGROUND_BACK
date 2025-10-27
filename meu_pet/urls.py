from django.urls import path
from .views import AnimalListCreateView, AnimalDetailView

urlpatterns = [
    path('animais/', AnimalListCreateView.as_view(), name='animais-list-create'),
    path('animais/<int:pk>/', AnimalDetailView.as_view(), name='animais-detail'),
]
