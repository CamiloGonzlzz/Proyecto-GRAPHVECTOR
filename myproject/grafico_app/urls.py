from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Vista para la página de inicio
    path('R2', views.graficar_vectorR2, name='vectorR2'),
    path('graficar_vector/', views.grafico_vector, name='graficar_vector'),
    path('PruebaR2_Menu/', views.PruebaR2_Menu, name='pruebaR2_Menu'),
    path('prueba_facilR2/', views.Prueba_FacilR2, name='prueba_facilR2'),
    path('prueba-media/', views.prueba_operaciones, name='prueba_operaciones'),
    path('prueba-dificil/', views.prueba_magnitud_angulo, name='prueba_magnitud_angulo'),
    path('suma_vectoresR2/', views.suma_vectoresR2, name='suma_vectoresR2'),
    path('resta_vectoresR2/', views.resta_vectoresR2, name='resta_vectoresR2'),
    path('multiplicacion_vectoresR2/', views.multiplicacion_vectoresR2, name='multiplicacion_vectoresR2'),
    path('menu/', views.menu, name='menu'),
    path('suma_vectoresR3/', views.suma_vectoresR3, name='suma_vectoresR3'),
    path('resta_vectoresR3/', views.resta_vectoresR3, name='resta_vectoresR3'),
    path('multiplicacion_vectoresR3/', views.multiplicacion_vectoresR3, name='multiplicacion_vectoresR3'),
    path('regresion/', views.graficar_regresion_lineal, name='regresion_lineal'),
    path('proyectil/', views.grafico_proyectil, name='grafico_proyectil'),
    path('area-bajo-curva/', views.area_bajo_curva, name='area_bajo_curva'),
    path('movimiento-proyectil/', views.Movimiento_Proyectil, name='movimiento_proyectil'),
]