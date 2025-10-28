from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import io
import urllib, base64
from .forms import VectorForm
import json
import random
import numpy as np
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D  # para gráfico 3D
import math
from django.urls import reverse
import plotly.graph_objects as go

def inicio(request):
    return render(request, 'grafico_app/Inicio.html')  # Asegúrate de tener este template

def menu(request):
    return render(request, "grafico_app/menu.html")

from django.shortcuts import render

def grafica_r2(request):
    return render(request, 'grafico_app/vectorR2.html')

def sumaR2(request):
    return render(request, 'grafico_app/suma_vectoresR2.html')

def restaR2(request):
    return render(request, 'grafico_app/resta_vectoresR2.html')

def multiplicacionR2(request):
    return render(request, 'grafico_app/multiplicacion_vectoresR2.html')

def PruebaR2_Menu(request):
    return render(request, 'grafico_app/Prueba_R2.html')

def Movimiento_Proyectil(request):
    return render(request, 'grafico_app/MovimientoProyectil.html')

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
    return render(request, 'grafico_app/grafico_vector.html')

def Prueba_FacilR2(request):
    # Inicializar contadores
    correctas = request.session.get('correctas', 0)
    incorrectas = request.session.get('incorrectas', 0)

    if request.method == 'POST':
        # Recuperar el vector correcto de la sesión
        x_real = request.session.get('x_real')
        y_real = request.session.get('y_real')
        x_val = int(request.POST.get('x_val'))
        y_val = int(request.POST.get('y_val'))

        # Verificar respuesta
        correcto = (x_val == x_real) and (y_val == y_real)
        if correcto:
            correctas += 1
            mensaje = f'✅ ¡Correcto! El vector es ({x_real}, {y_real})'
        else:
            incorrectas += 1
            mensaje = f'❌ Incorrecto. El vector correcto era ({x_real}, {y_real})'

        request.session['correctas'] = correctas
        request.session['incorrectas'] = incorrectas

        # Graficar ambos vectores
        fig, ax = plt.subplots()
        ax.quiver(0, 0, x_real, y_real, angles='xy', scale_units='xy', scale=1, color='r', label='Correcto')
        ax.quiver(0, 0, x_val, y_val, angles='xy', scale_units='xy', scale=1, color='b', linestyle='--', label='Tu respuesta')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.grid()
        ax.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        imagen = base64.b64encode(buf.getvalue()).decode('utf-8')

        return render(request, 'grafico_app/prueba_facilR2.html', {
            'imagen': imagen,
            'mensaje': mensaje,
            'estado': 'respuesta',
            'correctas': correctas,
            'incorrectas': incorrectas
        })

    # GET: Generar nueva pregunta y gráfica
    x_real = np.random.randint(-8, 8)
    y_real = np.random.randint(-8, 8)
    request.session['x_real'] = x_real
    request.session['y_real'] = y_real

    fig, ax = plt.subplots()
    ax.quiver(0, 0, x_real, y_real, angles='xy', scale_units='xy', scale=1, color='r')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.grid()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    imagen = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'grafico_app/prueba_facilR2.html', {
        'imagen': imagen,
        'estado': 'pregunta',
        'correctas': correctas,
        'incorrectas': incorrectas
    })
    

