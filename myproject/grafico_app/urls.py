from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Vista para la página de inicio
    path('R2', views.graficar_vectorR2, name='vectorR2'),
    path('graficar_vector/', views.grafico_vector, name='graficar_vector'),
    path('pruebaR2/', views.PruebaR2, name='Prueba_R2.html'),
    path('suma_vectoresR2/', views.suma_vectoresR2, name='suma_vectoresR2'),
    path('resta_vectoresR2/', views.resta_vectoresR2, name='resta_vectoresR2'),
    path('multiplicacion_vectoresR2/', views.multiplicacion_vectoresR2, name='multiplicacion_vectoresR2')
]