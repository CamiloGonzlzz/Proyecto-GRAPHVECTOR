from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64

def home(request):  # primera vista

    doc_externo = open("C:/Users/LENOVO/Documents/ProyectoDjango/myproject/myproject/Plantillas/Home.html")
    plt = Template(doc_externo.read())
    doc_externo.close()
    ctx = Context()
    documento = plt.render(ctx)

    return HttpResponse(documento)

