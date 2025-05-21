import numpy as np
from math import sqrt
from typing import TypeVar,Any
from yogi import read,scan

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
    row:int=int(chess_pos[1]) -1
    column:int= ord(chess_pos[0])-ord("a")
    return (row,column)

def matrix_to_chess_pos(pos:tuple[int,int],dim:int)->str:
    """Devuelve el indice de la casilla en formato 'columnrow' que correponde a los indices de la matriz del board.

    Prec:

    :param pos:
        Formato (row,column), row y column son enteros\n
        La casilla debe existir en el tablero dim x dim 
    :param dim: dim> 0 
    """
    if dim <=0: raise ValueError ("dim debe ser > 0")
    if not(valid_square(dim,pos)): raise ValueError (f'{pos} no existe en el tablero de dimensión {dim}x{dim}')
    row:str=f'{pos[0]+1}'
    column:str=chr(ord("a")+pos[1])
    return column+row



def uniform_selection(lista:list[T],semilla:int|None=None)->T|None:
    """Escoge y Devuelve un elemento de lista de manera uniforme U(n), si lista no está vacía"""
    if semilla is not None:
        np.random.seed(semilla) #para debug o juegos de test
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
        return valid_square(dim,dest) and self.matrix()[dest[0]][dest[1]] == 0
    
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
    
    def play_jump(self,moves:list[tuple[int,int]])->None:
        """Escoge y Aplica uno de los move de moves aleatoriamente siguiendo U(n), con n el número de moves"""
        move=uniform_selection(moves)
        if move is not None:
            knight_pos=self.knight_pos()
            self.matrix()[knight_pos[0]][knight_pos[1]]-=1 #se retira el caballo de la posición de origen
            self.matrix()[move[0]][move[1]]+=1 #se añade el caballo a la posición de destino
            self._knight_pos=move
    
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

    print('',end="\n\n\n") #saltos de línea

    return (squares,ches_pos,steps,torus,occupied_pos)


def main()->None:
    #Inputs Iniciales
    squares,chess_pos,steps,torus,occupied_pos=main_inputs()
    tablero=Knight_Board(chess_pos,squares,torus,occupied_pos)
    print(f'pos_inicial:{tablero.knight_pos()}')
    for i in range(steps):
        print(f'pos_paso_{i+1}:{tablero.next()}')
    
if __name__=="__main__":
    main()