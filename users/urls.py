from django.urls import path
from users.views import get_csrf,cadastro,login_user,logout_user,listar_usuarios,usuario_por_id

urlpatterns = [
    path("csrf/", get_csrf, name="csrf"),
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("", listar_usuarios, name="listar_usuarios"),
    path("<int:user_id>/", usuario_por_id, name="usuario_por_id"),
]