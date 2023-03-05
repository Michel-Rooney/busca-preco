from django.shortcuts import render
from apps.buscapreco.models import Produto


def pesquisar(request):
    return render(request, 'pages/produtos.html')

def exibir_resultados(request):
    nome_produto = request.POST.get('produto')
    dados = {
        'dados': Produto.objects.filter(nome__icontains=nome_produto).order_by('preco')
    }
    return render(request, 'pages/resultado_pesquisa.html', dados)