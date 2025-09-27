from django.urls import path
from .views import AnimalListCreateView

urlpatterns = [
    path('animais/', AnimalListCreateView.as_view(), name='animais-list-create'),
]
