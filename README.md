# Knights Walk PIE1 Summer 2025 por Unai Lema y Sebastián Luna
Este proyecto explora una variante de un antiguo problema matemático sobre los posibles caminos aleatorios que la figura del caballo ♞ puede realizar en un tablero de Ajedrez. 

## Objetivos
- **Modelar** los caminos que puede hacer un caballo en un tablero de Ajedrez.
- **Evaluar** si existe una distribución estacionaria sobre las casillas en las que se mueve el caballo.

## Herramientas Utilizadas

- Lenguajes de programación: Python
- Librerías Externas: numpy, yogi, seaborn
- Visualización: matplotlib
- Entorno Virtual: pixi

## Programas

### knight_walk_simulation.py
Permite generar un camino aleatorio para la figura del Caballo en un tablero de Ajedrez. Escribe el camino en la consola de ejecución y después dibuja un heapmap que muestra las casillas más visitadas del tablero durante el camino. Utiliza como parámetros:
- el número de casillas del tablero
- la posición inicial del Caballo
- el número de saltos que hará el caballo
- convertir el tablero a Torus o no
- las piezas en otras posiciones

### average_knight_walk_simulation.py
Permite generar una media de las casillas más visitadas del tablero de Ajedrez por el caballo con un camino de ciertas características. Escribe todos los caminos que genera en la consola de ejecución y después dibuja un heapmap que muestra las casillas más visitadas del tablero durante todos los caminos. Utiliza como parámetros:
- el número de caminos a generar (para calcular la media, cuánto más caminos más precisión y más tardará el programa en responder)
- el número de casillas del tablero
- la posición inicial del Caballo
- el número de saltos que hará el caballo
- convertir el tablero a Torus o no
- las piezas en otras posiciones

---