def prueba_operaciones(request):
    # Inicializar estado y variables
    estado = request.session.get('estado', 'inicio')
    operacion_actual = request.session.get('operacion_actual', 'suma')
    imagen = None
    mensaje = ''
    opciones = []
    
    # Función para generar imágenes de vectores
    def generar_imagen(v1, v2=None, resultado=None, operacion='suma'):
        plt.figure(figsize=(8, 6))
        
        # Dibujar primer vector
        plt.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, 
                  color='#1f77b4', width=0.015, label=f'Vector A ({v1[0]}, {v1[1]})')
        
        # Dibujar segundo vector si existe
        if v2:
            plt.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1,
                      color='#2ca02c', width=0.015, label=f'Vector B ({v2[0]}, {v2[1]})')
            
            # Dibujar resultado si existe
            if resultado and operacion != 'multiplicacion':
                plt.quiver(0, 0, resultado[0], resultado[1], angles='xy', scale_units='xy', scale=1,
                          color='#d62728', width=0.015, label=f'Resultado ({resultado[0]}, {resultado[1]})')
        
        # Configurar ejes
        max_val = max(
            max(abs(v1[0]), abs(v1[1])),
            max(abs(v2[0]), abs(v2[1])) if v2 else 0,
            max(abs(resultado[0]), abs(resultado[1])) if resultado and operacion != 'multiplicacion' else 0
        ) + 2
        
        plt.xlim(-max_val, max_val)
        plt.ylim(-max_val, max_val)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend()
        plt.title(f"Operación: {operacion.capitalize()}")
        
        # Convertir a imagen base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'iniciar':
            # Inicializar prueba
            request.session.update({
                'correctas': 0,
                'incorrectas': 0,
                'operacion_actual': 'suma',
                'estado': 'pregunta',
                'vector1': [random.randint(-10, 10), random.randint(-10, 10)],
                'vector2': [random.randint(-10, 10), random.randint(-10, 10)],
                'respuesta_correcta': None
            })
            return redirect(reverse('prueba_operaciones'))
        
        elif accion == 'responder':
            # Verificar respuesta
            respuesta_usuario = request.POST.get('respuesta', '')
            respuesta_correcta = request.session.get('respuesta_correcta', '')
            
            if respuesta_usuario == respuesta_correcta:
                request.session['correctas'] += 1
                mensaje = "¡Respuesta correcta!"
            else:
                request.session['incorrectas'] += 1
                mensaje = f"Incorrecto. La respuesta correcta era {respuesta_correcta}"
            
            estado = 'respuesta'
            request.session['estado'] = estado
        
        elif accion == 'siguiente':
            total = request.session.get('correctas', 0) + request.session.get('incorrectas', 0)
            
            if total >= 10:
                estado = 'finalizado'
            else:
                estado = 'pregunta'
                # Rotar operaciones
                operaciones = ['suma', 'resta', 'multiplicacion']
                current_idx = operaciones.index(request.session.get('operacion_actual', 'suma'))
                next_op = operaciones[(current_idx + 1) % len(operaciones)]
                
                request.session.update({
                    'operacion_actual': next_op,
                    'vector1': [random.randint(-10, 10), random.randint(-10, 10)],
                    'vector2': [random.randint(-10, 10), random.randint(-10, 10)],
                    'respuesta_correcta': None
                })
            
            request.session['estado'] = estado
    
    # Generar pregunta y opciones
    if estado == 'pregunta':
        operacion_actual = request.session.get('operacion_actual', 'suma')
        v1 = request.session.get('vector1', [0, 0])
        v2 = request.session.get('vector2', [0, 0])
        
        # Calcular resultado según operación
        if operacion_actual == 'suma':
            resultado = [v1[0] + v2[0], v1[1] + v2[1]]
            respuesta_correcta = f"{resultado[0]},{resultado[1]}"
        elif operacion_actual == 'resta':
            resultado = [v1[0] - v2[0], v1[1] - v2[1]]
            respuesta_correcta = f"{resultado[0]},{resultado[1]}"
        elif operacion_actual == 'multiplicacion':
            # Producto escalar
            resultado = v1[0] * v2[0] + v1[1] * v2[1]
            respuesta_correcta = str(resultado)
        
        request.session['respuesta_correcta'] = respuesta_correcta
        
        # Generar opciones múltiples (1 correcta + 3 incorrectas)
        opciones = [respuesta_correcta]
        
        for _ in range(3):
            if operacion_actual == 'multiplicacion':
                # Variaciones para producto escalar
                variacion = random.choice([-5, -3, -2, 2, 3, 5])
                opcion = resultado + variacion
            else:
                # Variaciones para suma/resta
                variacion_x = random.choice([-3, -2, -1, 1, 2, 3])
                variacion_y = random.choice([-3, -2, -1, 1, 2, 3])
                opcion = f"{resultado[0] + variacion_x},{resultado[1] + variacion_y}"
            opciones.append(str(opcion))
        
        random.shuffle(opciones)
        
        # Generar imagen de los vectores
        imagen = generar_imagen(v1, v2, resultado if operacion_actual != 'multiplicacion' else None, operacion_actual)
    
    elif estado == 'respuesta':
        operacion_actual = request.session.get('operacion_actual', 'suma')
        v1 = request.session.get('vector1', [0, 0])
        v2 = request.session.get('vector2', [0, 0])
        respuesta_correcta = request.session.get('respuesta_correcta', '0,0')
        
        # Recuperar resultado para la imagen
        if operacion_actual == 'multiplicacion':
            resultado = None
        else:
            resultado = list(map(int, respuesta_correcta.split(',')))
        
        imagen = generar_imagen(v1, v2, resultado, operacion_actual)
    
    context = {
        'estado': estado,
        'operacion': operacion_actual.capitalize(),
        'imagen': imagen,
        'opciones': opciones,
        'mensaje': mensaje,
        'correctas': request.session.get('correctas', 0),
        'incorrectas': request.session.get('incorrectas', 0),
        'vector1': request.session.get('vector1', [0, 0]),
        'vector2': request.session.get('vector2', [0, 0]),
    }
    
    return render(request, 'grafico_app/prueba_operaciones.html', context)

def prueba_magnitud_angulo(request):
    estado = request.session.get('estado', 'inicio')
    imagen = None
    mensaje = ''
    opciones = []

    def calcular_magnitud(x, y):
        return round(math.sqrt(x**2 + y**2), 2)

    def calcular_angulo(x, y):
        return round(math.degrees(math.atan2(y, x)), 2)

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'iniciar':
            request.session.update({
                'correctas': 0,
                'incorrectas': 0,
                'vector_x': random.randint(-10, 10),
                'vector_y': random.randint(-10, 10),
                'estado': 'pregunta'
            })
            return redirect('prueba_magnitud_angulo')

        elif accion == 'responder':
            x = request.session.get('vector_x')
            y = request.session.get('vector_y')
            respuesta = request.POST.get('respuesta', '')
            
            # Respuesta correcta en formato "magnitud,angulo"
            magnitud_correcta = calcular_magnitud(x, y)
            angulo_correcto = calcular_angulo(x, y)
            respuesta_correcta = f"{magnitud_correcta},{angulo_correcto}"
            
            if respuesta == respuesta_correcta:
                request.session['correctas'] += 1
                mensaje = "¡Respuesta correcta!"
            else:
                request.session['incorrectas'] += 1
                mensaje = f"Incorrecto. La respuesta correcta era {respuesta_correcta}"
            
            estado = 'respuesta'
            request.session['estado'] = estado

        elif accion == 'siguiente':
            total = request.session.get('correctas', 0) + request.session.get('incorrectas', 0)
            if total >= 10:
                estado = 'finalizado'
            else:
                estado = 'pregunta'
                request.session.update({
                    'vector_x': random.randint(-10, 10),
                    'vector_y': random.randint(-10, 10)
                })
            request.session['estado'] = estado

    # Generar opciones para pregunta múltiple
    if estado == 'pregunta':
        x = request.session.get('vector_x', 0)
        y = request.session.get('vector_y', 0)
        
        # Calcular respuesta correcta
        magnitud = calcular_magnitud(x, y)
        angulo = calcular_angulo(x, y)
        respuesta_correcta = f"{magnitud},{angulo}"
        opciones.append(respuesta_correcta)
        
        # Generar 3 opciones incorrectas
        for _ in range(3):
            # Variar magnitud ±1-2 y ángulo ±5-15°
            mag_var = magnitud + random.choice([-2, -1, 1, 2])
            ang_var = angulo + random.choice([-15, -10, -5, 5, 10, 15])
            opciones.append(f"{mag_var},{ang_var}")
        
        random.shuffle(opciones)

    # Generar imagen del vector
    if estado in ['pregunta', 'respuesta']:
        x = request.session.get('vector_x', 0)
        y = request.session.get('vector_y', 0)
        
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
        plt.title(f"Vector ({x}, {y})")
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        imagen = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

    context = {
        'estado': estado,
        'imagen': imagen,
        'opciones': opciones,
        'mensaje': mensaje,
        'correctas': request.session.get('correctas', 0),
        'incorrectas': request.session.get('incorrectas', 0),
        'vector_x': request.session.get('vector_x', 0),
        'vector_y': request.session.get('vector_y', 0),
    }
    
    return render(request, 'grafico_app/prueba_magnitud_angulo.html', context)

