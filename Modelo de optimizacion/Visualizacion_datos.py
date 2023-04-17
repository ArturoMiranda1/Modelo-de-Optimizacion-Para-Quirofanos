from Data_Base import*


class VisualizacionDatos(DataBase):
    def __init__(self):
        super().__init__()
        self.database = DataBase()


    def close_database(self):
        self.database.close()


    def accion(self):
        print('Opciones de visualizacion:\n 1.Ver todos los pacientes.\n 2.Filtrar por especialidad.\n 3.Filtrar solo por estado.')
        self.accion = input('Ingrese el numero de la accion que quiere hacer: ')
        while self.accion != '1' and self.accion != '2' and self.accion != '3':
            print('Ingrese una respuesta valida: ')
            self.accion = input('Ingrese el numero de la accion que quiere hacer: ')
        if self.accion == '1':
            self.ver_datos()
        elif self.accion == '2':
            self.agrupar_por_especialidad()
        elif self.accion == '3':
            self.observar_pendientes_programados()


    def ver_datos(self):
        self.database.ver_datos()


    def agrupar_por_especialidad(self):
        self.especialidad = input('Ingrese la especialidad por la que quiere filtrar: ')
        self.lista = self.database.agrupar_especialidad(self.especialidad)
        while not self.lista:
            print('Entrada incorrecta')
            self.especialidad = input('Ingrese la especialidad por la que quiere filtrar: ')
            self.lista = self.database.agrupar_especialidad(self.especialidad)
        self.agrupar_estado = input('Quiere filtrar tambien por estado?(s/n): ')
        while self.agrupar_estado.lower() != 's' and self.agrupar_estado.lower() != 'n':
            print('Entrada incorrecta')
            self.agrupar_estado = input('Quiere filtrar tambien por estado?(s/n): ')
        if self.agrupar_estado.lower() == 's':
            self.agrupar_especialidad_estado(self.especialidad)
        elif self.agrupar_estado.lower() == 'n':
            self.close_database()


    def agrupar_especialidad_estado(self, especialidad):
        self.estado = input('Quiere ver Programado o Pendiente: ')
        while self.estado != 'Programado' and self.estado != 'Pendiente':
            print('Entrada incorrecta')
            self.estado = input('Quiere ver Programado o Pendiente: ')
        self.especialidad_estado = self.database.agrupar_especialidad_estado(especialidad, self.estado)
        self.database.contar_pacientes(self.especialidad, self.estado)
        if not self.especialidad_estado:
            print('No hay cirugias que cumplan la condicion')
        self.close_database()


    def observar_pendientes_programados(self):
        self.estado_todos = input('Quiere ver todos los pacientes con estado Programado o Pendiente: ')
        while self.estado_todos != 'Programado' and self.estado_todos != 'Pendiente':
            print('Entrada incorrecta')
            self.estado_todos = input('Quiere ver todos los pacientes con estado Programado o Pendiente: ')
        if self.estado_todos == 'Programado':
            self.cuenta_programados = self.database.estados(self.estado_todos)
            if self.cuenta_programados == 0:
                print('No hay pacientes con estado Programado para mostrar.')
            else:
                self.database.ver_por_estados(self.estado_todos)  
        if self.estado_todos == 'Pendiente':
            self.cuenta_pendientes = self.database.estados(self.estado_todos)
            if self.cuenta_pendientes == 0:
                print('No hay pacientes con estado Pendiente para mostrar.')
            else:
                self.database.ver_por_estados(self.estado_todos)       
        self.close_database()


nueva_viualizacion = VisualizacionDatos()
nueva_viualizacion.accion()