from Data_Base import*
from Obtener_Datos import*


class EditarCita(ObtenerDatos, DataBase):
    def __init__(self):
        super().__init__()
        datos = self.obtener_semana()
        self.semana = datos['semana']
        self.semana1 = datos["semana1"]
        self.semana2 = datos["semana2"]
        self.semana3 = datos["semana3"]
        self.semana4 = datos["semana4"]
        self.dia = datos["dia"]
        self.accion = datos["accion"]
        self.semana = datos["semana"]
        self.celda_rango_inicio = datos["celda_rango_inicio"]
        self.celda_rango_fin = datos["celda_rango_fin"]
        self.fila_dias_inicio = datos["fila_dias_inicio"]
        self.fila_dias_fin = datos["fila_dias_fin"]
        datos2 = self.obtener_rangos_celdas()
        self.celda_rango = datos2["celda_rango"]
        self.fila_dias = datos2["fila_dias"]
        self.database = DataBase()

    
    def obtener_especialidad(self):
        self.cedula = input('Ingrese la cedula del paciente: ')
        estado = self.database.revisar_estado(self.cedula)
        if estado == 'Programado':
            print('El paciente ya ha sido programado.')
            self.database.mostrar_fila(self.cedula)
            exit()
        elif estado == 'Pendiente':
            nombre_especialidad = self.database.select_especialidad(self.cedula)
            return nombre_especialidad
    

    def obtener_horas_cancelar(self):
        self.cedula = input('Ingrese la cedula del paciente al que quiere cancelarle cita: ')
        estado = self.database.revisar_estado(self.cedula)
        if estado == 'Pendiente':
            print('El paciente no ha sido programado.')
            self.database.mostrar_fila(self.cedula)
            exit()
        elif estado == 'Programado':
            nombre_especialidad = self.database.select_especialidad(self.cedula)
            return nombre_especialidad

    
    def obtener_cirugia(self):
        nombre_cirugia = self.database.select_cirugia(self.cedula)
        return nombre_cirugia
    

    def obtener_duracion(self, cirugia, especialidad):
        duracion = self.database.select_duracion(cirugia, especialidad)
        return duracion
    

    def obtener_codigo(self, cirugia, especialidad):
        codigo = self.database.select_codigo(cirugia, especialidad)
        return codigo
    

    def cambio_nombre_especialista(self, especialista):
        self.database.actualizar_especialista(self.cedula, especialista)


    def cambio_nombre_especialistaP(self, especialista):
        self.database.actualizar_especialistaP(self.cedula, especialista)


    def nombre_programa(self, nombre):
        self.database.actualizar_nombre(self.cedula, nombre)


    def cambio_programado(self):
        self.database.actualizar_programado(self.cedula)
        self.database.mostrar_fila(self.cedula)


    def cambio_quirofano(self):
        self.database.actualizar_quirofano(self.cedula, self.hoja_nombre)


    def cambio_semana(self):
        self.database.actualizar_semana(self.cedula, self.semana)


    def cambio_dia(self):
        self.database.actualizar_dia(self.cedula, self.dia)


    def cambio_pendiente(self):
        self.database.actualizar_pendiente(self.cedula)
        self.database.mostrar_fila(self.cedula)


    def cambio_quirofanoP(self):
        self.database.actualizar_quirofanoP(self.cedula, self.hoja_nombre)


    def cambio_semanaP(self):
        self.database.actualizar_semanaP(self.cedula, self.semana)


    def cambio_diaP(self):
        self.database.actualizar_diaP(self.cedula, self.dia)


    def nombre_pendiente(self):
        self.database.actualizar_nombreP(self.cedula)


    def close_database(self):
        self.database.close()  


    def buscar_dia(self):
        self.encontrado = False
        self.columna_dia = None
        for celda in self.fila_dias[0]:
            if celda.value.lower() == self.dia.lower():
                print('El día fue encontrado en el calendario.')
                self.encontrado = True
                self.columna_dia = celda.column
                break
        if not self.encontrado:      
            print('El día no fue encontrado en el calendario.')
        else:
            if self.accion == 'p':
                self.especialidad = self.obtener_especialidad()
                self.cirugia = self.obtener_cirugia()         
                self.num_horas = self.obtener_duracion(self.cirugia, self.especialidad)
                self.codigo = self.obtener_codigo(self.cirugia, self.especialidad)
                self.num_horas = self.num_horas * 2
                self.programar_cita(self.columna_dia, self.num_horas)
            elif self.accion == 'c':
                self.especialidad = self.obtener_horas_cancelar()
                self.cirugia = self.obtener_cirugia()         
                self.num_horas = self.obtener_duracion(self.cirugia, self.especialidad)
                self.especialista = self.database.buscando_especialista(self.cedula)
                self.num_horas = int(self.num_horas * 2)
                self.cancelar_cita(self.columna_dia, self.num_horas)
            elif self.accion == 'o':
                print(f'Horario y disponibilidad para el día {self.dia}:')
                self.observar_disponibilidad(self.columna_dia)
            else:
                print('Accion no reconocida')


    def programar_cita(self, columna_dia, num_horas):
        self.citas_libres = 0
        for fila in self.hoja.iter_rows(min_row=2):
            if fila[columna_dia - 1].value == None:
                self.citas_libres += 1  
        self.nombre = input('Nombre de la persona que programa: ')          
        if self.citas_libres < num_horas:
            print(f'Solo hay {self.citas_libres/2} hora(s) libre(s), se necesitan {num_horas/2} para esta cirugia.')
            print('No hubo cambios en el horario')
            self.database.mostrar_fila(self.cedula)
            return
        self.respuesta_hora = input(f'{self.nombre},¿Desea programar la cita a una hora específica? (sí/no): ')
        if self.respuesta_hora.lower() == 'si':
            self.hora_programar = input('Ingrese la hora de la(s) cita(s) a programar (en formato hh:mm): ')
            self.hora_programar = self.hora_programar.split(':')
            self.hora_programar = [int(parte) for parte in self.hora_programar]
            self.hora_programar_hh, self.hora_programar_mm = self.hora_programar
        else:
            self.hora_programar_hh, self.hora_programar_mm = 0, 0
        self.cont_horas = 0
        self.bandera = False
        self.buscar_especialista = input('Ingrese el especialista que quiere programar: ')
        self.especialista = self.database.obtener_especialista(self.buscar_especialista, self.especialidad)
        while self.especialista == None:
            self.buscar_especialista = input('Ingrese el especialista que quiere programar: ')
            self.especialista = self.database.obtener_especialista(self.buscar_especialista, self.especialidad)            
        for fila in self.hoja.iter_rows(min_row=2):
            if self.cont_horas == num_horas:
                break
            if fila[columna_dia - 1].value != None and self.bandera == False:
                print('Ya hay espacios ocupados, se programara en el primer espacio disponible que se encuentre')
                self.bandera = True
            if fila[columna_dia - 1].value == None:
                self.hora = fila[0].value
                self.hora_hh, self.hora_mm = self.hora.split(' - ')[0].split(':')
                self.hora_hh, self.hora_mm = int(self.hora_hh), int(self.hora_mm)
                if self.hora_hh > self.hora_programar_hh or (self.hora_hh == self.hora_programar_hh and self.hora_mm >= self.hora_programar_mm):
                    fila[columna_dia - 1].value = f'Ocupado-{self.especialidad}-{self.cirugia}-{self.cedula}-{self.especialista}'
                    print(f'Se ha programado la cirugia {self.cirugia} para el día {self.dia} a las {self.hora} para la especialidad {self.especialidad} con {self.especialista}.')
                    self.cont_horas += 1
            self.cambio_quirofano()
            self.cambio_semana()
            self.cambio_dia()
            self.cambio_nombre_especialista(self.especialista)
            self.nombre_programa(self.nombre)
            self.archivo.save('Programa_cirugia_mes1.xlsx')
        self.horas_programadas = (num_horas / 2)
        print(f'{self.horas_programadas} hora(s) programada(s) exitosamente.')
        self.cambio_programado()
        self.close_database()


    def cancelar_cita(self, columna_dia, num_horas):
        self.citas_programadas = 0
        self.horas_ocupadas = []
        for fila in self.hoja.iter_rows(min_row=2):
            if fila[columna_dia - 1].value == f'Ocupado-{self.especialidad}-{self.cirugia}-{self.cedula}-{self.especialista}':
                self.citas_programadas += 1
                self.hora = fila[0].value
                self.horas_ocupadas.append(self.hora)
        if self.citas_programadas == 0:
            print('No hay citas programadas para este día, o el paciente no fue programado este dia.')
            self.database.mostrar_fila(self.cedula)
            return
        self.horas_cancelar = []
        for i in range(num_horas):
            self.hora_cancelar = input(f'Ingrese la hora de la cita {i+1} a cancelar (Ej: 9:00 - 9:30): ')
            if self.hora_cancelar in self.horas_ocupadas:
                self.horas_cancelar.append(self.hora_cancelar)
            else:
                self.hora_cancelar
        self.cont_horas = 0
        for fila in self.hoja.iter_rows(min_row=2):
            if self.cont_horas == num_horas:
                break
            if fila[columna_dia - 1].value != None:
                self.hora = fila[0].value
                if self.hora in self.horas_cancelar and len(self.horas_cancelar) == self.num_horas:
                    fila[columna_dia - 1].value = None
                    print(f'Se ha cancelado la cita para el día {self.dia} a las {self.hora}.')
                    self.cont_horas += 1
            self.archivo.save('Programa_cirugia_mes1.xlsx')
        self.horas_canceladas = (num_horas / 2)
        if self.cont_horas != 0:
            print(f'{self.horas_canceladas} hora(s) cancelada(s) exitosamente.')
            self.cambio_quirofanoP()
            self.cambio_semanaP()
            self.cambio_diaP()
            self.cambio_nombre_especialistaP(self.especialista)
            self.nombre_pendiente()
            self.cambio_pendiente()
        else: 
            print('No hubo cambios en el horario, las horas ingresadas estaban libres o correspondian a otro paciente') 
            self.database.mostrar_fila(self.cedula)
        self.close_database()


    def observar_disponibilidad(self, columna_dia):
        self.contador_disponibles = 0
        for fila in self.hoja.iter_rows(min_row=2, max_row=25):
            self.hora = fila[0].value
            self.estado_celda = fila[columna_dia - 1].value
            if self.estado_celda is None:
                self.contador_disponibles += 1
                print(f'{self.hora}: Disponible')
            else:
                print(f'{self.hora}: {self.estado_celda}')
        self.contador_disponibles = self.contador_disponibles / 2
        self.pendientes = self.database.buscar_pendientes()
        self.database.buscar_combinaciones(self.pendientes, self.contador_disponibles)
        self.close_database()
