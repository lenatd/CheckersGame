import turtle
import a
import random


class GameState:
    '''
        Class -- GameState
            Provides information about what pieces are where on the board,
            legal moves, current turn, and whether the game is over.
        Attributes:
            screen -- The screen for initial selection.
            move -- The screen for moves.
            capture -- The screen for capture
            multiple -- The screen for multiple captures
            board -- The board object.
            current_player -- The current player at a turn.
            opposing_player -- The opossing player at a turn.
            capture_search -- If there are capturing moves available.
            x -- The current player's x position
            y -- The current player's y position
            captures -- Contains all the possible captures.
            jumps -- Contains all the possible jumps.
            moves -- Contains all the possible moves.
        Methods:
            click_handler -- Registers the coordinates for the player's piece.
            set_piece -- Sets the coordinates for the player's piece.
            capture_exists -- Indentifies all possible capturing moves.
            bot_left -- Determines if there is a valid capture
            bottom left of opponent.
            bot_right -- Determines if there is a valid capture
            bottom right of opponent.
            top_left -- Determines if there is a valid capture
            top left of opponent.
            top_right -- Determines if there is a valid capture
            top right of opponent.
            capture_click -- Click handler for capturing moves.
            multiple_capture -- Click handler for another capturing move.
            move_click -- Click handler for moves.
            player_turn -- Updates the current player.
            get_valid_moves -- Identifies all possible moves for player.
            king_moves -- Identifies all possible moves for king pieces.
            move_bot_left -- Determines if there is a possible move
            bottom left of player.
            move_bot_right -- Determines if there is a possible move bottom
            right of player.
            computer -- The ai opponent player.
            get_coords -- Converts coordinates of clicks to rows and columns of
            the board.
            update_move -- Updates the pieces after a move.
            update_capture -- Updates the pieces after a capture.
            update_pieces -- Updates the pieces of the game.
            winner -- determines the winner based on the number of players
    '''

    def __init__(self, board):
        '''
            Constructor -- creates a new instance of GameState
            Parameters:
                self -- the current GameState object
                board -- the Board object
        '''
        self.screen = turtle.Screen()
        self.move = turtle.Screen()
        self.capture = turtle.Screen()
        self.multiple = turtle.Screen()

        self.board = board()
        self.board.setup_board()
        self.board.setup_pieces()

        self.current_player = a.BLACK
        self.opposing_player = a.RED
        self.capture_search = False
        self.x = 0
        self.y = 0
        self.captures = {}
        self.jumps = {}
        self.moves = {}

        self.screen.onclick(self.click_handler)

    def click_handler(self, x, y):
        '''
            Function -- click_handler
                Called when a click occurs and whether the clicks are in bound
                and calls a new click handler depending on the possible moves.
            Parameters:
                self -- the current GameState object
                x -- X coordinate of the click.
                y -- Y coordinate of the click.
            Returns:
                Does not and should not return. Click handlers are a special
                type of function automatically called by Turtle. You will not
                have access to anything returned by this function.
        '''
        if self.winner():
            self.board.winner_graphics()
        elif (x >= a.CORNER and x <= - a.CORNER and
                y >= a.CORNER and y <= -a.CORNER):
            row = self.get_coords(y)
            col = self.get_coords(x)
            self.get_valid_moves()
            if not self.capture_exists() and (row, col) in self.moves:
                self.set_piece(row, col)
                self.move.onclick(self.move_click)
            elif (row, col) in self.captures:
                self.set_piece(row, col)
                self.capture.onclick(self.capture_click)
        else:
            raise Exception("Out of bound!")

    def set_piece(self, row, col):
        '''
            Function -- set_piece
                Sets the coordinates to its respective variables as the
                player's current piece.
            Parameters:
                self -- the current GameState object
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
            Returns:
                Nothing.
        '''
        self.x = col
        self.y = row

    def capture_exists(self):
        '''
            Function -- capture_exists
                Indentifies all possible capturing moves.
            Parameters:
                self -- the current GameState object
            Returns:
                Whether a capture exists.
        '''
        self.capture_search = False
        self.captures.clear()
        self.jumps.clear()
        for col in range(a.NUM_SQUARES):
            for row in range(a.NUM_SQUARES):
                if self.board.squares[row][col].split()[0] == \
                        self.opposing_player.split()[0] and \
                        col < a.MAX and col > a.MIN and \
                        row < a.MAX and row > a.MIN:
                    if self.current_player.split()[0] == a.BLACK.split()[0]:
                        self.bot_left(row, col, a.BLACK)
                        self.bot_right(row, col, a.BLACK)
                        self.top_right(row, col, a.KING_BLACK)
                        self.top_left(row, col, a.KING_BLACK)
                        self.bot_left(row, col, a.KING_BLACK)
                        self.bot_right(row, col, a.KING_BLACK)
                    elif self.current_player.split()[0] == a.RED.split()[0]:
                        self.top_left(row, col, a.RED)
                        self.top_right(row, col, a.RED)
                        self.top_left(row, col, a.KING_RED)
                        self.top_right(row, col, a.KING_RED)
                        self.bot_left(row, col, a.KING_RED)
                        self.bot_right(row, col, a.KING_RED)
        return self.capture_search

    def bot_left(self, row, col, player):
        '''
            Function -- bot_left
                Determines if there is a valid capture bottom left of opponent.
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
                player -- The type of piece.
            Returns:
                Nothing.
        '''
        if self.board.squares[row - 1][col - 1] == player and \
                self.board.squares[row + 1][col + 1] == a.EMPTY:
            if (row - 1, col - 1) in self.captures:
                self.captures[(row - 1, col - 1)].append([row + 1, col + 1])
            else:
                self.captures[(row - 1, col - 1)] = [[row + 1, col + 1]]
            self.jumps[((row - 1, col - 1), (row + 1, col + 1))] = [row, col]
            self.capture_search = True

    def bot_right(self, row, col, player):
        '''
            Function -- bot_right
                Determines if there is a valid capture bottom right of opponent
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
                player -- The type of piece.
            Returns:
                Nothing.
        '''
        if self.board.squares[row - 1][col + 1] == player and \
                self.board.squares[row + 1][col - 1] == a.EMPTY:
            if (row - 1, col + 1) in self.captures:
                self.captures[(row - 1, col + 1)].append([row + 1, col - 1])
            else:
                self.captures[(row - 1, col + 1)] = [[row + 1, col - 1]]
            self.jumps[((row - 1, col + 1), (row + 1, col - 1))] = [row, col]
            self.capture_search = True

    def top_left(self, row, col, player):
        '''
            Function -- top_left
                Determines if there is a valid capture top left of opponent.
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
                player -- The type of piece.
            Returns:
                Nothing.
        '''
        if self.board.squares[row + 1][col - 1] == player and \
                self.board.squares[row - 1][col + 1] == a.EMPTY:
            if (row + 1, col - 1) in self.captures:
                self.captures[(row + 1, col - 1)].append([row - 1, col + 1])
            else:
                self.captures[(row + 1, col - 1)] = [[row - 1, col + 1]]
            self.jumps[((row + 1, col - 1), (row - 1, col + 1))] = [row, col]
            self.capture_search = True

    def top_right(self, row, col, player):
        '''
            Function -- top_right
                Determines if there is a valid capture top right of opponent.
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
                player -- The type of piece.
            Returns:
                Nothing.
        '''
        if self.board.squares[row + 1][col + 1] == player and \
                self.board.squares[row - 1][col - 1] == a.EMPTY:
            if (row + 1, col + 1) in self.captures:
                self.captures[(row + 1, col + 1)].append([row - 1, col - 1])
            else:
                self.captures[(row + 1, col + 1)] = [[row - 1, col - 1]]
            self.jumps[((row + 1, col + 1), (row - 1, col - 1))] = [row, col]
            self.capture_search = True

    def capture_click(self, x, y):
        '''
            Function -- capture_click
                Called when a capture move is available.
            Parameters:
                self -- the current GameState object
                x -- X coordinate of the click.
                y -- Y coordinate of the click.
            Returns:
                Does not return.
        '''
        row = self.get_coords(y)
        col = self.get_coords(x)
        if [row, col] in self.captures[(self.y, self.x)]:
            jump_x = col
            jump_y = row
            self.update_capture(self.y, self.x, jump_y, jump_x)
            self.set_piece(jump_y, jump_x)
            self.board.update_pieces()
            self.capture_exists()
            if self.winner():
                self.board.winner_graphics()
            elif (self.y, self.x) in self.captures:
                self.multiple.onclick(self.multiple_capture)
            else:
                self.player_turn()
                self.computer()

    def multiple_capture(self, x, y):
        '''
            Function -- multiple_capture
                Called when another capture move is available.
            Parameters:
                self -- the current GameState object
                x -- X coordinate of the click.
                y -- Y coordinate of the click.
            Returns:
                Does not return.
        '''
        row = self.get_coords(y)
        col = self.get_coords(x)
        if row == self.y and col == self.x:
            self.capture.onclick(self.capture_click)

    def move_click(self, x, y):
        '''
            Function -- move_click
                The click coordinates for the move.
            Parameters:
                self -- The current GameState object
                x -- The x coordinated of the click
                y -- The y coordinated of the click
            Returns:
                Does not return anything.
        '''
        row = self.get_coords(y)
        col = self.get_coords(x)
        if [row, col] in self.moves[(self.y, self.x)]:
            self.update_move(self.y, self.x, row, col)
            self.board.update_pieces()
            if self.winner():
                self.board.winner_graphics()
            else:
                self.player_turn()
                self.computer()
        else:
            print("Invalid Move!")
            self.screen.onclick(self.click_handler)

    def player_turn(self):
        '''
            Function -- player_turn
                Updates the current player.
            Parameters:
                self -- The current GameState object
            Returns:
                Does not return anything.
        '''
        if self.current_player == a.BLACK:
            self.current_player = a.RED
            self.opposing_player = a.BLACK
        else:
            self.current_player = a.BLACK
            self.opposing_player = a.RED

    def get_valid_moves(self):
        '''
            Function -- get_valid_moves
                Indentifies all possible moves.
            Parameters:
                self -- the current GameState object
            Returns:
                Nothing.
        '''
        self.moves.clear()
        for col in range(a.NUM_SQUARES):
            for row in range(a.NUM_SQUARES):
                if self.current_player == a.RED:
                    if self.board.squares[row][col] == a.RED:
                        if col == a.MAX:
                            self.move_bot_left(row, col)
                        elif col == a.MIN:
                            self.move_bot_right(row, col)
                        elif col > a.MIN and col < a.MAX:
                            self.move_bot_left(row, col)
                            self.move_bot_right(row, col)
                    elif self.board.squares[row][col] == a.KING_RED:
                        self.king_moves(row, col)
                elif self.current_player == a.BLACK:
                    if self.board.squares[row][col] == a.BLACK:
                        if col == a.MAX and row < a.MAX:
                            self.move_top_left(row, col)
                        elif col == a.MIN and row < a.MAX:
                            self.move_top_right(row, col)
                        elif col > a.MIN and col < a.MAX:
                            self.move_top_left(row, col)
                            self.move_top_right(row, col)
                    elif self.board.squares[row][col] == a.KING_BLACK:
                        self.king_moves(row, col)

    def king_moves(self, row, col):
        '''
            Function -- king_moves
                Indentifies all possible king moves.
            Parameters:
                self -- the current GameState object
            Returns:
                Nothing.
        '''
        if col == a.MAX:
            self.move_bot_left(row, col)
            self.move_top_left(row, col)
        elif col == a.MIN:
            self.move_bot_right(row, col)
            self.move_top_right(row, col)
        elif col > a.MIN and col < a.MAX:
            self.move_bot_right(row, col)
            self.move_bot_left(row, col)
            self.move_top_right(row, col)
            self.move_top_left(row, col)

    def move_bot_left(self, row, col):
        '''
            Function -- move_bot_left
                Determines if there is a valid move bottom left of opponent.
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
            Returns:
                Nothing.
        '''
        if row > a.MIN:
            if self.board.squares[row - 1][col - 1] == a.EMPTY:
                if (row, col) in self.moves:
                    self.moves[(row, col)].append([row - 1, col - 1])
                else:
                    self.moves[(row, col)] = [[row - 1, col - 1]]

    def move_bot_right(self, row, col):
        '''
            Function -- move_bot_right
                Determines if there is a valid move bottom right of opponent.
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
            Returns:
                Nothing.
        '''
        if row > a.MIN:
            if self.board.squares[row - 1][col + 1] == a.EMPTY:
                if (row, col) in self.moves:
                    self.moves[(row, col)].append([row - 1, col + 1])
                else:
                    self.moves[(row, col)] = [[row - 1, col + 1]]

    def move_top_left(self, row, col):
        '''
            Function -- move_top_left
                Determines if there is a valid move top left of opponent.
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
            Returns:
                Nothing.
        '''
        if row < a.MAX:
            if self.board.squares[row + 1][col - 1] == a.EMPTY:
                if (row, col) in self.moves:
                    self.moves[(row, col)].append([row + 1, col - 1])
                else:
                    self.moves[(row, col)] = [[row + 1, col - 1]]

    def move_top_right(self, row, col):
        '''
            Function -- move_top_right
                Determines if there is a valid move top right of opponent.
            Parameters:
                self -- the current GameState object.
                row -- X coordinate of the click in rows.
                col -- Y coordinate of the click in columns.
            Returns:
                Nothing.
        '''
        if row < a.MAX:
            if self.board.squares[row + 1][col + 1] == a.EMPTY:
                if (row, col) in self.moves:
                    self.moves[(row, col)].append([row + 1, col + 1])
                else:
                    self.moves[(row, col)] = [[row + 1, col + 1]]

    def computer(self):
        '''
            Function -- computer
                The ai opponent player. It determines the captures and moves.
            Parameters:
                self -- the current GameState object.
            Returns:
                Nothing.
        '''
        if self.winner():
            self.board.winner_graphics()
        elif self.current_player == a.RED:
            if not self.capture_exists():
                self.get_valid_moves()
                piece, move = random.choice(list(self.moves.items()))
                move = random.choice(move)
                self.update_move(piece[0], piece[1], move[0], move[1])
                self.screen.ontimer(self.board.update_pieces, a.TIME)
                self.player_turn()
                self.screen.onclick(self.click_handler)
            elif self.capture_exists():
                piece = random.choice(list(self.captures))
                while piece in self.captures:
                    jump = random.choice(self.captures[piece])
                    self.update_capture(piece[0], piece[1], jump[0], jump[1])
                    self.screen.ontimer(self.board.update_pieces, a.TIME)
                    piece = (jump[0], jump[1])
                    self.capture_exists()
                else:
                    self.player_turn()
                    self.screen.onclick(self.click_handler)

    def get_coords(self, value):
        '''
            Function -- get_coords
                Converts coordinates to columns and rows.
            Parameters:
                self -- the current GameState object.
                value -- the x or y coordinates.
            Returns:
                The value of the row or column.
        '''
        return int((value - a.CORNER) / a.SQUARE)

    def update_move(self, y, x, empty_y, empty_x):
        '''
            Function -- update_move
                Updates the board with the correct pieces by redefining it.
            Parameters:
                self -- the current GameState object.
                y -- the player's current row.
                x -- the player's current column.
                empty_y -- the desired row to move player.
                empty_x -- the desired column to move player.
            Returns:
                Nothing
        '''
        player = self.board.squares[y][x]
        self.board.squares[y][x] = a.EMPTY
        self.board.squares[empty_y][empty_x] = player

    def update_capture(self, y, x, jump_y, jump_x):
        '''
            Function -- update_capture
                Updates the board with the correct pieces by redefining it.
            Parameters:
                self -- the current GameState object.
                y -- the x or y coordinates.
                x -- the player's current column.
                jump_y -- the desired row to move player.
                jump_x -- the desired column to move player.
            Returns:
                Nothing
        '''
        capture = self.jumps[((y, x), (jump_y, jump_x))]
        player = self.board.squares[y][x]
        self.board.squares[y][x] = a.EMPTY
        self.board.squares[capture[0]][capture[1]] = a.EMPTY
        self.board.squares[jump_y][jump_x] = player

    def winner(self):
        '''
            Function -- winner
                Determines the winner based on the number of players
            Parameters:
                self -- The current GameState object
            Returns:
                Whether there is a winner.
        '''
        self.get_valid_moves()
        if len(self.moves) == 0:
            if self.current_player == a.RED:
                self.board.win = a.BLACK
                return True
            elif self.current_player == a.BLACK:
                self.board.win = a.RED
                return True
        return False