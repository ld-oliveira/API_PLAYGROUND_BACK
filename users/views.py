from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
import json
import logging

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def get_csrf(request):
    """
    Retorna o CSRF token em JSON e garante que o cookie 'csrftoken' seja setado.
    """
    token = get_token(request)
    resp = JsonResponse({"csrfToken": token})
    resp["Set-Cookie"] = (
        f"csrftoken={token}; Path=/; Secure; SameSite=None; Partitioned"
    )
    return resp

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

    if User.objects.filter(username__iexact=nome).exists():
        return JsonResponse({"error": "Usuário já existe"})

    if User.objects.filter(email__iexact=email).exists():
        return JsonResponse({"error": "Email já cadastrado"})

    try:
        User.objects.create_user(username=nome, email=email, password=senha_1)
        return JsonResponse({"status": "ok", "message": "Cadastro realizado com sucesso"})
    except Exception as e:
        logger.error("Erro ao criar usuário: %s", e)
        return JsonResponse({"error": "Erro ao criar usuário", "details": str(e)})

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
        auth_login(request, user)  # cria a sessão e gera cookie 'sessionid'
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



@require_GET
def listar_usuarios(request):
    usuarios = User.objects.all().values("id", "username", "email", "date_joined")
    return JsonResponse(list(usuarios), safe=False)



@require_GET
def usuario_por_id(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    return JsonResponse({
        "id": usuario.id,
        "username": usuario.username,
        "email": usuario.email,
        "date_joined": usuario.date_joined,
    })

@require_GET
def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Not authenticated"}, status=401)
    u = request.user
    return JsonResponse({
        "id": u.id,
        "username": u.username,
        "email": u.email,
    })