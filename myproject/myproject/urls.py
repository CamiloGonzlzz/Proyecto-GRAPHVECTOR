from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views


def inicio(request):
    return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('home/', views.home),

    path('vectores/', include('grafico_app.urls')),
    path('grafico/', include('grafico_app.urls')),

    # Inicio del proyecto → redirige al login
    path('', inicio),
]