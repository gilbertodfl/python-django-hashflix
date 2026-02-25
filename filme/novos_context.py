from .models import Filme

def lista_filmes_recentes(request):
    # Aqui estamos buscando os filmes mais recentes, ordenando por data de criação e pegando os 5 primeiros.
    lista_filmes  = Filme.objects.all().order_by('-data_criacao')[0:5]
    filme_destaque = lista_filmes.first()  # Pegando o primeiro filme da lista para destacar
    return {'lista_filmes_recentes': lista_filmes, 'filme_destaque': filme_destaque}

def lista_filmes_emalta(request):
    # Aqui estamos buscando os filmes mais recentes, ordenando por data de criação e pegando os 5 primeiros.
    lista_filmes_emalta  = Filme.objects.all().order_by('-visualizacoes')[0:10]
    return {'lista_filmes_emalta': lista_filmes_emalta}

def filme_destaque(request):
    # Aqui estamos buscando o filme mais recente para destacar.
    filme_destaque = Filme.objects.all().order_by('-data_criacao').first()
    return {'filme_destaque': filme_destaque}