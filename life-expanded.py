# Another Game of Life, on a larger board, with
# pixel darkness corresponding to # of live cells
# in the spaces covered by that pixel.
#
# Doesn't look nearly as interesting as I hoped it would.

from microbit import *
import random

ratio = 0.2
size = 15


def new_board():
    return [[False] * size for _ in range(size)]


def init():
    board = new_board()

    for y in range(0, size):
        for x in range(0, size):
            board[x][y] = random.random() <= ratio

    return board


def wrap(x):
    if x < 0:
        return x + size
    elif x >= size:
        return x - size
    else:
        return x


def is_alive(x, y, board):
    return board[wrap(x)][wrap(y)]


def any_live(board):
    for x in range(0, size):
        for y in range(0, size):
            if is_alive(x, y, board):
                return True
    return False


def count_neighbors(x, y, board):
    counter = 0

    for x_ in range(-1, 1):
        for y_ in range(-1, 1):
            if x_ and y_ and is_alive(x + x_, y + y_, board):
                counter = counter + 1

    return counter


def should_live(x, y, board):
    num_neighbors = count_neighbors(x, y, board)

    if num_neighbors == 2:
        return is_alive(x, y, board)
    elif num_neighbors == 3:
        return True
    else:
        return False


def evolve(board):
    next_board = new_board()

    for y in range(0, size):
        for x in range(0, size):
            next_board[x][y] = should_live(x, y, board)

    return next_board


def tween_step(image1, image2, step):
    frame = Image(5, 5)

    for x in range(0, 5):
        for y in range(0, 5):
            val1 = image1.get_pixel(x, y)
            val2 = image2.get_pixel(x, y)
            increment = ((val2 - val1) * step) / 9

            frame.set_pixel(x, y, int(val1 + increment))

    return frame


def tween(image1, image2):
    return [
        tween_step(image1, image2, x)
        for x in range(0, 10)
    ]


def count_live(x, y, step, board):
    return [
        is_alive(x + x_, y + y_, board)
        for x_ in range(0, step)
        for y_ in range(0, step)
    ].count(True)


def draw(board):
    image = Image(5, 5)

    step = int(size / 5)

    for x in range(0, 5):
        for y in range(0, 5):
            value = count_live(x * step, y * step, step, board)
            image.set_pixel(x, y, value)

    return image


last_board = init()
last_image = draw(last_board)
display.show(last_image)

while(True):
    if any_live(last_board):
        next_board = evolve(last_board)
    else:
        next_board = init()

    next_image = draw(next_board)
    anim = tween(last_image, next_image)
    display.show(anim, delay=100)

    last_board = next_board
    last_image = next_image
