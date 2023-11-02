from PIL import Image
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_imp
from .models import Produtos
from django.contrib.auth.decorators import login_required
from usuario.filters import ProdutoFilter
from reportlab.pdfgen import canvas
from PIL import Image
import os

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
            messages.error(request, 'Já existe um usuário com esse nome')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, first_name=nome, email=email, password=senha)
        user.save()

        context = {'cadastro_sucesso': True}
        return render(request, 'cadastro.html', context)


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
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválido! '
                                    'Por favor, tente novamente.')
    return redirect('login')


@login_required(login_url='../login/')
def home(request):
    categoria_filter = ProdutoFilter(request.GET, queryset=Produtos.objects.filter(user=request.user, active=True))

    context = {
        'form': categoria_filter.form,
        'produto': categoria_filter.qs
    }
    return render(request, 'home.html', context)


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
                # Verifique se uma nova imagem foi enviada
                if foto:
                    # Exclua a imagem anterior se existir
                    if produto.foto:
                        # Use o caminho do arquivo anterior para excluí-lo
                        if default_storage.exists(produto.foto.name):
                            default_storage.delete(produto.foto.name)

                    # Salve a nova imagem no local de upload
                    produto.foto.save(foto.name, ContentFile(foto.read()))
                produto.nome = nome
                produto.tipo = tipo
                produto.quantidade = quantidade
                produto.data_validade = data_validade
                produto.save()
        else:
            produto = Produtos.objects.filter(nome=nome, user=user, data_validade=data_validade).first()
            if produto:
                messages.error(request, 'Já existe um produto com esses dados')

            else:
                produto = Produtos.objects.create(nome=nome, tipo=tipo, quantidade=quantidade,
                                                  data_validade=data_validade, foto=foto, user=user)
                produto.save()

        return render(request, 'produto.html')


@login_required(login_url='../login/')
def produto_detalhe(request, id):
    produto = Produtos.objects.get(active=True, id=id)
    return render(request, 'dados_produto.html', {'produto': produto})


@login_required(login_url='../login/')
def excluir_produto(request, id):
    user = request.user
    if id:
        produto = Produtos.objects.get(id=id)
        if user == produto.user:
            # Verifique se uma nova imagem foi enviada
            default_storage.delete(produto.foto.name)
        produto.save()
    produto = Produtos.objects.get(id=id)
    produto.delete()
    return redirect('/home/')


def index(request):
    return render(request, 'index.html')


@login_required(login_url='../login/')
def gerar_pdf(request):
    queryset = Produtos.objects.filter(user=request.user, active=True)
    produto_filter = ProdutoFilter(request.GET, queryset=queryset)
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="lista_de_produtos.pdf"'

    # Create the PDF object, using the buffer as its "file."
    pdf = canvas.Canvas(response)

    y = 750

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(250, y, "Lista de Produtos")
    pdf.setFont("Helvetica", 12)
    y -= 30

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    for produto in produto_filter.qs:
        imagem = Image.open(produto.foto.path)
        width, height = imagem.size
        aspect_ratio = height / width
        new_width = 100
        new_height = int(new_width * aspect_ratio)

        pdf.drawImage(produto.foto.path, 100, y - 50, width=new_width, height=new_height)
        pdf.drawString(100, y - 60, f'Nome: {produto.nome}')
        pdf.drawString(100, y - 70, f'Categoria: {produto.tipo}')

        # Adicione mais campos do produto conforme necessário
        y -= new_height + 60
        if y < 50:
            y += 720
            pdf.showPage()

    pdf.save()
    return response