def suma_vectoresR2(request):
    if request.method == 'POST':
        x1 = int(request.POST.get('x1'))
        y1 = int(request.POST.get('y1'))
        x2 = int(request.POST.get('x2'))
        y2 = int(request.POST.get('y2'))

        # Cálculos de magnitudes y ángulos (en grados)
        def calcular_magnitud(x, y):
            return np.sqrt(x**2 + y**2)
        
        def calcular_angulo(x, y):
            return np.degrees(np.arctan2(y, x))
        
        mag_A = calcular_magnitud(x1, y1)
        ang_A = calcular_angulo(x1, y1)
        mag_B = calcular_magnitud(x2, y2)
        ang_B = calcular_angulo(x2, y2)
        mag_sum = calcular_magnitud(x1 + x2, y1 + y2)
        ang_sum = calcular_angulo(x1 + x2, y1 + y2)

        # Vector suma
        x_sum = x1 + x2
        y_sum = y1 + y2

        # Configuración del gráfico
        plt.figure(figsize=(12, 10))
        ax = plt.gca()
        
        # --- Vectores principales ---
        plt.quiver(0, 0, x1, y1, angles='xy', scale_units='xy', scale=1, 
                  color='#1f77b4', width=0.012, headwidth=7, headlength=10)
        plt.quiver(0, 0, x2, y2, angles='xy', scale_units='xy', scale=1, 
                  color='#2ca02c', width=0.012, headwidth=7, headlength=10)
        plt.quiver(0, 0, x_sum, y_sum, angles='xy', scale_units='xy', scale=1, 
                  color='#d62728', width=0.012, headwidth=7, headlength=10)

        # --- Extrapolares ---
        for x, y, color in [(x1, y1, '#1f77b4'), (x2, y2, '#2ca02c'), (x_sum, y_sum, '#d62728')]:
            plt.plot([0, x], [y, y], linestyle=':', color=color, alpha=0.6, linewidth=1.2)  # Horizontal
            plt.plot([x, x], [0, y], linestyle=':', color=color, alpha=0.6, linewidth=1.2)  # Vertical

        # --- Puntos en extremos ---
        plt.scatter([x1, x2, x_sum], [y1, y2, y_sum], 
                   color=['#1f77b4', '#2ca02c', '#d62728'], s=80, edgecolor='black', zorder=5)

        # --- Configuración de ejes ---
        max_range = max(abs(x1), abs(y1), abs(x2), abs(y2), abs(x_sum), abs(y_sum)) * 1.3
        plt.xlim(-max_range, max_range)
        plt.ylim(-max_range, max_range)
        plt.axhline(0, color='black', linewidth=1.2)
        plt.axvline(0, color='black', linewidth=1.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.5)
        ax.set_xticks(range(-int(max_range), int(max_range)+1, 2 if max_range <= 10 else 5))
        ax.set_yticks(range(-int(max_range), int(max_range)+1, 2 if max_range <= 10 else 5))

        # --- Ángulos y magnitudes ---
        # Cuadro de texto organizado
        info_text = (
            f"Vector A:\n"
            f"• Magnitud = {mag_A:.2f}\n"
            f"• Ángulo = {ang_A:.1f}°\n\n"
            f"Vector B:\n"
            f"• Magnitud = {mag_B:.2f}\n"
            f"• Ángulo = {ang_B:.1f}°\n\n"
            f"Suma:\n"
            f"• Magnitud = {mag_sum:.2f}\n"
            f"• Ángulo = {ang_sum:.1f}°"
        )
        
        plt.text(0.95, 0.95, info_text, transform=ax.transAxes,
                fontsize=11, verticalalignment='top', horizontalalignment='right',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round'))

        # --- Leyenda personalizada ---
        legend_elements = [
            plt.Line2D([0], [0], color='#1f77b4', lw=4, label=f'Vector A ({x1}, {y1})'),
            plt.Line2D([0], [0], color='#2ca02c', lw=4, label=f'Vector B ({x2}, {y2})'),
            plt.Line2D([0], [0], color='#d62728', lw=4, label=f'Suma ({x_sum}, {y_sum})')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

        plt.title('Suma de Vectores en R² con Ángulos y Magnitudes', pad=20, fontsize=14)

        # Guardar imagen
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer64 = base64.b64encode(imagen_png)
        imagen = buffer64.decode('utf-8')
        plt.close()

        return render(request, 'grafico_app/suma_vectoresR2.html', {'imagen': imagen})

    return render(request, 'grafico_app/suma_vectoresR2.html')

def resta_vectoresR2(request):
    if request.method == 'POST':
        x1 = int(request.POST.get('x1'))
        y1 = int(request.POST.get('y1'))
        x2 = int(request.POST.get('x2'))
        y2 = int(request.POST.get('y2'))

        # Cálculos de magnitudes y ángulos (en grados)
        def calcular_magnitud(x, y):
            return np.sqrt(x**2 + y**2)
        
        def calcular_angulo(x, y):
            return np.degrees(np.arctan2(y, x))
        
        mag_A = calcular_magnitud(x1, y1)
        ang_A = calcular_angulo(x1, y1)
        mag_B = calcular_magnitud(x2, y2)
        ang_B = calcular_angulo(x2, y2)
        
        # Vector resta (A - B)
        x_resta = x1 - x2
        y_resta = y1 - y2
        mag_resta = calcular_magnitud(x_resta, y_resta)
        ang_resta = calcular_angulo(x_resta, y_resta)

        # Configuración del gráfico
        plt.figure(figsize=(12, 10))
        ax = plt.gca()
        
        # --- Vectores principales ---
        plt.quiver(0, 0, x1, y1, angles='xy', scale_units='xy', scale=1, 
                  color='#1f77b4', width=0.012, headwidth=7, headlength=10)
        plt.quiver(0, 0, x2, y2, angles='xy', scale_units='xy', scale=1, 
                  color='#2ca02c', width=0.012, headwidth=7, headlength=10)
        plt.quiver(0, 0, x_resta, y_resta, angles='xy', scale_units='xy', scale=1, 
                  color='#d62728', width=0.012, headwidth=7, headlength=10)

        # --- Extrapolares ---
        for x, y, color in [(x1, y1, '#1f77b4'), (x2, y2, '#2ca02c'), (x_resta, y_resta, '#d62728')]:
            plt.plot([0, x], [y, y], linestyle=':', color=color, alpha=0.6, linewidth=1.2)  # Horizontal
            plt.plot([x, x], [0, y], linestyle=':', color=color, alpha=0.6, linewidth=1.2)  # Vertical

        # --- Puntos en extremos ---
        plt.scatter([x1, x2, x_resta], [y1, y2, y_resta], 
                   color=['#1f77b4', '#2ca02c', '#d62728'], s=80, edgecolor='black', zorder=5)

        # --- Configuración de ejes ---
        max_range = max(abs(x1), abs(y1), abs(x2), abs(y2), abs(x_resta), abs(y_resta)) * 1.3
        plt.xlim(-max_range, max_range)
        plt.ylim(-max_range, max_range)
        plt.axhline(0, color='black', linewidth=1.2)
        plt.axvline(0, color='black', linewidth=1.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.5)
        ax.set_xticks(range(-int(max_range), int(max_range)+1, 2 if max_range <= 10 else 5))
        ax.set_yticks(range(-int(max_range), int(max_range)+1, 2 if max_range <= 10 else 5))

        # --- Ángulos y magnitudes ---
        info_text = (
            f"Vector A:\n"
            f"• Magnitud = {mag_A:.2f}\n"
            f"• Ángulo = {ang_A:.1f}°\n\n"
            f"Vector B:\n"
            f"• Magnitud = {mag_B:.2f}\n"
            f"• Ángulo = {ang_B:.1f}°\n\n"
            f"Resta (A - B):\n"
            f"• Magnitud = {mag_resta:.2f}\n"
            f"• Ángulo = {ang_resta:.1f}°"
        )
        
        plt.text(0.95, 0.95, info_text, transform=ax.transAxes,
                fontsize=11, verticalalignment='top', horizontalalignment='right',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round'))

        # --- Leyenda personalizada ---
        legend_elements = [
            plt.Line2D([0], [0], color='#1f77b4', lw=4, label=f'Vector A ({x1}, {y1})'),
            plt.Line2D([0], [0], color='#2ca02c', lw=4, label=f'Vector B ({x2}, {y2})'),
            plt.Line2D([0], [0], color='#d62728', lw=4, label=f'Resta ({x_resta}, {y_resta})')
        ]
        plt.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

        plt.title('Resta de Vectores en R² con Ángulos y Magnitudes', pad=20, fontsize=14)

        # Guardar imagen
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer64 = base64.b64encode(imagen_png)
        imagen = buffer64.decode('utf-8')
        plt.close()

        return render(request, 'grafico_app/resta_vectoresR2.html', {'imagen': imagen})

    return render(request, 'grafico_app/resta_vectoresR2.html')

def multiplicacion_vectoresR2(request):
    if request.method == 'POST':
        x1 = int(request.POST.get('x1'))
        y1 = int(request.POST.get('y1'))
        x2 = int(request.POST.get('x2'))
        y2 = int(request.POST.get('y2'))

        # Cálculos matemáticos
        def producto_escalar(x1, y1, x2, y2):
            return x1*x2 + y1*y2
        
        def producto_vectorial(x1, y1, x2, y2):
            return x1*y2 - y1*x2
        
        esc = producto_escalar(x1, y1, x2, y2)
        vec = producto_vectorial(x1, y1, x2, y2)

        # Configuración del gráfico
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        
        # --- Vectores principales ---
        plt.quiver(0, 0, x1, y1, angles='xy', scale_units='xy', scale=1, 
                  color='#1f77b4', width=0.012, headwidth=7, headlength=10)
        plt.quiver(0, 0, x2, y2, angles='xy', scale_units='xy', scale=1, 
                  color='#2ca02c', width=0.012, headwidth=7, headlength=10)

        # --- Extrapolares ---
        for x, y, color in [(x1, y1, '#1f77b4'), (x2, y2, '#2ca02c')]:
            plt.plot([0, x], [y, y], linestyle=':', color=color, alpha=0.6, linewidth=1.2)  # Horizontal
            plt.plot([x, x], [0, y], linestyle=':', color=color, alpha=0.6, linewidth=1.2)  # Vertical

        # --- Puntos en extremos ---
        plt.scatter([x1, x2], [y1, y2], color=['#1f77b4', '#2ca02c'], s=80, edgecolor='black', zorder=5)

        # --- Configuración de ejes ---
        max_range = max(abs(x1), abs(y1), abs(x2), abs(y2)) * 1.5
        plt.xlim(-max_range, max_range)
        plt.ylim(-max_range, max_range)
        plt.axhline(0, color='black', linewidth=1.2)
        plt.axvline(0, color='black', linewidth=1.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.5)
        ax.set_xticks(range(-int(max_range), int(max_range)+1, 2 if max_range <= 10 else 5))
        ax.set_yticks(range(-int(max_range), int(max_range)+1, 2 if max_range <= 10 else 5))

        # --- Info matemática ---
        info_text = (
            f"Vector A ({x1}, {y1}):\n"
            f"• Magnitud = {np.sqrt(x1**2 + y1**2):.2f}\n\n"
            f"Vector B ({x2}, {y2}):\n"
            f"• Magnitud = {np.sqrt(x2**2 + y2**2):.2f}\n\n"
            f"Producto Escalar (A·B) = {esc:.2f}\n"
            f"Producto Vectorial (A×B) = {vec:.2f}"
        )
        plt.text(0.95, 0.95, info_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

        # --- Leyenda ---
        legend_elements = [
            plt.Line2D([0], [0], color='#1f77b4', lw=4, label=f'Vector A ({x1}, {y1})'),
            plt.Line2D([0], [0], color='#2ca02c', lw=4, label=f'Vector B ({x2}, {y2})')
        ]
        plt.legend(handles=legend_elements, loc='upper left')

        plt.title('Multiplicación de Vectores en R²', pad=20)

        # Guardar imagen
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer64 = base64.b64encode(imagen_png)
        imagen = buffer64.decode('utf-8')
        plt.close()

        return render(request, 'grafico_app/multiplicacion_vectoresR2.html', {
            'imagen': imagen,
            'producto_escalar': esc,
            'producto_vectorial': vec
        })

    return render(request, 'grafico_app/multiplicacion_vectoresR2.html')

def suma_vectoresR3(request):
    context = {}
    
    if request.method == 'POST':
        x1 = float(request.POST.get('x1', 0))
        y1 = float(request.POST.get('y1', 0))
        z1 = float(request.POST.get('z1', 0))
        x2 = float(request.POST.get('x2', 0))
        y2 = float(request.POST.get('y2', 0))
        z2 = float(request.POST.get('z2', 0))

        # Suma vectorial
        x_sum = x1 + x2
        y_sum = y1 + y2
        z_sum = z1 + z2

        # Configuración de estilo (igual a tu gráfica)
        color_proyecciones = '#003366'  # Azul oscuro como en tu imagen
        estilo_linea = dict(color=color_proyecciones, width=2, dash='dot')
        estilo_puntos = dict(color=color_proyecciones, size=4)

        # Función para crear todas las proyecciones y componentes (igual a tu gráfica)
        def crear_vector_con_proyecciones(x, y, z, color_vector):
            return [
                # Vector principal (línea sólida gruesa)
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[0, y], z=[0, z],
                     line=dict(color=color_vector, width=6),
                     name=f'({x:.1f}, {y:.1f}, {z:.1f})',
                     showlegend=True),
                
                # Proyección XY (vertical)
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, y], z=[0, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[x], y=[y], z=[0],
                     marker=estilo_puntos, showlegend=False),
                
                # Proyección XZ (horizontal)
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, y], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[x], y=[0], z=[z],
                     marker=estilo_puntos, showlegend=False),
                
                # Proyección YZ (lateral)
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[y, y], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[0], y=[y], z=[z],
                     marker=estilo_puntos, showlegend=False),
                
                # Líneas auxiliares (ejes)
                dict(type='scatter3d', mode='lines',
                     x=[x, 0], y=[y, y], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, 0], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[0, 0], y=[y, y], z=[z, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[0, 0], y=[y, 0], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, 0], y=[0, 0], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, 0], z=[z, 0],
                     line=estilo_linea, showlegend=False),
                
                # Componentes (descomposición)
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[0, 0], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, y], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, y], z=[0, z],
                     line=estilo_linea, showlegend=False)
            ]

        # Crear figura
        fig = go.Figure()

        # Vector A (rojo como en tu imagen)
        fig.add_traces(crear_vector_con_proyecciones(x1, y1, z1, 'red'))

        # Vector B (verde como en tu imagen)
        fig.add_traces(crear_vector_con_proyecciones(x2, y2, z2, 'green'))

        # Vector suma (azul como en tu imagen)
        fig.add_traces(crear_vector_con_proyecciones(x_sum, y_sum, z_sum, 'blue'))

        # Calcular rangos dinámicos (ajustado a tu gráfica)
        def calcular_rango(v1, v2, v3):
            valores = [v1, v2, v3, 0]  # Incluir el 0 como referencia
            margen = 0.5  # Margen pequeño como en tu gráfica
            return [min(valores) - margen, max(valores) + margen]

        x_range = calcular_rango(x1, x2, x_sum)
        y_range = calcular_rango(y1, y2, y_sum)
        z_range = calcular_rango(z1, z2, z_sum)

        # Configuración del layout (idéntico a tu gráfica)
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(
                    title='X',
                    range=x_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                yaxis=dict(
                    title='Y',
                    range=y_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                zaxis=dict(
                    title='Z',
                    range=z_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                aspectmode='cube',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=0.8),  # Vista isométrica como en tu gráfica
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0)
                )
            ),
            legend=dict(
                x=0.85,
                y=0.95,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                font=dict(size=10)
            ),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Convertir a HTML
        context['plot_html'] = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'grafico_app/suma_vectoresR3.html', context)


