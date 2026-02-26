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

    # quem é *args e **kwargs?
    # *args é uma tupla que contém os argumentos posicionais passados para a função, 
    # e **kwargs é um dicionário que contém os argumentos nomeados passados para a função.

    def get(self, request, *args, **kwargs):
        # Aqui estamos pegando o objeto filme que foi passado para o template, e incrementando o número de visualizações em 1.
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        ## redireciona o usuário para url final
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Aqui podemos adicionar mais dados ao contexto, além do objeto filme que já está sendo 
        # passado automaticamente pelo DetailView.
        context = super( Detalhesfilme, self).get_context_data(**kwargs)
        # Aqui estou passando filmes_relacionados que tem todos os filmes vinculados.
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria)[0:5] 
        context['filmes_relacionados'] = filmes_relacionados
        return context

class Pesquisafilme(ListView):
    template_name = "pesquisafilme.html"
    model = Filme

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:

            return self.model.objects.filter(titulo__icontains=query)
            ## o abaixo é apenas ilustrativo, o acima é melhor. 
            ## return Filme.objects.filter(titulo__icontains=query)
        else:
            return Filme.objects.none()

##FBS - Function Based Views. 
## o exemplo abaixo é uma função que recebe a requisição do usuário, processa os dados e retorna uma resposta.

#def homepage(request):
#    return render(request, "homepage.html")

# def homefilmes(request):
#     context = {}
#     lista_todos_filmes = Filme.objects.all()
#     context ['lista_filmes'] = lista_todos_filmes
#     return render(request, "homefilmes.html", context)

