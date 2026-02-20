## url - view - template
from django.urls import path, include
from .views import  Homepage, Homefilmes

### modelo FBS
# urlpatterns = [
#     path('', homepage),
#     path('filmes/', homefilmes),
# ]

## modelo CBV  
urlpatterns = [
    path('', Homepage.as_view()),
    path('filmes/', Homefilmes.as_view()),
]
