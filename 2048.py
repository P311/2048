from typing import List
from random import *
from pygame import *
from sys import exit

SIZE = 4
WIN = 2
LOSE = 1
NOT_OVER = 0
SCREEN_SIZE = (480, 480)
CELL_SIZE = (120, 120)
CELL_PIC = {2: "2.png", 4: "4.png", 8: "8.png", 16: "16.png", 32: "32.png",
            64: "64.png", 128: "128.png", 256: "256.png", 512: "512.png", 1024: "1024.png",
            2048: "2048.png"}


# --------Logic Part --------------

def reverse(mat: List[List]) -> List[List]:
    """
    Returns the reverse of the matrix
    1  2  3      3  2  1
    4  5  6  ->  6  5  4
    7  8  9      9  8  7
    mat[row][column]
    """
    new = []
    for r in mat:
        row = []
        for i in r:
            row.insert(0, i)
        new.append(row)
    return new


def transpose(mat: List[List]) -> List[List]:
    """
    Returns the transpose of the matrix
    1  2  3      1  4  7
    4  5  6  ->  2  5  8
    7  8  9      3  6  9
    mat[row][column]
    """
    new = []
    x = y = len(mat)
    for i in range(y):
        new.append([])
        for j in range(x):
            new[i].append(mat[j][i])
    return new


def cover(mat: List[List]) -> (List[List], int):
    """
    Cover cells to left
    0  2  1       2  1  0
    6  0  4  ->   6  4  0
    0  8  7       8  7  0
    """
    count = 0
    new = [[] for i in range(len(mat))]
    for r in range(len(mat)):
        for c in mat[r]:
            if c != 0:
                count += 1
                new[r].append(c)
        while len(new[r]) != len(mat[r]):
            new[r].append(0)
    over = LOSE if count == len(mat) ** 2 else NOT_OVER
    return new, over


def merge(mat: List[List]) -> (List[List], int):
    """
    Precondition: the matrix has been covered
    Merge value pair in mat
    2  2  0        4  0  0
    6  0  0   ->   6  0  0
    4  4  4        8  4  0
    """
    over = False
    new = [[] for i in range(len(mat))]
    for r in range(len(mat)):
        i = 0
        while i != len(mat[r]):
            if i < len(mat[r]) - 1 and mat[r][i] == mat[r][i + 1]:
                new[r].append(mat[r][i] * 2)
                over = WIN if (mat[r][i] == 1024 or over) else NOT_OVER
                new[r].append(0)
                i += 2
            else:
                new[r].append(mat[r][i])
                i += 1
    return cover(new)[0], over


def left(mat: List[List]) -> (List[List], int):
    """
    Move left
    """
    mat = cover(mat)[0]
    mat, over2 = merge(mat)
    mat, over3 = cover(mat)
    if over2 == WIN:
        return mat, WIN
    else:
        return mat, over3


def right(mat: List[List]) -> (List[List], int):
    """
    Move right
    """
    mat = reverse(mat)
    mat, over = left(mat)
    return reverse(mat), over


def up(mat: List[List]) -> (List[List], int):
    """
    Move up
    """
    mat = transpose(mat)
    mat, over = left(mat)
    return transpose(mat), over


def down(mat: List[List]) -> (List[List], int):
    """
    Move down
    """
    mat = reverse(transpose(mat))
    mat, over = left(mat)
    return transpose(reverse(mat)), over


class GameBoard:
    """
    Game class
    """
    matrix: List[List]

    def __init__(self, size: int) -> None:
        """
        Initialize the game board
        """
        self.matrix = [[0] * size for i in range(size)]
        self.over = 0
        self.generate_next()
        self.generate_next()

    def __str__(self) -> str:
        """
        str representation of the game
        """
        result = ""
        for r in self.matrix:
            for c in r:
                result += str(c)
                result += "  "
            result += "\n"
        return result

    def is_over(self) -> int:
        """
        Returns the game state
        """
        c1 = []
        c2 = []
        c3 = []
        c4 = []
        for i in self.matrix:
            c1.append(i.copy())
            c2.append(i.copy())
            c3.append(i.copy())
            c4.append(i.copy())
        result = [up(c1)[1], down(c2)[1], left(c3)[1], right(c4)[1]]
        if WIN not in result:
            return min(result)
        return WIN

    def generate_next(self):
        """
        Generate next step
        """
        index = (randint(0, SIZE - 1), randint(0, SIZE - 1))
        while self.matrix[index[0]][index[1]] != 0:
            index = (randint(0, SIZE - 1), randint(0, SIZE - 1))
        a = uniform(0, 1)
        if a <= 0.1:
            value = 4
        else:
            value = 2
        self.matrix[index[0]][index[1]] = value


# ----------- pygame part -----------


def game():
    """
    Major game process
    """
    def draw(g: GameBoard) -> None:
        """
        Draw the gameboard based on matrix of g
        """
        mat = g.matrix
        for r in range(len(mat)):
            for c in range(len(mat[r])):
                if mat[r][c] != 0:
                    pic = CELL_PIC[mat[r][c]]
                    sprite = image.load(pic).convert_alpha()
                    screen.blit(sprite, (c * CELL_SIZE[0], r * CELL_SIZE[1]))

    init()
    screen = display.set_mode(SCREEN_SIZE, 0, 32)
    background = image.load("title.png").convert()
    start = False
    while True:
        if start:
            if game.is_over() == 1:
                game = GameBoard(SIZE)
                background = image.load("Lose.png").convert()
                start = False
            elif game.is_over() == 2:
                game = GameBoard(SIZE)
                background = image.load("Win.png").convert()
                start = False
        screen.blit(background, (0, 0))
        for e in event.get():
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    background = image.load("background.png").convert()
                    game = GameBoard(SIZE)
                    start = True
                elif start:
                    before = game.matrix
                    if e.key == K_LEFT:
                        game.matrix = left(game.matrix)[0]
                    elif e.key == K_RIGHT:
                        game.matrix = right(game.matrix)[0]
                    elif e.key == K_UP:
                        game.matrix = up(game.matrix)[0]
                    elif e.key == K_DOWN:
                        game.matrix = down(game.matrix)[0]
                    if game.matrix != before:
                        game.generate_next()
        if start:
            draw(game)
        display.update()



if __name__ == "__main__":
    game()
