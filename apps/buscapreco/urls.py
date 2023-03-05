from django.urls import path
from . import views


urlpatterns = [
    path('', views.pesquisar, name='pesquisar'),
    path('resultados/', views.exibir_resultados, name='resultados')
]