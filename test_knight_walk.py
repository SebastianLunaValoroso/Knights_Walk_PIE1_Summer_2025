import pytest
import numpy as np
from math import sqrt
from knight_walk_simulation import valid_square, matrix_to_chess_pos, chess_pos_to_matrix


def test_valid_square()->None:
    """Comprueba si valid_square() funciona"""
    assert valid_square(8,"b1")
    assert not(valid_square(8,"j1"))
    assert valid_square(4,"b1")
    with pytest.raises(ValueError):
        valid_square(8,"11")
    with pytest.raises(ValueError):
        valid_square(8,"1b")
    with pytest.raises(ValueError):
        valid_square(0,"b1")
    #añadir casos con tuple[int,int]


def test_matrix_to_chess_pos()->None:
    """Comprueba si matrix_to_chess_pos() funciona"""
    assert matrix_to_chess_pos((0,1),8) == "b1"
    assert matrix_to_chess_pos((0,0),8) == "a1"
    assert matrix_to_chess_pos((0,7),8) == "h1"
    assert matrix_to_chess_pos((7,7),8) == "h8"
    assert not(matrix_to_chess_pos((0,0),8) == "h1")
    with pytest.raises(ValueError):
        matrix_to_chess_pos((0,7),0)
    with pytest.raises(ValueError):
        matrix_to_chess_pos((0,-10),8)


def test_chess_pos_to_matrix()->None:
    """Comprueba si chess_pos_to_matrix() funciona"""
    assert chess_pos_to_matrix("b1",8)==(0,1)
    assert chess_pos_to_matrix("d5",8)== (4,3)
    assert chess_pos_to_matrix("e5",8) == (4,4)
    with pytest.raises(ValueError):
        chess_pos_to_matrix("b2",0)
    with pytest.raises(ValueError):
        chess_pos_to_matrix("hola",1)