from django.test import TestCase
from django.urls import reverse
from .models import Produtos
from django.contrib.auth.models import User
from .views import *

class ViewsTest(TestCase):
    def setUp(self):
        # Criar um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_cadastro_view(self):
        # Simular uma solicitação POST para a view de cadastro
        response = self.client.post(reverse('cadastro'), {'nome': 'testuser', 'email': 'testemail', 'senha': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após o cadastro

    # Verifique se o usuário foi criado
        user = User.objects.filter(username='testuser').first()
        self.assertIsNotNone(user)



    def test_login_view(self):
        # Simular uma solicitação GET para a view de login
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Simular uma solicitação POST para a view de login
        response = self.client.post(reverse('login'), {'nome': 'testuser', 'senha': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após o login

    def test_home_view(self):
        # Logar o usuário
        self.client.login(username='testuser', password='testpassword')

        # Simular uma solicitação GET para a view home
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_produto_view(self):
        # Logar o usuário
        self.client.login(username='testuser', password='testpassword')

        # Simular uma solicitação GET para a view de produto
        response = self.client.get(reverse('produto'))
        self.assertEqual(response.status_code, 200)

        # Simular uma solicitação POST para a view de produto
        response = self.client.post(reverse('produto'), {'nome': 'produto_teste', 'tipo': 'tipo_teste', 'quantidade': 10, 'data_validade': '2023-11-01', 'produto-id': ''})
        self.assertEqual(response.status_code, 200)

        # Verificar se o produto foi criado
        produto = Produtos.objects.filter(nome='produto_teste').first()
        self.assertIsNotNone(produto)

    def test_produto_detalhe_view(self):
        # Logar o usuário
        self.client.login(username='testuser', password='testpassword')

        # Criar um produto de teste com uma imagem associada
        produto = Produtos.objects.create(
            nome='produto_teste', tipo='tipo_teste', quantidade=10, data_validade='2023-11-01', user=self.user
        )
        # Adicione uma imagem (substitua 'imagem_teste.jpg' pelo caminho da imagem real)
        produto.foto = 'caminho/para/imagem_teste.jpg'
        produto.save()

        # Simular uma solicitação GET para a view de detalhe do produto
        response = self.client.get(reverse('produto_detalhe', args=[produto.id]))
        self.assertEqual(response.status_code, 200)


    def test_excluir_produto_view(self):
        # Logar o usuário
        self.client.login(username='testuser', password='testpassword')

        # Criar um produto de teste
        produto = Produtos.objects.create(nome='produto_teste', tipo='tipo_teste', quantidade=10, data_validade='2023-11-01', user=self.user)

        # Simular uma solicitação POST para a view de excluir produto
        response = self.client.post(reverse('excluir', args=[produto.id]))
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento após a exclusão

        # Verificar se o produto foi excluído
        produto_exists = Produtos.objects.filter(id=produto.id).exists()
        self.assertFalse(produto_exists)

    def test_gerar_pdf_view(self):
        # Logar o usuário
        self.client.login(username='testuser', password='testpassword')

        # Simular uma solicitação GET para a view de geração de PDF
        response = self.client.get(reverse('relatorio'))
        self.assertEqual(response.status_code, 200)
