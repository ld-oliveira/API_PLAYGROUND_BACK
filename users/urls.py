from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_user, name='logout'),
    path("usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("usuarios/<int:user_id>/", views.usuario_por_id, name="usuario_por_id"),    
]
