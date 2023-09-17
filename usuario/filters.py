import django_filters
from usuario.models import Produtos


class ProdutoFilter(django_filters.FilterSet):
    
    tipo = django_filters.CharFilter(lookup_expr='icontains', label='Nome')
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Categoria')

    class Meta:
        model = Produtos
        fields = ['nome', 'tipo']