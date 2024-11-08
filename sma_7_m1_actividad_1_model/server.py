"""
Configura los elementos de visualización e instancia un servidor para la simulación de agentes de limpieza,
incluyendo la visualización de datos recolectados.
"""

from .model import CleaningModel  # Importa el modelo de limpieza
import mesa

# Función de representación del agente en la visualización


def agent_portrayal(agent):
    """
    Define cómo se verá un agente en la visualización.
    - Si el agente está limpiando, se muestra en rojo.
    - Si el agente no está limpiando, se muestra en verde.
    """
    if agent is None:
        return

    # Configuración visual del agente
    portrayal = {"Shape": "circle", "Filled": "true", "r": 1}

    # Color y capa del agente basado en su estado
    if agent.is_cleaning:  # Verifica si el agente está limpiando
        portrayal["Color"] = "red"  # Rojo si está limpiando
        portrayal["Layer"] = 0
        portrayal["r"] = 1  # Radio más grande para indicar acción de limpieza
    else:
        portrayal["Color"] = "green"  # Verde si no está limpiando
        portrayal["Layer"] = 1
        portrayal["r"] = 1  # Radio estándar cuando no está limpiando

    return portrayal


# Configuración de la cuadrícula para la visualización de agentes y la habitación
grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Gráfico para visualizar el porcentaje de celdas limpias en cada paso
chart_porcentaje_limpio = mesa.visualization.ChartModule(
    [{"Label": "Porcentaje Limpio", "Color": "Black"}],
    data_collector_name="datacollector"
)

# Gráfico para visualizar el número total de movimientos realizados por los agentes en cada paso
chart_movimientos_totales = mesa.visualization.ChartModule(
    [{"Label": "Movimientos Totales", "Color": "Blue"}],
    data_collector_name="datacollector"
)

# Gráfico para visualizar el tiempo transcurrido en la simulación
chart_tiempo_transcurrido = mesa.visualization.ChartModule(
    [{"Label": "Tiempo Transcurrido", "Color": "Red"}],
    data_collector_name="datacollector"
)

# Gráfico comparativo de celdas limpias frente a sucias
chart_limpias_vs_sucias = mesa.visualization.ChartModule(
    [
        {"Label": "Celdas Limpias", "Color": "Green"},
        {"Label": "Celdas Sucias", "Color": "Brown"},
    ],
    data_collector_name="datacollector"
)

# Elemento de texto para mostrar estadísticas generales de la simulación


class SimulationDataElement(mesa.visualization.TextElement):
    """
    Elemento de texto para mostrar:
    - El porcentaje de limpieza alcanzado
    - El número de celdas sucias restantes frente al número de celdas limpias
    - El tiempo necesario para limpiar todas las celdas (o hasta el límite de tiempo)
    - El número total de movimientos realizados por todos los agentes
    """

    def render(self, model):
        # Obtiene los datos recolectados del modelo
        porcentaje_limpio = model.habitacion.porcentaje_celdas_limpias()
        movimientos_totales = sum(
            agent.movimientos for agent in model.schedule.agents
        )
        tiempo_transcurrido = model.tiempo_transcurrido
        tiempo_maximo = model.tiempo_max

        # Calcular celdas sucias restantes y celdas limpias
        celdas_sucias_restantes = model.habitacion.contar_celdas_sucias()
        celdas_limpias = model.habitacion.contar_celdas_limpias()

        return f"<b>Estadísticas de Simulación:</b><br>" \
            f"Porcentaje Limpio: {porcentaje_limpio:.2f}%<br>" \
            f"Celdas Sucias/Limpias: {celdas_sucias_restantes}/{celdas_limpias}<br>" \
            f"Movimientos Totales: {movimientos_totales}<br>" \
            f"Tiempo Transcurrido: {tiempo_transcurrido}/{tiempo_maximo}<br>"


# Parámetros del modelo de limpieza
model_kwargs = {
    "M": 10,  # Número de filas de la habitación
    "N": 10,  # Número de columnas de la habitación
    "num_agents": 10,  # Número de agentes de limpieza
    # Porcentaje inicial de celdas sucias (como decimal)
    "porcentaje_sucias": 0.5,
    "tiempo_max": 20  # Tiempo máximo de ejecución
}

# Configuración del servidor para la simulación
server = mesa.visualization.ModularServer(
    CleaningModel,
    [
        grid,
        chart_porcentaje_limpio,
        chart_movimientos_totales,
        chart_tiempo_transcurrido,
        chart_limpias_vs_sucias,
        SimulationDataElement()  # Incluye todos los elementos de visualización
    ],
    "Simulación de Agentes de Limpieza - Equipo 7",
    model_kwargs,
)
