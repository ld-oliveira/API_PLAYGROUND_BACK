from django.urls import path
from .views import clima, proximas, amanha
from . import views

urlpatterns = [
    path('clima/', views.clima),
    path('proximas/',views.proximas),
    path('amanha/', views.amanha)
]