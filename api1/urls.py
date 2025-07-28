from django.urls import path
from .views import clima, proximas, amanha

urlpatterns = [
    path('clima/', clima),
    path('proximas/', proximas),
    path('amanha/', amanha)
]