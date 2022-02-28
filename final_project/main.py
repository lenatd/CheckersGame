'''
Lena Duong
CS 5001, Fall 2021

This is a graphical game of checkers that one player would be able to play with
the computer.
'''
import turtle
from turn import GameState
from gameboard import Board


def main():
    try:
        GameState(Board)
    except Exception as ex:
        print(ex)
    turtle.done()


if __name__ == "__main__":
    main()
