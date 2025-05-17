from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from .forms import VectorForm
import json
import random
import numpy as np
import matplotlib.patches as patches


def inicio(request):
    return render(request, 'grafico_app/Inicio.html')  # Asegúrate de tener este template

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