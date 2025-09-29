from django.urls import path
from users.views import cadastro, login_user, logout_user, listar_usuarios, usuario_por_id, csrf_token

urlpatterns = [
    path("users/csrf/", csrf_token, name="csrf"),
    path("users/cadastro/", cadastro, name="cadastro"),
    path("users/login/", login_user, name="login"),
    path("users/logout/", logout_user, name="logout"),
    path("users/", listar_usuarios, name="listar_usuarios"),
    path("users/<int:user_id>/", usuario_por_id, name="usuario_por_id"),
]