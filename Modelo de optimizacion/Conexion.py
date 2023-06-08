import tkinter as tk
import pymysql

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
ventana.title("Selección de Médico")

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
boton_obtener_medicos = tk.Button(ventana, text="Ver nombres", command=obtener_medicos)
boton_obtener_medicos.pack()

# Cuadro de médicos
cuadro_medicos = tk.Listbox(ventana, width=50, height=10)
cuadro_medicos.pack()

# Cuadro de especialista seleccionado
cuadro_especialista = tk.Entry(ventana, textvariable=medico_seleccionado, width=50, state="readonly")
cuadro_especialista.pack()


# Asignar el nombre del especialista seleccionado al cuadro de texto
def seleccionar_medico(event):
    widget = event.widget
    indice = int(widget.curselection()[0])
    nombre_medico = widget.get(indice)
    medico_seleccionado.set(nombre_medico)

cuadro_medicos.bind("<<ListboxSelect>>", seleccionar_medico)

# Ejecutar interfaz
ventana.mainloop()

# Cerrar conexión a la base de datos al cerrar la ventana
cursor.close()
conexion.close()