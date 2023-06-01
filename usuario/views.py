from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_imp
from .models import Produtos
from django.contrib.auth.decorators import login_required


# Create your views here.


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=nome).first()

        if user:
            return HttpResponse('Já existe um usuário com esse nome')

        user = User.objects.create_user(username=nome, first_name=nome, email=email, password=senha)
        user.save()

        return HttpResponse('Usuário cadastrado com sucesso')


def logout(request):
    return redirect(request, 'index.html')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = authenticate(username=nome, password=senha)
        if user:
            login_imp(request, user)
            return render(request, 'home.html')
        else:
            messages.error(request, 'Usuário ou senha inválido! '
                                    'Por favor, tente novamente.')
    return redirect('login')


def home(request):
    return render(request, 'home.html')


def produto(request):
    if request.method == "GET":
        return render(request, 'produto.html')
    else:
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        quantidade = request.POST.get('quantidade')
        data_validade = request.POST.get('data_validade')
        foto = request.FILES.get('foto')
        user = request.user

        produto = Produtos.objects.filter(nome=nome, user=user, data_validade=data_validade).first()

        if produto:
            return HttpResponse('Já existe um produto com esse nome')

        produto = Produtos.objects.create(nome=nome, tipo=tipo, quantidade=quantidade,
                                          data_validade=data_validade, foto=foto, user=user)
        produto.save()

        return render(request, 'produto.html')


@login_required(login_url='login/')
def listar_produtos(request):
    produto = Produtos.objects.filter(user=request.user, active=True)
    return render(request, 'lista.html', {'produto': produto})


def index(request):
    return render(request, 'index.html')
