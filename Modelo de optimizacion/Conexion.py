import tkinter as tk
import pymysql
from datetime import datetime, timedelta

# Conexión a la base de datos
conexion = pymysql.connect(
    host="localhost",
    user="root",
    password="Qwertyuiop12",
    database="cirugia"
)
cursor = conexion.cursor()

# Crear ventana
ventana = tk.Tk()
ventana.title("Interfaz Cirugias")

# Dimensiones de la ventana
ancho_ventana = 500
alto_ventana = 400

# Obtener el tamaño de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular la posición central de la ventana
x_pos = int((ancho_pantalla / 2) - (ancho_ventana / 2))
y_pos = int((alto_pantalla / 2) - (alto_ventana / 2))

# Establecer la geometría de la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Variables de control
especialidad_seleccionada = tk.StringVar()
medico_seleccionado = tk.StringVar()
cirugia_seleccionada = tk.StringVar()
hora_inicio = tk.StringVar()
hora_fin = tk.StringVar()

# Función para obtener los médicos según la especialidad seleccionada
def obtener_medicos():
    especialidad = especialidad_seleccionada.get()

    # Limpiar cuadro de médicos antes de cargar nuevos datos
    cuadro_medicos.delete(0, tk.END)

    # Consulta a la base de datos
    consulta = "SELECT nombre_medico FROM EE WHERE especialidad = %s"
    cursor.execute(consulta, (especialidad,))

    # Obtener y mostrar los resultados en el cuadro de médicos
    for row in cursor.fetchall():
        cuadro_medicos.insert(tk.END, row[0])

    # Limpiar cuadro de especialista seleccionado
    medico_seleccionado.set("")

    # Limpiar cuadro de cirugías
    cuadro_cirugias.delete(0, tk.END)
    cirugia_seleccionada.set("")

# Función para obtener las cirugías de la especialidad seleccionada
def obtener_cirugias():
    especialidad = especialidad_seleccionada.get()

    # Limpiar cuadro de cirugías antes de cargar nuevos datos
    cuadro_cirugias.delete(0, tk.END)

    # Consulta a la base de datos
    consulta = "SELECT nombre_cirugia FROM cirugias WHERE especialidad = %s"
    cursor.execute(consulta, (especialidad,))

    # Obtener y mostrar los resultados en el cuadro de cirugías
    for row in cursor.fetchall():
        cuadro_cirugias.insert(tk.END, row[0])

    # Limpiar cuadro de cirugia seleccionada
    cirugia_seleccionada.set("")

# Función para calcular la hora de finalización
def calcular_hora_fin():
    seleccion = cuadro_cirugias.curselection()
    if seleccion:
        indice = int(seleccion[0])
        nombre_cirugia = cuadro_cirugias.get(indice)
        consulta_duracion = "SELECT duracion_horas, duracion_minutos FROM cirugias WHERE nombre_cirugia = %s"
        cursor.execute(consulta_duracion, (nombre_cirugia,))
        duracion = cursor.fetchone()
        duracion_horas = int(duracion[0])
        duracion_minutos = int(duracion[1])

        hora_inicio_str = hora_inicio.get()
        try:
            hora_inicio_dt = datetime.strptime(hora_inicio_str, "%H:%M")
            hora_fin_dt = hora_inicio_dt + timedelta(hours=duracion_horas, minutes=duracion_minutos)
            hora_fin_str = hora_fin_dt.strftime("%H:%M")
            hora_fin.set(hora_fin_str)
        except ValueError:
            hora_fin.set("Error")

# Obtener las especialidades desde la base de datos
consulta_especialidades = "SELECT DISTINCT especialidad FROM EE"
cursor.execute(consulta_especialidades)
especialidades = [row[0] for row in cursor.fetchall()]

# Etiqueta y cuadro de selección de especialidad
etiqueta_especialidad = tk.Label(ventana, text="Seleccione la Especialidad:")
etiqueta_especialidad.pack()
cuadro_especialidades = tk.OptionMenu(ventana, especialidad_seleccionada, *especialidades)
cuadro_especialidades.pack()

# Botón para obtener los médicos según la especialidad seleccionada
boton_obtener_medicos = tk.Button(ventana, text="Especialistas", command=obtener_medicos)
boton_obtener_medicos.pack()

# Cuadro de médicos
cuadro_medicos = tk.Listbox(ventana, width=50, height=10)
cuadro_medicos.pack()

# Cuadro de especialista seleccionado
cuadro_especialista = tk.Entry(ventana, textvariable=medico_seleccionado, width=50, state="readonly")
cuadro_especialista.pack()

# Botón para obtener las cirugías de la especialidad seleccionada
boton_obtener_cirugias = tk.Button(ventana, text="Cirugias", command=obtener_cirugias)
boton_obtener_cirugias.pack()

# Cuadro de cirugías
cuadro_cirugias = tk.Listbox(ventana, width=50, height=10)
cuadro_cirugias.pack()

# Cuadro de cirugía seleccionada
cuadro_cirugia_seleccionada = tk.Entry(ventana, textvariable=cirugia_seleccionada, width=50, state="readonly")
cuadro_cirugia_seleccionada.pack()

# Etiqueta y cuadro de selección de hora de inicio
etiqueta_hora_inicio = tk.Label(ventana, text="Hora de Inicio:")
etiqueta_hora_inicio.pack()
cuadro_hora_inicio = tk.Entry(ventana, textvariable=hora_inicio)
cuadro_hora_inicio.pack()

# Etiqueta y cuadro de hora de fin
etiqueta_hora_fin = tk.Label(ventana, text="Hora de Finalización:")
etiqueta_hora_fin.pack()
cuadro_hora_fin = tk.Entry(ventana, textvariable=hora_fin, state="readonly")
cuadro_hora_fin.pack()

# Botón para calcular la hora de finalización
boton_calcular_hora_fin = tk.Button(ventana, text="Agendar", command=calcular_hora_fin)
boton_calcular_hora_fin.pack()

# Asignar el nombre de la cirugía seleccionada al cuadro de texto
def seleccionar_cirugia(event):
    widget = event.widget
    if widget.curselection():
        indice = int(widget.curselection()[0])
        nombre_cirugia = widget.get(indice)
        cirugia_seleccionada.set(nombre_cirugia)

cuadro_cirugias.bind("<<ListboxSelect>>", seleccionar_cirugia)

# Asignar el nombre del médico seleccionado al cuadro de texto
def seleccionar_medico(event):
    widget = event.widget
    if widget.curselection():
        indice = int(widget.curselection()[0])
        nombre_medico = widget.get(indice)
        medico_seleccionado.set(nombre_medico)

cuadro_medicos.bind("<<ListboxSelect>>", seleccionar_medico)

# Ejecutar interfaz
ventana.mainloop()

# Cerrar conexión a la base de datos al cerrar la ventana
cursor.close()
conexion.close()

