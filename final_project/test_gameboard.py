import a
from gameboard import Board

def test_constructors():
    board = Board()

    assert(board.win == None)