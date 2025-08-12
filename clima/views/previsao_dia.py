from django.http import JsonResponse
from clima.services.tomorrow_api import requisitar

def previsao_dia_seguinte(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'erro': 'Latitude e longitude são obrigatórios.'}, status=400)

    try:
        dados = requisitar("forecast", {
            "location": f"{lat},{lon}",
            "timesteps": "1d",
            "units": "metric",
            "fields": "temperatureMax,temperatureMin,temperatureAvg,precipitationProbability,visibilityAvg,windSpeedAvg",
        })

        previsoes = dados.get("timelines", {}).get("daily", [])
        if len(previsoes) < 4:
            return JsonResponse({'erro': 'Não há dados suficientes para amanhã, +2 e +3 dias.'}, status=404)

        def pick(i):
            v = previsoes[i].get("values", {})
            return {
                "min": v.get("temperatureMin"),
                "max": v.get("temperatureMax"),
                "avg": v.get("temperatureAvg"),
                "chuva": v.get("precipitationProbability"),
                "visib": v.get("visibilityAvg"),
                "vento": v.get("windSpeedAvg"),
                "time": previsoes[i].get("time"),
            }

        resultado = {
            "amanha": pick(1),
            "depois_de_amanha": pick(2),
            "terceiro_dia": pick(3),
        }
        return JsonResponse(resultado)

    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
