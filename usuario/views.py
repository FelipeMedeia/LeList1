from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_imp, logout
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


@login_required
def logout(request):
    return redirect(request, '/')


@login_required(login_url='/login/')
def duvidas(request):
    return render(request, 'duvida.html')


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


@login_required(login_url='../login/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='../login/')
def produto(request):
    if request.method == "GET":
        produto_id = request.GET.get('id')
        if produto_id:
            produto = Produtos.objects.get(id=produto_id)
            if produto.user == request.user:
                return render(request, 'produto.html', {'produto': produto})
        return render(request, 'produto.html')
    else:
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        quantidade = request.POST.get('quantidade')
        data_validade = request.POST.get('data_validade')
        foto = request.FILES.get('file')
        produto_id = request.POST.get('produto-id')
        user = request.user
        if produto_id:
            produto = Produtos.objects.get(id=produto_id)
            if user == produto.user:
                produto.nome = nome
                produto.tipo = tipo
                produto.quantidade = quantidade
                produto.data_validade = data_validade
                if foto:
                    produto.foto = foto
                produto.save()

        else:
            produto = Produtos.objects.filter(nome=nome, user=user, data_validade=data_validade).first()
            if produto:
                return HttpResponse('Já existe um produto com esse nome')
            produto = Produtos.objects.create(nome=nome, tipo=tipo, quantidade=quantidade,
                                              data_validade=data_validade, foto=foto, user=user)
            produto.save()

        return render(request, 'produto.html')


@login_required(login_url='../login/')
def listar_produtos(request):
    produto = Produtos.objects.filter(user=request.user, active=True)
    return render(request, 'lista.html', {'produto': produto})


@login_required(login_url='../login/')
def produto_detalhe(request, id):
    produto = Produtos.objects.get(active=True, id=id)
    return render(request, 'dados_produto.html', {'produto': produto})


@login_required(login_url='../login/')
def excluir_produto(request, id):
    produto = Produtos.objects.get(id=id)
    produto.delete()
    return redirect('/home/')


def index(request):
    return render(request, 'index.html')
