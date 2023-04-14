import pymysql


class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Qwertyuiop12',
            db='bd_cirugia'
        )

        self.cursor = self.connection.cursor()

    def select_especialidad(self, cedula):
        sql = f'SELECT especialidad FROM Programacion WHERE numero_identificacion = "{cedula}"'.format(cedula=cedula)
        self.cursor.execute(sql)
        especialidad = self.cursor.fetchone()
        if especialidad is None:
            print('El paciente no fue encontrado revise la cedula ingresada')
            self.close()
            exit() 
        else:
            print('Especialidad: ', especialidad[0])
            return especialidad[0]
    

    def revisar_estado(self, cedula):
        sql = f'SELECT estado_programacion FROM Programacion WHERE numero_identificacion = "{cedula}"'.format(cedula=cedula)
        self.cursor.execute(sql)
        estado = self.cursor.fetchone()
        if estado is None:
            print('El paciente no fue encontrado revise la cedula ingresada')
            self.close()
            exit() 
        else:
            return estado[0]


    def select_cirugia(self, cedula):
        sql = f'SELECT nombre_prestacion FROM Programacion WHERE numero_identificacion = "{cedula}"'.format(cedula=cedula)
        self.cursor.execute(sql)
        cirugia = self.cursor.fetchone()
        print('Cirugia: ', cirugia[0])
        return cirugia[0]


    def select_duracion(self, cirugia, especialidad):
        sql = f'SELECT duracion FROM {especialidad} WHERE nombre = "{cirugia}"'.format(cirugia=cirugia)
        self.cursor.execute(sql)
        duracion = self.cursor.fetchone()
        print('Duracion: ', duracion[0], 'horas')
        return duracion[0]
    

    def select_codigo(self, cirugia, especialidad):
        sql = f'SELECT codigo FROM {especialidad} WHERE nombre = "{cirugia}"'.format(cirugia=cirugia)
        self.cursor.execute(sql)
        codigo = self.cursor.fetchone()
        print('Codigo: ', codigo[0])
        return codigo[0]
    

    def obtener_especialista(self, especialista, especialidad):
        sql = f"SELECT nombre_medico FROM medico WHERE especialidad_medico = '{especialidad}' AND nombre_medico = '{especialista}'"
        self.cursor.execute(sql)
        especialista = self.cursor.fetchone()
        if especialista == None:
            return(especialista)
        else: return especialista[0]
    

    def buscando_especialista(self, cedula):
        sql = f"SELECT especialista FROM Programacion WHERE numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        especialista = self.cursor.fetchone()
        return especialista[0]

    def actualizar_especialista(self, cedula, especialista):
        sql = f"UPDATE Programacion SET especialista = '{especialista}' WHERE especialista IS NULL AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_especialistaP(self, cedula, especialista):
        sql = f"UPDATE Programacion SET especialista = NULL WHERE especialista = '{especialista}' AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_nombre(self, cedula, nombre):
        sql = f"UPDATE Programacion SET nombre_persona_que_programa = '{nombre}' WHERE nombre_persona_que_programa IS NULL AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_programado(self, cedula):
        estadoP = 'Programado'
        sql = f"UPDATE Programacion SET estado_programacion = '{estadoP}' WHERE estado_programacion = 'Pendiente' AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()

    
    def actualizar_quirofano(self, cedula, quirofano):
        sql = f"UPDATE Programacion SET quirofano_cirugia = '{quirofano}' WHERE quirofano_cirugia IS NULL AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_semana(self, cedula, semana):
        sql = f"UPDATE Programacion SET semana_cirugia = '{semana}' WHERE semana_cirugia IS NULL AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_dia(self, cedula, dia):
        sql = f"UPDATE Programacion SET dia_cirugia = '{dia}' WHERE dia_cirugia IS NULL AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_pendiente(self, cedula):
        estadoP = 'Pendiente'
        sql = f"UPDATE Programacion SET estado_programacion = '{estadoP}' WHERE estado_programacion = 'Programado' AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_quirofanoP(self, cedula, quirofano):
        sql = f"UPDATE Programacion SET quirofano_cirugia = NULL WHERE quirofano_cirugia = '{quirofano}' AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_semanaP(self, cedula, semana):
        sql = f"UPDATE Programacion SET semana_cirugia = NULL WHERE semana_cirugia = '{semana}' AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_diaP(self, cedula, dia):
        sql = f"UPDATE Programacion SET dia_cirugia = NULL WHERE dia_cirugia = '{dia}' AND numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()


    def actualizar_nombreP(self, cedula):
        sql = f"UPDATE Programacion SET nombre_persona_que_programa = NULL WHERE numero_identificacion = '{cedula}'"
        self.cursor.execute(sql)
        self.connection.commit()

        
    def mostrar_fila(self, cedula):
        sql = f"SELECT * FROM Programacion WHERE numero_identificacion = {cedula}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print(result)


    def buscar_pendientes(self):
        sql = f"SELECT numero_identificacion , nombre_prestacion, especialidad FROM Programacion WHERE estado_programacion = 'pendiente'"
        self.cursor.execute(sql)
        cirugias_pendientes = self.cursor.fetchall()
        cirugias_dict = {}
        for cirugia in cirugias_pendientes:
            id_fila = cirugia[0]
            nombre_cirugia = cirugia[1]
            especialidad = cirugia[2]
            sql = f"SELECT duracion FROM {especialidad} WHERE nombre = %s"
            self.cursor.execute(sql, (nombre_cirugia,))
            duracion = self.cursor.fetchone()[0]
            cirugias_dict[nombre_cirugia] = {"duracion": duracion, "cedula": id_fila}
        return cirugias_dict

    
    def buscar_combinaciones(self, cirugias, horas_disponibles):
        combinaciones = []
        combinacion_actual = []
        def backtrack(cirugias, horas_disponibles, combinacion_actual):
            if sum([c['duracion'] for c in combinacion_actual]) == horas_disponibles:
                combinaciones.append([(c['nombre'], c['duracion'], c['cedula']) for c in combinacion_actual])
                return
            elif sum([c['duracion'] for c in combinacion_actual]) > horas_disponibles:
                return
            for nombre, cirugia in cirugias.items():
                if nombre not in [c['nombre'] for c in combinacion_actual]:
                    combinacion_actual.append({'nombre': nombre, 'duracion': cirugia['duracion'], 'cedula': cirugia['cedula']})
                    backtrack(cirugias, horas_disponibles, combinacion_actual)
                    combinacion_actual.pop()
        backtrack(cirugias, horas_disponibles, combinacion_actual)
        horas_disponibles = int(horas_disponibles)
        if (len(combinaciones)) >= 1:
            print(f'Hay {horas_disponibles} horas disponibles y estas son las posibles combinaciones en las que puede programar las cirugias pendientes para optimizar todo el tiempo:')
            print()
            for combinacion in combinaciones:
                print(combinacion)
                print()
        else: print(f'No hay combinaciones para optimizar todo el tiempo, ya que hay mas horas disponibles que horas de cirugia para programar.')

