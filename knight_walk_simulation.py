import numpy as np
from math import sqrt

def valid_square(dim:int,pos:tuple[int,int]|str)->bool:
    """Devuelve True si la casilla de pos existe en la matriz dim x dim"""
    if type(pos) is str:
        if len(pos) >2 or pos[0].isdigit() or not(pos[1].isdigit()): raise ValueError ("Si pos es un string debe tener 2 carácteres, el primero una letra y el segundo un dígito")
        return 1 <= int(pos[1]) <= dim and "a" <= pos[0] <="h" #en compramos int(pos[1]) con 1 y dim y no 0 y dim-1 porque se empieza a contar desde el 1 si pos es un string
    return type(pos) is tuple[int,int] and 0<=pos[0]<= dim-1 and 0<=pos[1]<= dim-1
        


def chess_pos_to_matrix(chess_pos:str,dim:int)->tuple[int,int]:
    """Devuelve los indices de la matriz del board row,column al que corresponde chess_pos
    Prec: chess_poss debes existir"""
    if not(valid_square(dim,chess_pos)): raise ValueError (f'{chess_pos} no existe en el tablero de dimensión {dim}x{dim}')
    row:dict[str,int]={f'{i+1}':i for i in range(dim)}
    column:dict[str,int]={chr(ord("a")+i):i for i in range(dim)}
    return (row[chess_pos[1]],column[chess_pos[0]])






def main()->None:
    xt=np.random.uniform(0,1,10) # o numpy.random.randint(low, high=None, size=None, dtype='l') Returns random integers from the “discrete uniform” distribution
    print(xt)


main()