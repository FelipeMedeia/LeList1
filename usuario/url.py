from django.http import request
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('produto/', views.produto, name='produto'),
    path('lista/', views.listar_produtos, name='lista'),
    path('detalhes/<id>/', views.produto_detalhe),
    path('detalhes/excluir/<id>/', views.excluir_produto, name='excluir'),
    path('home/duvidas/', views.duvidas, name='duvida')
]

