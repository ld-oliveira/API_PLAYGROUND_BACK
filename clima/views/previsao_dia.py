from django.http import JsonResponse
from clima.services.tomorrow_api import requisitar

def previsao_dia_seguinte(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')

    if not latitude or not longitude:
        return JsonResponse({'erro': 'Latitude e longitude são obrigatórios.'}, status=400)

    try:
        dados = requisitar("forecast", {
            "location": f"{latitude},{longitude}",
            "timesteps": "1d",
            "units": "metric",
            "fields": "temperature,precipitationProbability",
        })

        previsoes = dados.get("timelines", {}).get("daily", [])
        if len(previsoes) < 2:
            return JsonResponse({'erro': 'Não foi possível obter a previsão do dia seguinte.'}, status=404)

        dia_seguinte = previsoes[1]
        return JsonResponse(dia_seguinte, safe=False)

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
