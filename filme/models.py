from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
LISTA_CATEGORIAS = (
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros"),
)

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

class Episodio(models.Model):
    # Um episódio pertence a um filme, e um filme pode ter vários episódios. 
    # Por isso, usamos uma ForeignKey para relacionar o episódio com o filme.
    # No caso de aulas, por exemplo, curso de python e ai vários episódios, cada episódio pertence a um curso.

    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='episodios')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)
    video = models.URLField()
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.filme.titulo} - {self.titulo}"

class Usuario(AbstractUser):
    # Herda de AbstractUser, que já tem os campos básicos de um usuário, como username, email, password, etc.
    # Aqui podemos adicionar campos adicionais, como por exemplo, data de nascimento, ou foto de perfil.
    #filmes_vistos = models.ManyToManyField(Filme, related_name='usuarios_vistos', blank=True)
    filmes_vistos = models.ManyToManyField('Filme')