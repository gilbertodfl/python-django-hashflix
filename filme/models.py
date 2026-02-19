from django.db import models
from django.utils import timezone
LISTA_CATEGORIAS = [
    ("acao", "Ação"),
    ("comedia", "Comédia"),
    ("drama", "Drama"),
    ("terror", "Terror"),
    ("ficcao", "Ficção Científica"),
    ("animacao", "Animação"),
    ("aventura", "Aventura"),
    ("romance", "Romance"),
    ("documentario", "Documentário"),
]

# Create your models here.
class Filme(models.Model):
    titulo = models.CharField(max_length=255)
    thumb = models.ImageField(upload_to='thumbs_filmes/')
    descricao = models.TextField(max_length=1000)
    categoria= models.CharField(max_length=20, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
#    data_criacao = models.DateTimeField(auto_now_add=True)
    data_criacao = models.DateTimeField(default=timezone.now)


    def __str__(self):
        ##return self.titulo,  self.categoria, self.visualizacoes, self.data_criacao    
        return self.titulo           