####### Para visualizar datos############

    def ver_datos(self):
        sql = f"SELECT * FROM  Programacion "
        self.cursor.execute(sql)
        ver_datos = self.cursor.fetchall()
        for fila in ver_datos:
            print(fila)

    def agrupar_especialidad(self, especialidad):
        sql = f"SELECT * FROM  Programacion WHERE especialidad = '{especialidad}'"
        self.cursor.execute(sql)
        agrupando_especialidad = self.cursor.fetchall()
        for fila in agrupando_especialidad:
            print(fila)
        return agrupando_especialidad

    
    def agrupar_especialidad_estado(self, especialidad, estado):
        sql = f"SELECT * FROM  Programacion WHERE especialidad = '{especialidad}' AND estado_programacion = '{estado}'"
        self.cursor.execute(sql)
        agrupando_especialidad_estado = self.cursor.fetchall()
        for fila in agrupando_especialidad_estado:
            print(fila)
        return agrupando_especialidad_estado
    

    def contar_pacientes(self, especialidad, estado):
        sql = f"SELECT COUNT(*) AS total_programados FROM Programacion WHERE estado_programacion = '{estado}' AND especialidad = '{especialidad}'"
        self.cursor.execute(sql)
        cuenta = self.cursor.fetchone()
        print(f'El total de pacientes de la especialidad Anestesiologia con estado {estado} es: ', cuenta[0])


    def estados(self, estado):
        sql = f"SELECT COUNT(*) AS total_programados FROM Programacion WHERE estado_programacion = '{estado}'"
        self.cursor.execute(sql)
        cuenta = self.cursor.fetchone()
        print(f'El total de pacientes con estado {estado} es: ', cuenta[0])
        return cuenta[0]
    

    def ver_por_estados(self, estado):
        sql = f"SELECT * FROM  Programacion WHERE estado_programacion = '{estado}'"
        self.cursor.execute(sql)
        estados = self.cursor.fetchall()
        for fila in estados:
            print(fila)


    def close(self):
        self.connection.close()
