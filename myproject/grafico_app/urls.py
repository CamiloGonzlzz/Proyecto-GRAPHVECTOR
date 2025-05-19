from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Vista para la página de inicio
    path('R2', views.graficar_vectorR2, name='vectorR2'),
    path('graficar_vector/', views.grafico_vector, name='graficar_vector'),
    path('pruebaR2/', views.PruebaR2, name='Prueba_R2'),
    path('pruebamagnitudangulo/', views.prueba_magnitud_angulo, name='pruebamagnitudangulo'),
    path('pruebaoperacionesVectores/', views.prueba_operaciones, name='pruebaoperacionesVectores'),
    path('suma_vectoresR2/', views.suma_vectoresR2, name='suma_vectoresR2'),
    path('resta_vectoresR2/', views.resta_vectoresR2, name='resta_vectoresR2'),
    path('multiplicacion_vectoresR2/', views.multiplicacion_vectoresR2, name='multiplicacion_vectoresR2'),
    path('menu/', views.menu, name='menu'),
    path('suma_vectoresR3/', views.suma_vectoresR3, name='suma_vectoresR3'),
    path('resta_vectoresR3/', views.resta_vectoresR3, name='resta_vectoresR3'),
    path('multiplicacion_vectoresR3/', views.multiplicacion_vectoresR3, name='multiplicacion_vectoresR3'),
]