import turtle
import a


class Board:
    '''
        Class -- Board
            Creates the board.
        Attributes:
            squares -- the layout of each piece.
            player -- the object to draw the pieces
            setpieces -- the inital layout of the pieces
            win -- the last standing player.
        Methods:
            draw_square -- draws the squares on the board
            draw_circle -- draws the pieces on the board
            setup_board -- draws the entire board
            setup_pieces -- draws the pieces on the board before playing
            king_create -- redefines a regular piece as a kings piece
            update_pieces -- redraws the pieces on the board
            winner_graphics -- displays the graphics of the winner
    '''

    def __init__(self):
        self.squares = [
            [a.EMPTY, a.BLACK, a.EMPTY, a.BLACK,
                a.EMPTY, a.BLACK, a.EMPTY, a.BLACK],
            [a.BLACK, a.EMPTY, a.BLACK, a.EMPTY,
                a.BLACK, a.EMPTY, a.BLACK, a.EMPTY],
            [a.EMPTY, a.BLACK, a.EMPTY, a.BLACK,
                a.EMPTY, a.BLACK, a.EMPTY, a.BLACK],
            [a.EMPTY, a.EMPTY, a.EMPTY, a.EMPTY,
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
        self.player = turtle.Turtle()
        self.setpieces = turtle.Turtle()
        self.win = None

    def draw_square(self, a_turtle, size):
        '''
            Function -- draw_square
                Draw a square of a given size.
            Parameters:
                self -- the current Board object
                a_turtle -- an instance of Turtle
                size -- the length of each side of the square
            Returns:
                Nothing. Draws a square in the graphics window.
        '''
        RIGHT_ANGLE = 90
        a_turtle.begin_fill()
        a_turtle.pendown()
        for i in range(4):
            a_turtle.forward(size)
            a_turtle.left(RIGHT_ANGLE)
        a_turtle.end_fill()
        a_turtle.penup()

    def draw_circle(self, a_turtle, size):
        '''
            Function -- draw_circle
                Creates the individual circles
            Parameters:
                self -- The current GameState object
                a_turtle -- The turtle object
                size -- The size of the circle
        '''
        a_turtle.begin_fill()
        a_turtle.pendown()
        a_turtle.circle(size)
        a_turtle.penup()
        a_turtle.end_fill()

    def setup_board(self):
        '''
            Function -- setup_board
                Draws the entire board.
            Parameters:
                self -- the current Board object
            Returns:
                Nothing. Draws the board.
        '''
        turtle.title("Checkers Game")
        turtle.setup(a.WINDOW_SIZE, a.WINDOW_SIZE)
        turtle.screensize(a.BOARD_SIZE, a.BOARD_SIZE)
        turtle.bgcolor("white")
        turtle.tracer(0, 0)
        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()
        pen.color("black", "white")
        pen.setposition(a.CORNER, a.CORNER)
        self.draw_square(pen, a.BOARD_SIZE)
        for col in range(a.NUM_SQUARES):
            for row in range(a.NUM_SQUARES):
                pen.color("black", a.SQUARE_COLORS[0])
                pen.setposition(a.CORNER + a.SQUARE * col,
                                a.CORNER + a.SQUARE * row)
                if col % 2 != row % 2:
                    self.draw_square(pen, a.SQUARE)

    def setup_pieces(self):
        '''
            Function -- setup
                Sets up of the game pieces before the player starts to play.
            Parameters:
                self -- The current GameState object
            Returns:
                Nothing.
        '''
        self.setpieces.penup()
        for col in range(a.NUM_SQUARES):
            for row in range(a.NUM_SQUARES):
                if col % 2 != row % 2:
                    self.setpieces.setposition(a.CORNER + a.RADIUS + a.SQUARE *
                                               col, a.CORNER + a.SQUARE * row)
                    if row not in a.SKIP_ROWS:
                        if row < a.SKIP_ROWS[0]:
                            self.setpieces.color("black", a.CIRCLE_COLORS[1])
                        elif row > a.SKIP_ROWS[1]:
                            self.setpieces.color("black", a.CIRCLE_COLORS[0])
                        self.draw_circle(self.setpieces, a.RADIUS)

    def king_create(self, col):
        '''
            Function -- king_create
                Identifies the regular piece as a king.
            Parameters:
                self -- The current GameState object
                col -- The column of the board
            Returns:
                Nothing.
        '''
        if self.squares[a.MAX][col] == a.BLACK:
            self.squares[a.MAX][col] = a.KING_BLACK
            self.squares[a.MAX][col] = a.KING_BLACK
        elif self.squares[a.MIN][col] == a.RED:
            self.squares[a.MIN][col] = a.KING_RED

    def update_pieces(self):
        '''
            Function -- update_pieces
                Updates the pieces of the board after every move
            Parameters:
                self -- The current GameState object
                row -- The row of the board when the click is made
                col -- The column of the board when the click is made
            Returns:
                Nothing.
        '''
        self.player.clear()
        self.setpieces.clear()
        self.player.penup()
        for col in range(a.NUM_SQUARES):
            self.king_create(col)
            for row in range(a.NUM_SQUARES):
                if self.squares[row][col] != a.EMPTY:
                    self.player.setposition(a.CORNER + a.RADIUS + a.SQUARE *
                                            col, a.CORNER + a.SQUARE * row)
                    if self.squares[row][col] == a.BLACK or \
                            self.squares[row][col] == a.KING_BLACK:
                        self.player.color(a.CIRCLE_COLORS[1],
                                          a.CIRCLE_COLORS[1])
                    elif self.squares[row][col] == a.RED or \
                            self.squares[row][col] == a.KING_RED:
                        self.player.color(a.CIRCLE_COLORS[1],
                                          a.CIRCLE_COLORS[0])
                    self.draw_circle(self.player, a.RADIUS)

                    self.player.setposition(a.CORNER + a.RADIUS + a.SQUARE *
                                            col, a.CORNER + (a.RADIUS / 2) +
                                            a.SQUARE * row)
                    if self.squares[row][col] == a.KING_BLACK:
                        self.player.color(a.CIRCLE_COLORS[2],
                                          a.CIRCLE_COLORS[1])
                        self.draw_circle(self.player, (a.RADIUS / 2))
                    elif self.squares[row][col] == a.KING_RED:
                        self.player.color(a.CIRCLE_COLORS[2],
                                          a.CIRCLE_COLORS[0])
                        self.draw_circle(self.player, (a.RADIUS / 2))

    def winner_graphics(self):
        '''
            Function -- winner_graphics
                Displays the winner's graphics
            Parameters:
                self -- The current GameState object
            Returns:
                Nothing.
        '''
        turtle.color('green')
        style = ('arial', 30, 'bold')
        turtle.write(self.win + ' Wins!', font=style, align='center')
        turtle.hideturtle()
