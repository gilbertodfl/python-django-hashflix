from ast import List
from django.shortcuts import render
from .models import Filme
from django.views.generic import DetailView, TemplateView, ListView


## cbv é uma classe que herda de TemplateView, e tem um método get_context_data 
# que é responsável por passar os dados para o template.
class Homepage(TemplateView):
    template_name = "homepage.html"
    
class Homefilmes(ListView):
    template_name = "homefilmes.html"
    model = Filme
    ## object_list é o nome da variável que vai ser passada para o template, e que vai conter a lista de filmes.

class Detalhesfilme(DetailView):
    template_name = "detalhesfilme.html"    
    model = Filme
    ## Diferente da ListView, aqui estamos passando um objeto específico, e não uma lista de objetos. 
    # O nome da variável que vai ser passada para o template é filme, e não object_list.

##FBS - Function Based Views. 
## o exemplo abaixo é uma função que recebe a requisição do usuário, processa os dados e retorna uma resposta.

#def homepage(request):
#    return render(request, "homepage.html")

# def homefilmes(request):
#     context = {}
#     lista_todos_filmes = Filme.objects.all()
#     context ['lista_filmes'] = lista_todos_filmes
#     return render(request, "homefilmes.html", context)

