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
    path('relatorio/', views.gerar_pdf, name='relatorio'),
    path('detalhes/<int:id>/', views.produto_detalhe, name='produto_detalhe'),
    path('detalhes/excluir/<int:id>/', views.excluir_produto, name='excluir'),
    path('home/duvidas/', views.duvidas, name='duvida')
]
