import a
from turn import GameState
from pytest import raises
from gameboard import Board



def test_constructor():
    game = GameState(Board)

    assert(game.current_player == a.BLACK)
    assert(game.opposing_player == a.RED)
    assert(game.capture_search is False)
    assert(game.x == 0)
    assert(game.y == 0)
    assert(game.captures == {})
    assert(game.jumps == {})
    assert(game.moves == {})


def test_click_bounds_validate():
    game = GameState(Board)
    with raises(Exception):
        game.click_handler(a.BOARD_SIZE, a.BOARD_SIZE)


def test_turn():
    game = GameState(Board)
    game.player_turn()
    assert(game.current_player == a.RED)
    assert(game.opposing_player == a.BLACK)

def test_set_piece():
    game = GameState(Board)
    game.set_piece(1, 2)
    assert(game.x == 2)
    assert(game.y == 1)

def test_get_coords():
    game = GameState(Board)
    assert(game.get_coords(a.SQUARE) == 5)

def test_update_move():
    game = GameState(Board)
    game.update_move(2, 1, 3, 0)

    squares_after = [
            [a.EMPTY, a.BLACK, a.EMPTY, a.BLACK,
                a.EMPTY, a.BLACK, a.EMPTY, a.BLACK],
            [a.BLACK, a.EMPTY, a.BLACK, a.EMPTY,
                a.BLACK, a.EMPTY, a.BLACK, a.EMPTY],
            [a.EMPTY, a.EMPTY, a.EMPTY, a.BLACK,
                a.EMPTY, a.BLACK, a.EMPTY, a.BLACK],
            [a.BLACK, a.EMPTY, a.EMPTY, a.EMPTY,
                a.EMPTY, a.EMPTY, a.EMPTY, a.EMPTY],
            [a.EMPTY, a.EMPTY, a.EMPTY, a.EMPTY,
                a.EMPTY, a.EMPTY, a.EMPTY, a.EMPTY],
            [a.RED, a.EMPTY, a.RED, a.EMPTY, a.RED,
                a.EMPTY, a.RED, a.EMPTY],
            [a.EMPTY, a.RED, a.EMPTY, a.RED, a.EMPTY,
                a.RED, a.EMPTY, a.RED],
            [a.RED, a.EMPTY, a.RED, a.EMPTY, a.RED,
                a.EMPTY, a.RED, a.EMPTY]
        ]

    assert(game.board.squares == squares_after)

def test_capture_exists():
    game = GameState(Board)
    assert(game.capture_exists() is False)

def test_bot_left():
    game = GameState(Board)
    game.bot_left(2, 3, a.BLACK)
    captures_after = {(1, 2): [[3, 4]]}
    jumps_after = {((1, 2), (3, 4)): [2, 3]}
    assert(game.captures == captures_after)
    assert(game.jumps == jumps_after)
    assert(game.capture_search is True)

def test_bot_right():
    game = GameState(Board)
    game.bot_right(2, 3, a.BLACK)
    captures_after = {(1, 4): [[3, 2]]}
    jumps_after = {((1, 4), (3, 2)): [2, 3]}
    assert(game.captures == captures_after)
    assert(game.jumps == jumps_after)
    assert(game.capture_search is True)

def test_top_left():
    game = GameState(Board)
    game.top_left(5, 6, a.RED)
    captures_after = {(6, 5): [[4, 7]]}
    jumps_after = {((6, 5), (4, 7)): [5, 6]}
    assert(game.captures == captures_after)
    assert(game.jumps == jumps_after)
    assert(game.capture_search is True)

def test_top_right():
    game = GameState(Board)
    game.top_right(5, 6, a.RED)
    captures_after = {(6, 7): [[4, 5]]}
    jumps_after = {((6, 7), (4, 5)): [5, 6]}
    assert(game.captures == captures_after)
    assert(game.jumps == jumps_after)
    assert(game.capture_search is True)

def test_get_valid_moves():
    game = GameState(Board)
    moves_after = {
        (2, 1): [[3, 0], [3, 2]],
        (2, 3): [[3, 2], [3, 4]],
        (2, 5): [[3, 4], [3, 6]],
        (2, 7): [[3, 6]]
        }
    game.get_valid_moves()
    assert(game.moves == moves_after)

def test_king_moves():
    game = GameState(Board)

    game.king_moves(5, 6)
    game.king_moves(2, 1)
    moves_after = {
        (5, 6): [[4, 7], [4, 5]],
        (2, 1): [[3, 2], [3, 0]]
        }
    assert(game.moves == moves_after)

def test_move_bot_left():
    game = GameState(Board)

    game.move_bot_left(5, 6)
    moves_after = {(5, 6): [[4, 5]]}
    assert(game.moves == moves_after)

def test_move_bot_right():
    game = GameState(Board)

    game.move_bot_right(5, 6)
    moves_after = {(5, 6) : [[4, 7]]}
    assert(game.moves == moves_after)

def test_move_top_left():
    game = GameState(Board)

    game.move_top_left(2, 1)
    moves_after = {(2, 1): [[3, 0]]}
    assert(game.moves == moves_after)

def test_move_top_right():
    game = GameState(Board)

    game.move_top_right(2, 1)
    moves_after = {(2, 1): [[3, 2]]}
    assert(game.moves == moves_after)

def test_winner():
    game = GameState(Board)

    game.winner()
    assert(game.winner() is False)