def resta_vectoresR3(request):
    context = {}
    
    if request.method == 'POST':
        x1 = float(request.POST.get('x1', 0))
        y1 = float(request.POST.get('y1', 0))
        z1 = float(request.POST.get('z1', 0))
        x2 = float(request.POST.get('x2', 0))
        y2 = float(request.POST.get('y2', 0))
        z2 = float(request.POST.get('z2', 0))

        # Resta vectorial (A - B)
        x_resta = x1 - x2
        y_resta = y1 - y2
        z_resta = z1 - z2

        # Configuración de estilo (idéntica a tu gráfica)
        color_proyecciones = '#003366'  # Azul oscuro
        estilo_linea = dict(color=color_proyecciones, width=2, dash='dot')
        estilo_puntos = dict(color=color_proyecciones, size=4)

        # Función para crear vector con proyecciones (igual a tu gráfica)
        def crear_vector_con_proyecciones(x, y, z, color_vector, nombre):
            return [
                # Vector principal
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[0, y], z=[0, z],
                     line=dict(color=color_vector, width=6),
                     name=nombre,
                     showlegend=True),
                
                # Proyecciones (igual a tu imagen)
                # XY
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, y], z=[0, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[x], y=[y], z=[0],
                     marker=estilo_puntos, showlegend=False),
                # XZ
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, y], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[x], y=[0], z=[z],
                     marker=estilo_puntos, showlegend=False),
                # YZ
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[y, y], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[0], y=[y], z=[z],
                     marker=estilo_puntos, showlegend=False),
                
                # Líneas auxiliares (igual a tu gráfica)
                dict(type='scatter3d', mode='lines',
                     x=[x, 0], y=[y, y], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, 0], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[0, 0], y=[y, y], z=[z, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[0, 0], y=[y, 0], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, 0], y=[0, 0], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, 0], z=[z, 0],
                     line=estilo_linea, showlegend=False),
                
                # Componentes (descomposición)
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[0, 0], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, y], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, y], z=[0, z],
                     line=estilo_linea, showlegend=False)
            ]

        # Crear figura
        fig = go.Figure()

        # Vector A (rojo)
        fig.add_traces(crear_vector_con_proyecciones(x1, y1, z1, 'red', f'A ({x1}, {y1}, {z1})'))

        # Vector B (verde) - mostramos el opuesto para la resta
        fig.add_traces(crear_vector_con_proyecciones(-x2, -y2, -z2, 'green', f'-B ({-x2}, {-y2}, {-z2})'))

        # Vector resta (azul)
        fig.add_traces(crear_vector_con_proyecciones(x_resta, y_resta, z_resta, 'blue', f'A-B ({x_resta}, {y_resta}, {z_resta})'))

        # Calcular rangos dinámicos (ajustado como en tu gráfica)
        def calcular_rango(v1, v2, v3):
            valores = [v1, v2, v3, 0, -v2, -v1]  # Incluir todos los valores relevantes
            margen = 0.5
            return [min(valores) - margen, max(valores) + margen]

        x_range = calcular_rango(x1, x2, x_resta)
        y_range = calcular_rango(y1, y2, y_resta)
        z_range = calcular_rango(z1, z2, z_resta)

        # Configuración del layout (idéntico a tu gráfica)
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(
                    title='X',
                    range=x_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                yaxis=dict(
                    title='Y',
                    range=y_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                zaxis=dict(
                    title='Z',
                    range=z_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                aspectmode='cube',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=0.8),
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0)
                )
            ),
            legend=dict(
                x=0.85,
                y=0.95,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                font=dict(size=10)
            ),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Convertir a HTML
        context['plot_html'] = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'grafico_app/resta_vectoresR3.html', context)


