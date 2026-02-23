## url - view - template
from django.urls import path, include
from .views import  Homepage, Homefilmes, Detalhesfilme

### modelo FBS
# urlpatterns = [
#     path('', homepage),
#     path('filmes/', homefilmes),
# ]

app_name='filme'
## modelo CBV  

# path('', Homepage.as_view(), name='homepage')
#       ^        ^                   ^
#    caminho   view              nome da URL
urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('filmes/', Homefilmes.as_view(), name='homefilmes'),
    path('filmes/<int:pk>/', Detalhesfilme.as_view(), name='detalhesfilme'),
]
