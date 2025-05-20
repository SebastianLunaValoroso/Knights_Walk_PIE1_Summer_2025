import pytest
import numpy as np
from math import sqrt
from knight_walk_simulation import valid_square


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
