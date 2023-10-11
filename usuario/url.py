from django.http import request
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('home/filter/', views.home_filter, name='filter'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('produto/', views.produto, name='produto'),
    path('relatorio/', views.some_view, name='relatorio'),
    path('detalhes/<id>/', views.produto_detalhe),
    path('detalhes/excluir/<id>/', views.excluir_produto, name='excluir'),
    path('home/duvidas/', views.duvidas, name='duvida')
]

