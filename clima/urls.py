from django.urls import path
from clima.views.temperatura import clima_atual
from clima.views.previsao_horas import previsao_proximas_horas
from clima.views.previsao_dia import previsao_dia_seguinte

urlpatterns = [
    path('clima/', clima_atual),
    path('previsao-horas/', previsao_proximas_horas),
    path('previsao-dia/', previsao_dia_seguinte),
]
