SMA-7-M1-Actividad-1: Simulación de un Robot de Limpieza
========================


Este proyecto estudia el comportamiento y eficiencia de un robot de limpieza reactivo en una habitación de tamaño $M \times N$, evaluando cómo el número de agentes influye en el rendimiento de la limpieza. La simulación considera una cantidad inicial de celdas sucias distribuidas aleatoriamente y un número máximo de pasos que cada agente puede ejecutar.

SMA-7: [Ulises Jaramillo](https://github.com/Ulises-JPx) & [Julio Vivas](https://github.com/Dino-Julius).

## Índice

1. [Instrucciones de Simulación](#instrucciones-de-simulación)
2. [Datos Recopilados](#datos-recopilados)
3. [Análisis Realizado](#análisis-realizado)
4. [Descargar y Ejecutar el Proyecto](#descargar-y-ejecutar-el-proyecto)

## Instrucciones de Simulación:

1. **Inicialización**: La simulación comienza con las celdas sucias distribuidas aleatoriamente y todos los agentes colocados en la celda inicial $[1,1]$.
2. **Dinámica de Movimiento**: En cada paso de tiempo:
   - Si el agente está en una celda sucia, la limpia.
   - Si la celda está limpia, el agente selecciona una dirección aleatoria para moverse a una de las 8 celdas vecinas (permaneciendo en la misma si no es posible moverse).
3. **Término de Simulación**: La simulación se detiene al alcanzar el tiempo máximo definido o cuando todas las celdas están limpias.

## Datos Recopilados:

- **Tiempo para limpiar todas las celdas** (o hasta alcanzar el límite de tiempo).
- **Porcentaje de celdas limpias** al finalizar la simulación.
- **Total de movimientos realizados** por todos los agentes.

## Análisis Realizado:

El informe en PDF documenta el impacto de la cantidad de agentes sobre el tiempo de limpieza y los movimientos realizados, destacando cómo la eficiencia cambia con diferentes configuraciones.

## Descargar y Ejecutar el Proyecto:

Para descargar y ejecutar el proyecto, sigue estos pasos:

1. Clona el repositorio:
    ```sh
    git clone https://github.com/Dino-Julius/SMA-7-M1-ACTIVIDAD-1.git
    ```

2. Navega al directorio del proyecto:
    ```sh
    cd sma-7-m1-actividad-1
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Ejecuta la simulación:
    ```sh
    python run.py
    ```

Esto iniciará el servidor y podrás visualizar la simulación en tu navegador web.