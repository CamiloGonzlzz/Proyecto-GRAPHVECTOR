from django.urls import path
from . import views

urlpatterns = [
    path('R2', views.graficar_vectorR2, name='vectorR2'),
    path('graficar_vector/', views.grafico_vector, name='graficar_vector'),
    path('pruebaR2/', views.PruebaR2, name='Prueba_R2.html'),
]