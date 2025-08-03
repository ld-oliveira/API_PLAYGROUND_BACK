from django.http import JsonResponse
from clima.services.tomorrow_api import requisitar

def clima_atual(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'erro': 'Latitude e longitude são obrigatórios.'}, status=400)

    try:
        dados = requisitar("realtime", {
            "location": f"{lat},{lon}",
        })
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
