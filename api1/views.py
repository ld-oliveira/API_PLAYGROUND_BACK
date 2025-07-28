from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from decouple import config

API_KEY = config('TOMORROW_API_KEY')


def clima(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')

    if not latitude or not longitude:
        return JsonResponse({'erro': 'Latitude e longitude são obrigatórios.'}, status=400)

    url = f"https://api.tomorrow.io/v4/weather/realtime?location={latitude},{longitude}&apikey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        print("Resposta da API /clima:")
        print(json.dumps(data, indent=2))

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


def proximas(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')

    if not latitude or not longitude:
        return JsonResponse({'erro': 'Latitude e longitude são obrigatórios.'}, status=400)

    url = "https://api.tomorrow.io/v4/weather/forecast"
    params = {
        "location": f"{latitude},{longitude}",
        "timesteps": "1h",
        "units": "metric",
        "fields": "temperature",
        "apikey": API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        previsoes = data.get("timelines", {}).get("hourly", [])

        if not previsoes:
            return JsonResponse({'erro': 'Nenhuma previsão encontrada.'}, status=404)

        # Retorna as 6 primeiras previsões horárias
        previsao_6h = previsoes[:6]

        return JsonResponse(previsao_6h, safe=False)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)



def amanha(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')
    
    if not latitude or not longitude:
        return JsonResponse({'erro': 'Latitude e longitude são obrigatórios.'}, status=400)
    
    url = "https://api.tomorrow.io/v4/weather/forecast"
    params = {
        "location": f"{latitude},{longitude}",
        "timesteps": "1d",
        "units": "metric",
        "fields": "temperatureAvg",
        "apikey": API_KEY,
    }

    try:
        response = requests.get(url, params=params)  # corrigido aqui
        data = response.json()
        
        amanha = data.get("timelines", {}).get("daily", [])
        
        if len(amanha) < 2:  # verificação segura
            return JsonResponse({'erro': 'Previsão de amanhã indisponível.'}, status=404)
        
        previsao_amanha = amanha[1]  # segundo item: amanhã
        
        return JsonResponse(previsao_amanha, safe=False)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
