from openpyxl import load_workbook


class ObtenerDatos:
    def __init__(self):
        self.archivo_nombre = 'Programa_cirugia_mes1.xlsx'
        self.hoja_nombre = input("Ingrese el nombre del quirofano: ")
        self.archivo = load_workbook(self.archivo_nombre)
        self.hoja = self.archivo[self.hoja_nombre]

    def obtener_semana(self):
        self.semana1 = {"celda_rango_inicio": "A1", "celda_rango_fin": "H25", "fila_dias_inicio": "B1", "fila_dias_fin": "H1"}
        self.semana2 = {"celda_rango_inicio": "J1", "celda_rango_fin": "Q25", "fila_dias_inicio": "K1", "fila_dias_fin": "Q1"}
        self.semana3 = {"celda_rango_inicio": "S1", "celda_rango_fin": "Z25", "fila_dias_inicio": "T1", "fila_dias_fin": "Z1"}
        self.semana4 = {"celda_rango_inicio": "AB1", "celda_rango_fin": "AI25", "fila_dias_inicio": "AC1", "fila_dias_fin": "AI1"}

        semana = input("Ingrese la semana (1, 2, 3, 4): ")
        
        if semana == "1":
            self.celda_rango_inicio = self.semana1["celda_rango_inicio"]
            self.celda_rango_fin = self.semana1["celda_rango_fin"]
            self.fila_dias_inicio = self.semana1["fila_dias_inicio"]
            self.fila_dias_fin = self.semana1["fila_dias_fin"]
        elif semana == "2":
            self.celda_rango_inicio = self.semana2["celda_rango_inicio"]
            self.celda_rango_fin= self.semana2["celda_rango_fin"]
            self.fila_dias_inicio = self.semana2["fila_dias_inicio"]
            self.fila_dias_fin = self.semana2["fila_dias_fin"]
        elif semana == "3":
            self.celda_rango_inicio = self.semana3["celda_rango_inicio"]
            self.celda_rango_fin = self.semana3["celda_rango_fin"]
            self.fila_dias_inicio = self.semana3["fila_dias_inicio"]
            self.fila_dias_fin = self.semana3["fila_dias_fin"]
        elif semana == "4":
            self.celda_rango_inicio = self.semana4["celda_rango_inicio"]
            self.celda_rango_fin = self.semana4["celda_rango_fin"]
            self.fila_dias_inicio = self.semana4["fila_dias_inicio"]
            self.fila_dias_fin = self.semana4["fila_dias_fin"]
        else:
            print("Semana inválida. Ingrese una semana del 1 al 4.")
            exit()
        dia = str(input('Ingrese el dia de interes: '))
        accion = str(input('Que desea hacer?(p/c/o): '))
        return{
            'semana1': self.semana1,
            'semana2': self.semana2,
            'semana3': self.semana3,
            'semana4': self.semana4,
            'dia': dia,
            'accion': accion,
            'semana': semana,
            'celda_rango_inicio': self.celda_rango_inicio,
            'celda_rango_fin': self.celda_rango_fin,
            'fila_dias_inicio': self.fila_dias_inicio,
            'fila_dias_fin': self.fila_dias_fin
        }

    def obtener_rangos_celdas(self):
        self.celda_rango = self.hoja[self.celda_rango_inicio:self.celda_rango_fin]
        self.fila_dias = self.hoja[self.fila_dias_inicio:self.fila_dias_fin]
        return{'celda_rango': self.celda_rango,
               'fila_dias': self.fila_dias}