def multiplicacion_vectoresR3(request):
    context = {}
    
    if request.method == 'POST':
        x1 = float(request.POST.get('x1', 0))
        y1 = float(request.POST.get('y1', 0))
        z1 = float(request.POST.get('z1', 0))
        x2 = float(request.POST.get('x2', 0))
        y2 = float(request.POST.get('y2', 0))
        z2 = float(request.POST.get('z2', 0))

        # Producto escalar (punto)
        producto_escalar = x1*x2 + y1*y2 + z1*z2

        # Producto vectorial (cruz)
        x_cruz = y1*z2 - z1*y2
        y_cruz = z1*x2 - x1*z2
        z_cruz = x1*y2 - y1*x2

        # Configuración de estilo (igual a tu gráfica)
        color_proyecciones = '#003366'  # Azul oscuro
        estilo_linea = dict(color=color_proyecciones, width=2, dash='dot')
        estilo_puntos = dict(color=color_proyecciones, size=4)

        # Función para crear vector con proyecciones (igual a tu gráfica)
        def crear_vector_con_proyecciones(x, y, z, color_vector, nombre):
            return [
                # Vector principal
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[0, y], z=[0, z],
                     line=dict(color=color_vector, width=6),
                     name=nombre,
                     showlegend=True),
                
                # Proyecciones (XY, XZ, YZ)
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, y], z=[0, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[x], y=[y], z=[0],
                     marker=estilo_puntos, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, y], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[x], y=[0], z=[z],
                     marker=estilo_puntos, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[y, y], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='markers',
                     x=[0], y=[y], z=[z],
                     marker=estilo_puntos, showlegend=False),
                
                # Líneas auxiliares
                dict(type='scatter3d', mode='lines',
                     x=[x, 0], y=[y, y], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, 0], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[0, 0], y=[y, y], z=[z, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[0, 0], y=[y, 0], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, 0], y=[0, 0], z=[z, z],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, 0], z=[z, 0],
                     line=estilo_linea, showlegend=False),
                
                # Componentes
                dict(type='scatter3d', mode='lines',
                     x=[0, x], y=[0, 0], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[0, y], z=[0, 0],
                     line=estilo_linea, showlegend=False),
                dict(type='scatter3d', mode='lines',
                     x=[x, x], y=[y, y], z=[0, z],
                     line=estilo_linea, showlegend=False)
            ]

        # Crear figura
        fig = go.Figure()

        # Vector A (rojo)
        fig.add_traces(crear_vector_con_proyecciones(x1, y1, z1, 'red', f'A ({x1}, {y1}, {z1})'))

        # Vector B (verde)
        fig.add_traces(crear_vector_con_proyecciones(x2, y2, z2, 'green', f'B ({x2}, {y2}, {z2})'))

        # Producto vectorial (azul) - solo si no es cero
        if not (x_cruz == 0 and y_cruz == 0 and z_cruz == 0):
            fig.add_traces(crear_vector_con_proyecciones(
                x_cruz, y_cruz, z_cruz, 
                'blue', 
                f'A×B ({x_cruz:.2f}, {y_cruz:.2f}, {z_cruz:.2f})'
            ))

        # Calcular rangos dinámicos
        def calcular_rango(v1, v2, v3):
            valores = [v1, v2, v3, 0]
            margen = 0.5
            return [min(valores) - margen, max(valores) + margen]

        # Ajustar rangos para incluir todos los vectores
        x_vals = [x1, x2, x_cruz]
        y_vals = [y1, y2, y_cruz]
        z_vals = [z1, z2, z_cruz]

        x_range = calcular_rango(min(x_vals), max(x_vals), 0)
        y_range = calcular_rango(min(y_vals), max(y_vals), 0)
        z_range = calcular_rango(min(z_vals), max(z_vals), 0)

        # Configuración del layout (idéntico a tu gráfica)
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=30),
            scene=dict(
                xaxis=dict(
                    title='X',
                    range=x_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                yaxis=dict(
                    title='Y',
                    range=y_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                zaxis=dict(
                    title='Z',
                    range=z_range,
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='lightgray',
                    showspikes=False
                ),
                aspectmode='cube',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=0.8),
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0)
                )
            ),
            legend=dict(
                x=0.85,
                y=0.95,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                font=dict(size=10)
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            title=dict(
                text=f"Producto Escalar: {producto_escalar:.2f} | Producto Vectorial: ({x_cruz:.2f}, {y_cruz:.2f}, {z_cruz:.2f})",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font=dict(size=12)
        )
        )
        # Convertir a HTML
        context['plot_html'] = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'grafico_app/multiplicacion_vectoresR3.html', context)

