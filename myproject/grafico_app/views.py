from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from .forms import VectorForm
import json
import random

def graficar_vectorR2(request):
    if request.method == 'POST':
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))

        plt.figure()

        # Dibujar el vector
        plt.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color='black', label=f'Vector ({x}, {y})')

        # Dibujar las líneas extrapolares
        plt.plot([0, x], [y, y], linestyle='--', color='blue', label='Línea Extrapolar Y')  # Línea horizontal
        plt.plot([x, x], [0, y], linestyle='--', color='red', label='Línea Extrapolar X')  # Línea vertical

        # Configuraciones de la gráfica
        max_range = max(abs(x), abs(y)) + 1
        plt.xlim(-max_range, max_range)
        plt.ylim(-max_range, max_range)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend()

        # Guardar la imagen en memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer64 = base64.b64encode(imagen_png)
        imagen = buffer64.decode('utf-8')
        plt.close()

        return render(request, 'grafico_app/grafico.html', {'imagen': imagen})

    return render(request, 'grafico_app/grafico.html')

def grafico_vector(request):
    if request.method == 'POST':
        x = request.POST.get('x')
        y = request.POST.get('y')
        z = request.POST.get('z')
        # Aquí puedes hacer lo que quieras con x, y, z
        # Por ejemplo, pasarlos al contexto para graficar
        return render(request, 'grafico_app/grafico_vector.html', {'x': x, 'y': y, 'z': z})
    return render(request, 'grafico_app/form_vectorR3.html')

def PruebaR2(request):
    estado = request.session.get('estado', 'inicio')
    imagen = None
    x_val = ''
    y_val = ''
    mensaje = ''

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'iniciar':
            request.session['correctas'] = 0
            request.session['incorrectas'] = 0
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            request.session['x_vector'] = x
            request.session['y_vector'] = y
            estado = 'pregunta'

        elif accion == 'responder':
            x_correcto = request.session.get('x_vector')
            y_correcto = request.session.get('y_vector')
            x_val = request.POST.get('x_val', '')
            y_val = request.POST.get('y_val', '')

            try:
                x_usuario = int(x_val)
                y_usuario = int(y_val)
                if x_usuario == x_correcto and y_usuario == y_correcto:
                    request.session['correctas'] += 1
                    mensaje = "¡Respuesta correcta!"
                else:
                    request.session['incorrectas'] += 1
                    mensaje = f"Incorrecto. El vector era ({x_correcto}, {y_correcto})"
            except ValueError:
                request.session['incorrectas'] += 1
                mensaje = "Debes ingresar valores numéricos."

            # Verifica si se llegó a 10 respuestas
            total = request.session['correctas'] + request.session['incorrectas']
            if total >= 10:
                estado = 'finalizado'
            else:
                estado = 'respuesta'

        elif accion == 'siguiente':
            # Verifica si se llegó a 10 respuestas antes de generar nueva pregunta
            total = request.session['correctas'] + request.session['incorrectas']
            if total >= 10:
                estado = 'finalizado'
            else:
                x = random.randint(1, 10)
                y = random.randint(1, 10)
                request.session['x_vector'] = x
                request.session['y_vector'] = y
                estado = 'pregunta'
                x_val = ''
                y_val = ''

        request.session['estado'] = estado

    else:
        estado = 'inicio'
        request.session['estado'] = estado

    # Si hay que mostrar la gráfica
    if estado in ['pregunta', 'respuesta']:
        x = request.session.get('x_vector')
        y = request.session.get('y_vector')
        plt.figure()
        plt.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color='black')
        plt.plot([0, x], [y, y], linestyle='--', color='blue')
        plt.plot([x, x], [0, y], linestyle='--', color='red')
        max_range = max(abs(x), abs(y)) + 1
        plt.xlim(-max_range, max_range)
        plt.ylim(-max_range, max_range)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        # plt.legend()  # Ya no mostramos la leyenda
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer64 = base64.b64encode(imagen_png)
        imagen = buffer64.decode('utf-8')
        plt.close()

    context = {
        'imagen': imagen,
        'x_val': x_val,
        'y_val': y_val,
        'correctas': request.session.get('correctas', 0),
        'incorrectas': request.session.get('incorrectas', 0),
        'mensaje': mensaje,
        'estado': estado,
    }
    return render(request, 'grafico_app/Prueba_R2.html', context)

