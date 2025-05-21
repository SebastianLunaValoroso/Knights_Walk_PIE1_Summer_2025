import numpy as np
from math import sqrt
from typing import TypeVar,Any
from yogi import read,scan
import seaborn as sns
import matplotlib.pyplot as plt


T = TypeVar("T", bound=Any)





def valid_square(dim:int,pos:tuple[int,int]|str)->bool:
    """Devuelve True si la casilla de pos existe en la matriz dim x dim.

    Prec:

    :param dim: dim> 0
    """
    if dim <=0: raise ValueError ("dim debe ser > 0")
    if type(pos) is str:
        if len(pos) >2 or pos[0].isdigit() or not(pos[1].isdigit()): raise ValueError ("Si pos es un string debe tener 2 carácteres, el primero una letra y el segundo un dígito")
        return 1 <= int(pos[1]) <= dim and "a" <= pos[0] <="h" #comparamos int(pos[1]) con 1 y dim y no 0 y dim-1 porque se empieza a contar desde el 1 si pos es un string
    return (type(pos)==tuple and len(pos)==2) and 0<=pos[0]<= dim-1 and 0<=pos[1]<= dim-1
        


def chess_pos_to_matrix(chess_pos:str,dim:int)->tuple[int,int]:
    """Devuelve los indices de la matriz del board row,column al que corresponde chess_pos.

    Prec:

    :param chess_pos:
        Formato 'columnrow' column es una letra (la primera letra es a) y row un entero (contando desde el 1)\n
        La casilla debe existir en el tablero dim x dim 
    :param dim: dim> 0 
    """
    if dim <=0: raise ValueError ("dim debe ser > 0")
    if not(valid_square(dim,chess_pos)): raise ValueError (f'{chess_pos} no existe en el tablero de dimensión {dim}x{dim}')
    row:dict[str,int]={f'{i+1}':i for i in range(dim)}
    column:dict[str,int]={chr(ord("a")+i):i for i in range(dim)}
    return (row[chess_pos[1]],column[chess_pos[0]])

def uniform_selection(lista:list[T])->T|None:
    """Escoge y Devuelve un elemento de lista de manera uniforme U(n), si lista no está vacía"""
    #np.random.seed(13) #dev quitar----------------------------------------------------------------------------------------------------------------
    n=len(lista) #número de elementos de lista
    if n==0:
        return None
    prob=np.random.uniform(0,1)
    for i in range(n):
        if i/n <=prob <=(i+1)/n:
            return lista[i]
    return None #para que MyPy no dé errores



class Knight_Board:
    """Clase para representar el tablero de ajedrez con los movimientos del Knight"""

    _matrix:list[list[int]]
    _knight_pos:tuple[int,int]
    _torus:bool

    def __init__(self,pos:str,squares:int,torus:bool=False,occupied_pos:list[str]=[])->None:
        """Constructor del Knight_Board"""
        dimension:int=int(sqrt(squares))
        if dimension <=0: raise ValueError ("squares debe ser > 0")
        self._matrix=[[0 for _ in range(dimension)] for _ in range(dimension)]
        self._knight_pos=chess_pos_to_matrix(pos,dimension)
        self._matrix[self._knight_pos[0]][self._knight_pos[1]]=1
        self._torus=torus
        for chess_pos in occupied_pos:
            posicion:tuple[int,int]=chess_pos_to_matrix(chess_pos,dimension)
            if self._matrix[posicion[0]][posicion[1]] !=0: raise ValueError (f"La casilla en {chess_pos} ya estaba ocupada.")
            self._matrix[posicion[0]][posicion[1]]=-1
    
    def knight_pos(self)->tuple[int,int]:
        """Devuelve una copia de la posición del knight"""
        return (self._knight_pos[0],self._knight_pos[1])
    
    def matrix(self)->list[list[int]]:
        """Devuelve la matriz del tablero"""
        return self._matrix #no es una copia
    
    def is_torus(self)->bool:
        """Devuelve si el tablero es Torus"""
        return self._torus

    def board_dimension(self)->int:
        """Devuelve la dimensión del tablero
        Ejemplo: si un tablero es n x n, devuelve n"""
        return len(self.matrix())
    
    def valid_destination(self,dim:int,dest:tuple[int,int])->bool:
        """Devuelve True si la casilla dest existe en la matriz dim x dim del tablero y está vacía"""
        #return valid_square(dim,dest) and self.matrix()[dest[0]][dest[1]] == 0
        return valid_square(dim, dest) and self.matrix()[dest[0]][dest[1]] != -1

    
    def jump_destination(self,origin:tuple[int,int],jump:tuple[int,int])->tuple[int,int]:
        """Devuelve la casilla de destino de jump aplicado a origin"""
        dim:int=self.board_dimension()
        dest=(origin[0]+jump[0],origin[1]+jump[1])
        if not(self.is_torus()) or valid_square(dim,dest):
            return dest
        #Aquí el tablero es Torus y el destino no es una casilla existente, hay que convertirlo
        if dest[0]<0:
            dest=(dest[0]+dim,dest[1])
        elif dest[0] >0:
            dest=(dest[0]-dim,dest[1])
        if dest[1] < 0:
            dest=(dest[0], dest[1]+dim)
        elif dest[0] >0:
            dest= (dest[0],dest[1]-dim)
        return dest
    
    def generate_knight_moves(self)->list[tuple[int,int]]:
        """Devuelve las posiciones de destino posibles"""
        moves:list[tuple[int,int]]=[]
        saltos:list[tuple[int,int]]=[(-1,-2),(-1,2),(1,-2),(1,2),(-2,-1),(2,-1),(-2,1),(2,1)] #saltos posibles del caballo
        for salto in saltos:
            dest=self.jump_destination(self.knight_pos(),salto)
            if self.valid_destination(self.board_dimension(),dest):
                moves.append(dest)
        return moves
    
    def play_jump(self, moves: list[tuple[int, int]]) -> None:
        """Escoge y aplica uno de los moves aleatoriamente siguiendo U(n), con n el número de moves"""
        move = uniform_selection(moves)
        if move is not None:
            self.matrix()[move[0]][move[1]] += 1  # Acumula una visita
            self._knight_pos = move

    
    def next(self)->tuple[int,int]:
        """Realiza el siguiente movimiento del Knight y devuelve su nueva posición"""
        self.play_jump(self.generate_knight_moves())
        return self.knight_pos()
    



