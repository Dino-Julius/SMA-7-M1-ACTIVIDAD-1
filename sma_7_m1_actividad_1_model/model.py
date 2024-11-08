'''
Modelo que simula la limpieza de una habitación por un agente reacivo limpiador. 

Autores:
- A01749879 Julio Cesar Vivas Medina
- A01798380 Ulises Jaramillo Portilla

Fecha de creación: 2024-11-07

Fecha de modificación 2024-11-07
'''

import mesa
import random


class Celda:
    '''
    Clase que representa una celda en la habitación. 
    
    Cada celda puede estar sucia o limpia.
    '''

    def __init__(self, sucia=False):
        self.sucia = sucia

    def limpiar(self):
        '''Limpia la celda marcándola como no sucia.'''
        self.sucia = False


class Habitacion:
    '''
    Clase que representa la habitación de MxN con celdas sucias y limpias.
    '''

    def __init__(self, M, N, porcentaje_sucias):
        self.M = M
        self.N = N
        # Genera la habitación con celdas sucias de acuerdo al porcentaje proporcionado.
        self.celdas = [
            [Celda(sucia=(random.random() < porcentaje_sucias))
             for _ in range(N)]
            for _ in range(M)
        ]

    def limpiar_celda(self, x, y):
        '''Limpia la celda en la posición (x, y).'''
        self.celdas[x][y].limpiar()

    def esta_sucia(self, x, y):
        '''Retorna True si la celda en (x, y) está sucia, de lo contrario, False.'''
        return self.celdas[x][y].sucia

    def porcentaje_celdas_limpias(self):
        '''Calcula el porcentaje de celdas limpias en la habitación.'''
        celdas_limpias = sum(
            1 for fila in self.celdas for celda in fila if not celda.sucia
        )
        total_celdas = self.M * self.N
        return (celdas_limpias / total_celdas) * 100

    def contar_celdas_limpias(self):
        '''Cuenta la cantidad de celdas limpias.'''
        return sum(1 for fila in self.celdas for celda in fila if not celda.sucia)

    def contar_celdas_sucias(self):
        '''Cuenta la cantidad de celdas sucias.'''
        return sum(1 for fila in self.celdas for celda in fila if celda.sucia)


class CleaningAgent(mesa.Agent):  # noqa
    """
    Agente que limpia la habitación. Comienza en la celda (0,0).
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Contador de movimientos realizados por el agente.
        self.movimientos = 0
        # Estado del agente: si está limpiando (True) o moviéndose (False).
        self.is_cleaning = False

    def move(self):
        '''
        Mueve al agente a una celda vecina aleatoria.
        '''
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.movimientos += 1

    def clean_cell(self):
        '''
        Limpia la celda en la posición actual del agente si está sucia.
        '''
        x, y = self.pos
        if self.model.habitacion.esta_sucia(x, y):
            self.is_cleaning = True
            self.model.habitacion.limpiar_celda(x, y)
        else:
            self.is_cleaning = False

    def step(self):
        """
        Realiza un paso de acción en la vida del agente:
        - Si la celda está sucia, la limpia.
        - Si la celda está limpia, se mueve aleatoriamente a una celda vecina.
        """
        self.clean_cell()
        if not self.is_cleaning:
            self.move()


class CleaningModel(mesa.Model):
    """
    Modelo de simulación de agentes limpiadores en una habitación de MxN.
    """

    def __init__(self, M, N, num_agents, porcentaje_sucias, tiempo_max):
        super().__init__()
        # Inicialización de la habitación con celdas sucias.
        self.habitacion = Habitacion(M, N, porcentaje_sucias)
        self.num_agents = num_agents
        self.tiempo_max = tiempo_max
        self.tiempo_transcurrido = 0  # Contador de tiempo de simulación.
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width=N, height=M, torus=True)

        # Creación de agentes y asignación a la celda (0,0).
        for i in range(self.num_agents):
            new_agent = CleaningAgent(i, self)
            self.schedule.add(new_agent)
            self.grid.place_agent(new_agent, (0, 0))

        # Inicialización de la recolección de datos.
        self.datacollector = mesa.datacollection.DataCollector(
            model_reporters={
                "Porcentaje Limpio": lambda m: m.habitacion.porcentaje_celdas_limpias(),
                "Movimientos Totales": lambda m: sum(
                    agente.movimientos for agente in m.schedule.agents
                ),
                "Tiempo Transcurrido": lambda m: m.tiempo_transcurrido,
                "Celdas Limpias": lambda m: m.habitacion.contar_celdas_limpias(),
                "Celdas Sucias": lambda m: m.habitacion.contar_celdas_sucias()
            }
        )

        self.running = True  # Bandera de ejecución del modelo.

    def step(self):
        '''
        Realiza un paso en la simulación:
        - Si no se ha alcanzado el tiempo máximo o si todas las celdas no están limpias,
          los agentes actúan y se recopilan datos.
        '''
        if self.tiempo_transcurrido < self.tiempo_max and self.habitacion.porcentaje_celdas_limpias() < 100:
            self.schedule.step()
            self.tiempo_transcurrido += 1
            # Recolección de datos del paso actual.
            self.datacollector.collect(self)
        else:
            # Detiene el modelo si se cumple alguna condición.
            self.running = False

    def get_results(self):
        '''
        Devuelve los resultados finales de la simulación en un diccionario.
        '''
        return self.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
