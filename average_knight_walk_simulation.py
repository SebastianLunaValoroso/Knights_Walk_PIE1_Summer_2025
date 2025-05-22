import numpy as np
from math import sqrt
from typing import TypeVar,Any
from yogi import read,scan
import seaborn as sns
import matplotlib.pyplot as plt
from knight_walk_simulation import main_inputs, Knight_Board, write_knight_walk

#Este programa está diseñado para hacer una media de varios caminos hechos por el Caballo
#Si su intención es sólo realizar 1 camino utilice knight_walk_simulation.py




def plot_average_board(matrix:np.ndarray,reps:int, title: str = "Knight's Average Visit Frequency") -> None:
    """Dibuja un heatmap del tablero con la media de las frecuencias de visita"""
    matrix = (1/reps)* matrix #matriz con las medias
    flipped_matrix = np.flipud(matrix)  # Para que la fila 0 esté abajo como en un tablero de ajedrez

    plt.figure(figsize=(8, 6))
    dim = len(matrix)
    if dim >=25: # ¿and reps >=15:?
        ax = sns.heatmap(flipped_matrix, fmt=".2f", cmap="Blues", cbar=True, linewidths=.5, square=True)
    else:
        ax = sns.heatmap(flipped_matrix, annot=True, fmt=".2f", cmap="Blues", cbar=True, linewidths=.5, square=True)

    
    ax.set_title(title)
    if dim+97 > 122: ending=chr(165+dim)
    else: ending=chr(dim+96)
    ax.set_xlabel(f"Columnas (a-{ending})")
    ax.set_ylabel(f"Filas (1-{dim})")

    # Aumenta el limite de labels en función de las dimensiones  del board
    ax.set_xticks(np.arange(dim) + 0.5)
    ax.set_yticks(np.arange(dim) + 0.5)

    # Etiquetas de las columnas (letras a-h, o más si el tablero es más grande)
    col_labels =(chr(i) if i <= 122 else chr(69+i) for i in range(97,dim+97)) #utiliza las letras de a-z y si hay más labels continua desde el carácter Unicode À
    row_labels=(f'{i}' for i in range(dim,0,-1))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels, rotation=0)

    plt.tight_layout()
    plt.show()


def main_average_inputs()->tuple[int,str,int,bool,list[str],int]:
    """Permite seleccionar los parámetros inciales de entrada y los devuelve"""
    print("Choose the number of times you want to repeat the walk (a higher number creates a better average walk, write -1 to leave default reps=10):")
    reps=read(int)
    if reps<=-1:reps=10
    print(f'{reps} reps selected!')
    squares,chess_pos,steps,torus,occupied_pos=main_inputs()
    return (squares,chess_pos,steps,torus,occupied_pos,reps)

def main()->None:
    squares,chess_pos,steps,torus,occupied_pos,reps=main_average_inputs()
    dim=int(sqrt(squares))
    accumulator_matrix=np.zeros([dim,dim],int) #creates a dim x dim matrix of 0's
    for i in range(reps):
        tablero=Knight_Board(chess_pos,squares,torus,occupied_pos)
        print(f"Camino_{i}:")
        write_knight_walk(tablero,steps)
        accumulator_matrix=accumulator_matrix + np.array(tablero.matrix())
    print(f"Drawing Knight's Average Visit Frequency plot...")
    plot_average_board(accumulator_matrix,reps,f"Knight's Average Visit Frequency for {steps} steps starting at {chess_pos}")

if __name__=="__main__":
    main()