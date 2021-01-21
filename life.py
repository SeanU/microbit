# Game of life on a 5x5 toroidal board

from microbit import *
import random

ratio = 0.3


def to_pixel(bool_val):
    return 9 if bool_val else 0


def init():
    image = Image(5, 5)
    for y in range(0, 5):
        for x in range(0, 5):
            value = to_pixel(random.random() <= ratio)
            image.set_pixel(x, y, value)

    return image


def wrap(x):
    if x < 0:
        return x + 5
    elif x >= 5:
        return x - 5
    else:
        return x


def is_alive(x, y, image):
    return image.get_pixel(wrap(x), wrap(y)) > 0


def any_live(image):
    return [
        is_alive(x, y, image)
        for x in range(0, 5)
        for y in range(0, 5)
    ].count(True) > 0


def count_neighbors(x, y, image):
    return [
        is_alive(x - 1, y - 1, image),
        is_alive(x, y - 1, image),
        is_alive(x + 1, y - 1, image),
        is_alive(x - 1, y, image),
        is_alive(x + 1, y, image),
        is_alive(x - 1, y + 1, image),
        is_alive(x, y + 1, image),
        is_alive(x + 1, y + 1, image)
    ].count(True)


def count_neighbors_2(x, y, image):
    return [
        is_alive(x + x_, y + y_, image)
        for x_ in (-1, 0, 1)
        for y_ in (-1, 0, 1)
        if x_ != 0 or y_ != 0
    ].count(True)


def should_live(x, y, image):
    num_neighbors = count_neighbors_2(x, y, image)

    if num_neighbors == 2:
        return is_alive(x, y, image)
    elif num_neighbors == 3:
        return True
    else:
        return False


def next_frame(image):
    next_image = Image(5, 5)

    for y in range(0, 5):
        for x in range(0, 5):
            alive = should_live(x, y, image)
            value = to_pixel(alive)
            next_image.set_pixel(x, y, value)

    return next_image


def tween_step(image1, image2, step):
    frame = Image(5, 5)

    for x in range(0, 5):
        for y in range(0, 5):
            val1 = image1.get_pixel(x, y)
            val2 = image2.get_pixel(x, y)

            if val1 == val2:
                frame.set_pixel(x, y, val1)
            elif val1 > val2:
                frame.set_pixel(x, y, val1 - step)
            else:
                frame.set_pixel(x, y, step)

    return frame


def tween(image1, image2):
    return [
        tween_step(image1, image2, x)
        for x in range(0, 10)
    ]


last_image = init()
display.show(last_image)

while(True):
    if any_live(last_image):
        next_image = next_frame(last_image)
    else:
        sleep(2000)
        next_image = init()

    anim = tween(last_image, next_image)
    display.show(anim, delay=100)
    last_image = next_image
