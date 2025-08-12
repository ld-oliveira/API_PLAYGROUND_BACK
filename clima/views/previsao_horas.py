from django.http import JsonResponse
from clima.services.tomorrow_api import requisitar

def previsao_proximas_horas(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'erro': 'Latitude e longitude são obrigatórios.'}, status=400)


    try:
        dados = requisitar("forecast", {
            "location": f"{lat},{lon}",
            "timesteps": "1h",
            "units": "metric",
            "fields": "temperature,precipitationProbability,visibility",
        })
        previsoes = dados.get("timelines", {}).get("hourly", [])
        if not previsoes:
            return JsonResponse({'erro': 'Nenhuma previsão encontrada.'}, status=404)
        return JsonResponse(previsoes[:6], safe=False)
    
    
    
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


