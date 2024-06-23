import numpy as np
import tensorflow as tf
import tkinter as tk
from math import cos, sin

# Cargar el modelo guardado
model = tf.keras.models.load_model('models/robot_arm_model2.h5')

# Configuración del brazo robótico
l1, l2, l3 = 100, 100, 100  # Longitudes de los segmentos del brazo
origin_x, origin_y = 250, 250  # Punto de origen del brazo en el canvas

# Función para dibujar el brazo
def draw_arm(canvas, theta1, theta2, theta3):
    theta1 = np.radians(theta1)
    theta2 = np.radians(theta2)
    theta3 = np.radians(theta3)

    x0, y0 = origin_x, origin_y
    x1, y1 = x0 + l1 * cos(theta1), y0 + l1 * sin(theta1)
    x2, y2 = x1 + l2 * cos(theta1 + theta2), y1 + l2 * sin(theta1 + theta2)
    x3, y3 = x2 + l3 * cos(theta1 + theta2 + theta3), y2 + l3 * sin(theta1 + theta2 + theta3)

    canvas.create_line(x0, y0, x1, y1, fill="blue", width=4)
    canvas.create_line(x1, y1, x2, y2, fill="red", width=4)
    canvas.create_line(x2, y2, x3, y3, fill="green", width=4)

# Función para mover el brazo
def move_arm(x, y):
    # Convertir las coordenadas del canvas al sistema de coordenadas del brazo
    x_normalized = x - origin_x
    y_normalized = y - origin_y
    
    # Usar el modelo para predecir los ángulos
    angles = model.predict(np.array([[x_normalized, y_normalized]]))[0]
    theta1, theta2, theta3 = angles
    canvas.delete("all")
    
    # Dibujar la base
    draw_base(canvas)  
    draw_arm(canvas, theta1, theta2, theta3)

    # Dibujar el objeto en su nueva posición
    canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")

# Función para iniciar la simulación
def start_simulation():
    x_start, y_start = 150, 150  # Posición inicial del objeto
    x_end, y_end = 350, 350  # Posición final del objeto
    
    def move_to_position(x, y):
        move_arm(x, y)
    
    move_to_position(x_start, y_start)  # Mover el brazo al objeto
    root.after(1000, lambda: move_to_position(x_end, y_end))  # Mover el brazo al nuevo lugar

# Función para dibujar la base del brazo robótico
def draw_base(canvas):
    canvas.create_rectangle(200, 200, 300, 300, outline="black", width=4)

# Crear la ventana principal
root = tk.Tk()
root.title("Simulador de Brazo Robótico")

canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Dibujar la base y el brazo en la posición inicial
draw_base(canvas)
draw_arm(canvas, 0, 0, 0)

# Dibujar el objeto en la posición inicial
canvas.create_oval(145, 145, 155, 155, fill="black")

# Crear un botón para iniciar la simulación
start_button = tk.Button(root, text="Iniciar", command=start_simulation)
start_button.pack()

root.mainloop()