def graficar_regresion_lineal(request):
    if request.method == 'POST':
        x_input = request.POST.get('x')
        y_input = request.POST.get('y')

        try:
            x = list(map(float, x_input.split(',')))
            y = list(map(float, y_input.split(',')))
        except Exception:
            return render(request, 'grafico_app/regresion.html', {
                'error': 'Por favor, ingrese valores numéricos separados por comas.'
            })

        if len(x) != len(y) or len(x) < 2:
            return render(request, 'grafico_app/regresion.html', {
                'error': 'Debe ingresar la misma cantidad de valores X e Y (mínimo 2).'
            })

        # Calcular regresión lineal
        coeficientes = np.polyfit(x, y, 1)
        pendiente, intercepto = coeficientes
        y_pred = np.polyval(coeficientes, x)

        # Crear la figura
        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, color='cyan', label='Datos originales')
        plt.plot(x, y_pred, color='orange', label=f'Regresión: y = {pendiente:.2f}x + {intercepto:.2f}')
        plt.title('Regresión Lineal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()

        # Guardar imagen como base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_png = buffer.getvalue()
        buffer64 = base64.b64encode(imagen_png)
        imagen = buffer64.decode('utf-8')
        plt.close()

        # --- 🧠 Análisis de hipótesis ---
        if abs(pendiente) < 0.01:  # Pendiente muy pequeña ≈ sin relación
            decision = "Se acepta la hipótesis nula (H₀)."
            explicacion = (
                "La pendiente calculada es muy cercana a cero, "
                "por lo tanto no se observa una relación lineal significativa entre las variables."
            )
        else:
            decision = "Se rechaza la hipótesis nula (H₀)."
            if pendiente > 0:
                explicacion = (
                    "La pendiente es positiva, lo que indica que existe una relación lineal directa: "
                    "al aumentar X, también aumenta Y."
                )
            else:
                explicacion = (
                    "La pendiente es negativa, lo que indica una relación lineal inversa: "
                    "al aumentar X, Y tiende a disminuir."
                )

        # --- 🔮 Predicción para T = 2000 ---
        T = 2000
        c_pred = pendiente * T + intercepto

        return render(request, 'grafico_app/regresion.html', {
            'imagen': imagen,
            'pendiente': pendiente,
            'intercepto': intercepto,
            'decision': decision,
            'explicacion': explicacion,
            'c_pred': c_pred,
            'T_pred': T
        })

    return render(request, 'grafico_app/regresion.html')


def grafico_proyectil(request):
    # Valores por defecto
    v0 = 20      # m/s
    angXY = 45   # grados
    angZ = 30    # grados

    if request.method == 'POST':
        v0 = float(request.POST.get('v0', v0))
        angXY = float(request.POST.get('angXY', angXY))
        angZ = float(request.POST.get('angZ', angZ))

    context = {
        'v0': v0,
        'angXY': angXY,
        'angZ': angZ
    }
    return render(request, 'grafico_app/grafico_proyectil.html', context)

def area_bajo_curva(request):
    x_values = []
    y_values = []
    a = b = 0
    funcion = ""

    if request.method == 'POST':
        try:
            funcion = request.POST.get('funcion', 'x**2')
            a = float(request.POST.get('a', 0))
            b = float(request.POST.get('b', 2))

            # Crear los puntos
            x = np.linspace(a, b, 200)
            y = eval(funcion.replace('x', 'x'))  # Evaluar la función

            # Convertir a listas para Plotly
            x_values = x.tolist()
            y_values = y.tolist()

        except Exception as e:
            print("Error al evaluar la función:", e)

    context = {
        'x_values': json.dumps(x_values),
        'y_values': json.dumps(y_values),
        'a': a,
        'b': b,
        'funcion': funcion
    }
    return render(request, 'grafico_app/area_bajo_curva.html', context)

def Prueba_Facil_Regresion(request):
    # Inicializar contadores
    correctas = request.session.get('correctas_regresion', 0)
    incorrectas = request.session.get('incorrectas_regresion', 0)

    if request.method == 'POST':
        # Recuperar valores reales de la sesión
        pendiente_real = request.session.get('pendiente_real')
        intercepto_real = request.session.get('intercepto_real')
        
        # Obtener respuestas del usuario
        try:
            pendiente_usuario = float(request.POST.get('pendiente'))
            intercepto_usuario = float(request.POST.get('intercepto'))
        except (TypeError, ValueError):
            pendiente_usuario = 0
            intercepto_usuario = 0

        # Verificar respuesta (con margen de error del 5%)
        margen_error = 0.05
        pendiente_correcta = abs(pendiente_usuario - pendiente_real) <= abs(pendiente_real * margen_error)
        intercepto_correcto = abs(intercepto_usuario - intercepto_real) <= abs(intercepto_real * margen_error)
        
        correcto = pendiente_correcta and intercepto_correcto

        if correcto:
            correctas += 1
            mensaje = f'✅ ¡Correcto! La ecuación es: y = {pendiente_real:.2f}x + {intercepto_real:.2f}'
        else:
            incorrectas += 1
            mensaje = f'❌ Incorrecto. La ecuación correcta era: y = {pendiente_real:.2f}x + {intercepto_real:.2f}<br>'
            mensaje += f'Tu respuesta: y = {pendiente_usuario:.2f}x + {intercepto_usuario:.2f}'

        request.session['correctas_regresion'] = correctas
        request.session['incorrectas_regresion'] = incorrectas

        # Graficar ambas rectas
        x_real = request.session.get('x_data')
        y_real = request.session.get('y_data')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Datos originales
        ax.scatter(x_real, y_real, color='cyan', label='Datos', s=50)
        
        # Recta correcta
        x_line = np.array([min(x_real), max(x_real)])
        y_line_real = pendiente_real * x_line + intercepto_real
        ax.plot(x_line, y_line_real, 'r-', linewidth=2, label=f'Correcto: y = {pendiente_real:.2f}x + {intercepto_real:.2f}')
        
        # Recta del usuario
        y_line_usuario = pendiente_usuario * x_line + intercepto_usuario
        ax.plot(x_line, y_line_usuario, 'b--', linewidth=2, label=f'Tu respuesta: y = {pendiente_usuario:.2f}x + {intercepto_usuario:.2f}')
        
        ax.set_xlim(min(x_real)-1, max(x_real)+1)
        ax.set_ylim(min(y_real)-1, max(y_real)+1)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Regresión Lineal - Comparación')
        
        # Convertir a base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        imagen = base64.b64encode(buf.getvalue()).decode('utf-8')

        return render(request, 'grafico_app/prueba_facil_regresion.html', {
            'imagen': imagen,
            'mensaje': mensaje,
            'estado': 'respuesta',
            'correctas': correctas,
            'incorrectas': incorrectas
        })

    # GET: Generar nueva pregunta
    # Crear datos aleatorios para la regresión
    n_puntos = np.random.randint(5, 8)  # Entre 5 y 7 puntos
    x_real = np.random.uniform(1, 10, n_puntos)
    
    # Generar pendiente e intercepto aleatorios
    pendiente_real = np.random.uniform(-3, 3)
    intercepto_real = np.random.uniform(-5, 5)
    
    # Agregar algo de ruido a los datos
    ruido = np.random.normal(0, 0.5, n_puntos)
    y_real = pendiente_real * x_real + intercepto_real + ruido

    # Guardar en sesión
    request.session['pendiente_real'] = pendiente_real
    request.session['intercepto_real'] = intercepto_real
    request.session['x_data'] = x_real.tolist()
    request.session['y_data'] = y_real.tolist()

    # Graficar solo los datos (sin la recta)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x_real, y_real, color='cyan', s=60)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Encuentra la recta de regresión para estos datos')
    
    # Ajustar límites
    ax.set_xlim(min(x_real)-1, max(x_real)+1)
    ax.set_ylim(min(y_real)-1, max(y_real)+1)

    # Convertir a base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    imagen = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'grafico_app/prueba_facil_regresion.html', {
        'imagen': imagen,
        'estado': 'pregunta',
        'correctas': correctas,
        'incorrectas': incorrectas
    })


