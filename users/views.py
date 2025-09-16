from django.shortcuts import render
from users.forms import LoginForms
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def cadastro(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405, content_type="application/json")

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "JSON inválido", "message": str(e)}, status=400, content_type="application/json")

    nome = data.get("nome_cad")
    email = data.get("email_cad")
    senha_1 = data.get("senha_1")
    senha_2 = data.get("senha_2")

    if not all([nome, email, senha_1, senha_2]):
        return JsonResponse({
            "error": "Todos os campos são obrigatórios", 
            "received_data": {"nome": nome, "email": email, "senha_1": senha_1, "senha_2": senha_2}
        }, status=400, content_type="application/json")

    if senha_1 != senha_2:
        return JsonResponse({"error": "As senhas não coincidem"}, status=400, content_type="application/json")

    # Verificação de duplicação de usuário ou email
    if User.objects.filter(username=nome).exists():
        return JsonResponse({"error": "Usuário já existe"}, status=400, content_type="application/json")

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email já cadastrado"}, status=400, content_type="application/json")

    try:
        usuario = User.objects.create_user(
            username=nome,
            email=email,
            password=senha_1
        )
        usuario.save()
        return JsonResponse({"status": "ok", "message": "Cadastro realizado com sucesso"}, status=201, content_type="application/json")
    except Exception as e:
        print("Erro ao criar usuário:", e)
        return JsonResponse({"error": "Erro ao criar usuário", "details": str(e)}, status=500, content_type="application/json")

def login(request):
    form = LoginForms()
    return render(request, 'login.html', {"form": form})
