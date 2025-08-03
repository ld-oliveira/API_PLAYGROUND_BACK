import requests
from django.conf import settings
from decouple import config

API_KEY = config('TOMORROW_API_KEY')

def requisitar(endpoint, params=None):
    base_url = f"https://api.tomorrow.io/v4/weather/{endpoint}"
    
    if params is None:
        params={}
    params["apikey"] = API_KEY
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()
    