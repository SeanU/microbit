# Really hokey metaballs implementation. Can't do much on a 5x5 grid.
#   https://en.wikipedia.org/wiki/Metaballs
from microbit import *
from math import sqrt, floor

force = 0.005


def get_value(x, y, balls):
    value = 0.0
    for ball in balls:
        position = ball[0]
        d = 1.0 / ((x - position[0]) ** 2 + (y - position[1]) ** 2 + 1)
        value = value + (d * 3)
    return value


def draw(balls):
    image = Image(5, 5)

    for x in range(5):
        for y in range(5):
            value = get_value(x, y, balls)
            image.set_pixel(x, y, int(floor(value)))

    display.show(image)


def delta(position):
    if position < 1.0:
        return force
    elif position > 4.0:
        return force * -1
    else:
        return 0


def update_velocity(velocity, position):
    return (
        velocity[0] + delta(position[0]),
        velocity[1] + delta(position[1])
    )


def update_position(position, velocity):
    return (
        position[0] + velocity[0],
        position[1] + velocity[1]
    )


def evolve_ball(ball):
    position, velocity = ball
    velocity = update_velocity(velocity, position)
    position = update_position(position, velocity)
    return (position, velocity)


def evolve(balls):
    return [
        evolve_ball(ball)
        for ball in balls
    ]


balls = [
    ((1.0, 1.1), (0.1, 0.1)),
    ((3.6, 3.7), (-0.1, -0.05))
]

while(True):
    draw(balls)
    balls = evolve(balls)
