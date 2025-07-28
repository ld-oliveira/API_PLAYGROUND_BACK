from django.shortcuts import render
from django.http import JsonResponse
import requests

def hello_world(request):
    return JsonResponse({'mensagem': 'Olá, mundo!'})