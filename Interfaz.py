from tkinter import *
from PIL import ImageTk, Image

ventana = Tk()
ventana.title('Programacion de cirugia')
ventana.geometry('1000x800')
ventana.resizable(False, False)
ventana.iconbitmap('Logo-clinica-ces.ico')

fondo = PhotoImage(file = 'C:/Users/artur/Documents/Practica2/Codigos/Optimizacion tiempos/Logo clinica ces.png')
fondo1 = Label(ventana, image = fondo).place(x = -385, y = -300, relwidth = 1, relheight = 1)

titulo = Label(ventana, text='Pogramacion de Cirugia', font=('Lucinda Console', 20)).place(x = 390, y = 100)

ventana.mainloop()
