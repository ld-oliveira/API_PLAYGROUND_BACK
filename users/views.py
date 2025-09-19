from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login
import json
import logging
from django.contrib.auth import logout as auth_logout


logger = logging.getLogger(__name__)

@csrf_exempt #atenção ao usar isso. se possivel evitar.
@require_POST
def cadastro(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "JSON inválido", "message": str(e)})

    nome = data.get("nome_cad")
    email = data.get("email_cad")
    senha_1 = data.get("senha_1")
    senha_2 = data.get("senha_2")

    if not all([nome, email, senha_1, senha_2]):
        return JsonResponse({
            "error": "Todos os campos são obrigatórios",
            "received_data": {"nome": nome, "email": email}
        })

    if senha_1 != senha_2:
        return JsonResponse({"error": "As senhas não coincidem"})

    if User.objects.filter(username__iexact=nome).exists(): #iexact = evitar problemas com maiusculas e minusculas
        return JsonResponse({"error": "Usuário já existe"})

    if User.objects.filter(email__iexact=email).exists():
        return JsonResponse({"error": "Email já cadastrado"})

    try:
        User.objects.create_user(username=nome, email=email, password=senha_1)
        return JsonResponse({"status": "ok", "message": "Cadastro realizado com sucesso"})
    except Exception as e:
        logger.error("Erro ao criar usuário: %s", e)
        return JsonResponse({"error": "Erro ao criar usuário", "details": str(e)})


@csrf_exempt
@require_POST
def login_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JsonResponse({"error": "JSON inválido", "message": str(e)})

    nome = data.get("nome_login")
    senha = data.get("senha_login")

    if not all([nome, senha]):
        return JsonResponse({
            "error": "Todos os campos são obrigatórios",
            "received_data": {"nome": nome}
        })

    user = authenticate(request, username=nome, password=senha)

    if user is not None:
        auth_login(request, user)
        return JsonResponse({"status": "ok", "message": "Login realizado com sucesso"})
    else:
        return JsonResponse({"error": "Usuário ou senha inválidos"})
    
@require_POST
def logout_user(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return JsonResponse({"status": "ok", "message": "Logout realizado com sucesso"})
    else:
        return JsonResponse({"error": "Usuário não está logado"})