def main_inputs()->tuple[int,str,int,bool,list[str]]:
    """Permite seleccionar los parámetros inciales de entrada y los devuelve"""

    print("Choose the board's squares (it will create an sqrt(squares) x sqrt(squares) board, write -1 to leave default squares=64):")
    squares=read(int)
    if squares<=-1:squares=64
    print(f'{squares} selected!')

    print("Choose the knight's initial position (format: columnrow, write -1 to leave default position 'b1'):")
    ches_pos=read(str)
    if ches_pos=="-1":ches_pos="b1"
    print(f'{ches_pos} position selected!')

    print("Choose the knight's steps (write -1 to leave the default steps=10):")
    steps=read(int)
    if steps<=-1:steps=10
    print(f'{steps} steps selected!')

    print("Choose whether the chess board should be a torus: (format: T for True, F for False, write -1 to leave the default option torus=False):")
    torus_str=read(str)
    if torus_str=="-1" or torus_str=="F":torus=False
    else: torus=True
    print(f'torus={torus} selected!')

    print("Add other pieces position's (to stop input enter Ctr+D Linux/macOS or Ctr+Z Windows):")
    occupied_pos:list[str]=[]
    piece_pos=scan(str)
    while piece_pos is not None:
        occupied_pos.append(piece_pos)
        piece_pos=scan(str)
    print(f'{occupied_pos} positions selected!')

    return (squares,ches_pos,steps,torus,occupied_pos)

def plot_board(board: Knight_Board, title: str = "Knight's Visit Frequency") -> None:
    """Grafica un heatmap del tablero con las frecuencias de visita"""
    matrix = np.array(board.matrix())
    flipped_matrix = np.flipud(matrix)  # Para que la fila 0 esté abajo como en un tablero de ajedrez

    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(flipped_matrix, annot=True, fmt="d", cmap="Blues", cbar=True, linewidths=.5, square=True)

    dim = board.board_dimension()
    ax.set_title(title)
    ax.set_xlabel("Columnas (a-h)")
    ax.set_ylabel("Filas (1-8)")

    # Etiquetas de las columnas (letras a-h, o más si el tablero es más grande)
    col_labels = [chr(ord("a") + i) for i in range(dim)]
    row_labels = list(range(1, dim + 1))[::-1]  # Invertido por flipud
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels, rotation=0)

    knight_row, knight_col = board.knight_pos()
    flipped_row = dim - 1 - knight_row  # Ajustar por el flipud

    # Dibujar una ♞ roja en la celda final
    ax.text(knight_col + 0.5, flipped_row + 0.5, '♞', 
            ha='center', va='center', color='red', fontsize=18, fontweight='bold')

    plt.tight_layout()
    plt.show()

def main()->None:
    #Inputs Iniciales
    squares,chess_pos,steps,torus,occupied_pos=main_inputs()
    tablero=Knight_Board(chess_pos,squares,torus,occupied_pos)
    print(tablero)
    print(f'pos_inicial:{tablero.knight_pos()}')
    for i in range(steps):
        print(f'pos_paso_{i+1}:{tablero.next()}')
    print(f'frecuencias de visita del caballo:')
    plot_board(tablero)

main()