import numpy as np
import json
from django.shortcuts import render

def Prueba_Facil_Area(request):
    # Inicializar contadores
    correctas = request.session.get('correctas_area', 0)
    incorrectas = request.session.get('incorrectas_area', 0)

    if request.method == 'POST':
        # Recuperar valores reales de la sesión
        area_real = request.session.get('area_real')
        funcion_real = request.session.get('funcion_real')
        a_real = request.session.get('a_real')
        b_real = request.session.get('b_real')
        
        # Obtener respuesta del usuario
        try:
            area_usuario = float(request.POST.get('area_respuesta'))
        except (TypeError, ValueError):
            area_usuario = 0

        # Verificar respuesta (con margen de error del 10%)
        margen_error = 0.10
        correcto = abs(area_usuario - area_real) <= abs(area_real * margen_error)

        if correcto:
            correctas += 1
            mensaje = f'✅ ¡Correcto! El área bajo la curva es aproximadamente {area_real:.2f}'
        else:
            incorrectas += 1
            mensaje = f'❌ Incorrecto. El área real es {area_real:.2f}<br>Tu respuesta: {area_usuario:.2f}'

        # Explicación adicional
        explicacion = f"El área bajo f(x) = {funcion_real} desde {a_real} hasta {b_real} se calcula mediante integración definida."

        request.session['correctas_area'] = correctas
        request.session['incorrectas_area'] = incorrectas

        # Preparar datos para el gráfico
        x_values = request.session.get('x_data', [])
        y_values = request.session.get('y_data', [])

        return render(request, 'grafico_app/prueba_facil_area.html', {
            'x_values': json.dumps(x_values),
            'y_values': json.dumps(y_values),
            'funcion': funcion_real,
            'a': a_real,
            'b': b_real,
            'mensaje': mensaje,
            'explicacion': explicacion,
            'estado': 'respuesta',
            'correctas': correctas,
            'incorrectas': incorrectas
        })

    # GET: Generar nueva pregunta
    # Seleccionar función aleatoria con áreas precalculadas
    funciones = [
        {'func': 'x**2', 'nombre': 'x²', 'a': 0, 'b': 3, 'area': 9.0},
        {'func': 'x', 'nombre': 'x', 'a': 0, 'b': 4, 'area': 8.0},
        {'func': 'np.sqrt(x)', 'nombre': '√x', 'a': 0, 'b': 4, 'area': 5.33},
        {'func': 'x**3', 'nombre': 'x³', 'a': 0, 'b': 2, 'area': 4.0},
        {'func': '2*x + 1', 'nombre': '2x + 1', 'a': 0, 'b': 3, 'area': 12.0},
        {'func': '4 - x**2', 'nombre': '4 - x²', 'a': 0, 'b': 2, 'area': 5.33},
        {'func': 'np.sin(x)', 'nombre': 'sin(x)', 'a': 0, 'b': 3.14, 'area': 2.0},
        {'func': 'np.exp(x/2)', 'nombre': 'e^(x/2)', 'a': 0, 'b': 2, 'area': 2.3}
    ]
    
    funcion_data = np.random.choice(funciones)
    funcion_str = funcion_data['func']
    funcion_nombre = funcion_data['nombre']
    a = funcion_data['a']
    b = funcion_data['b']
    area_real = funcion_data['area']

    # Generar puntos para el gráfico - FORMA CORREGIDA
    x = np.linspace(a, b, 200)
    
    # Evaluar la función de forma segura
    try:
        if 'np.sqrt' in funcion_str:
            y = np.sqrt(x)
        elif 'np.sin' in funcion_str:
            y = np.sin(x)
        elif 'np.exp' in funcion_str:
            y = np.exp(x/2)
        else:
            # Para funciones básicas sin numpy
            y = eval(funcion_str, {'x': x, 'np': np})
    except Exception as e:
        # En caso de error, usar función por defecto
        print(f"Error evaluando función: {e}")
        y = x**2

    # Asegurarse de que no hay valores NaN o infinitos
    y = np.nan_to_num(y, nan=0.0, posinf=10.0, neginf=0.0)
    
    # Convertir a listas Python
    x_list = x.tolist()
    y_list = y.tolist()

    # DEBUG: Verificar los datos
    print(f"Función: {funcion_nombre}")
    print(f"X: {x_list[:5]}...")  # Primeros 5 elementos
    print(f"Y: {y_list[:5]}...")  # Primeros 5 elementos

    # Guardar en sesión
    request.session['area_real'] = area_real
    request.session['funcion_real'] = funcion_nombre
    request.session['a_real'] = a
    request.session['b_real'] = b
    request.session['x_data'] = x_list
    request.session['y_data'] = y_list

    return render(request, 'grafico_app/prueba_facil_area.html', {
        'x_values': json.dumps(x_list),
        'y_values': json.dumps(y_list),
        'funcion': funcion_nombre,
        'a': a,
        'b': b,
        'estado': 'pregunta',
        'correctas': correctas,
        'incorrectas': incorrectas
    })