# Simple focus timer
#
# Features:
#  The timer counts down 25 minutes, with one LED going dark every minute. 
#  At the end of 25 minutes, the LED grid starts blinking to indicate break time.
#
#  There is no break time timer. If you're keeping an eye on the screen, you aren't
#  really taking a break. Step away from your desk. :3 I use my phone as a timer for
#  breaks.
#
#  Controls:
#    The left button toggles the timer on/off. Toggling it off just blanks the screen.
#    Toggling it back on starts a new pomodoro. There is no pause/resume.
#
#    The right button starts a new pomodoro.

from microbit import *

# States
WORK = 1
WORK_DONE = 2
HUSH = 3

# 25 minutes, 25 pixels, 10 brighness levels per pixel
WORK_TICK_MS = 6000
# WORK_TICK_MS = 10
BLINK_TICK_MS = 500

image = Image(5, 5)
cur_x = 0
cur_y = 0
last_tick = None


def tick_next_minute():
    global cur_x
    global cur_y
    if cur_x < 4:
        cur_x = cur_x + 1
        return work_tick()
    else:
        if cur_y < 4:
            cur_x = 0
            cur_y = cur_y + 1
            return work_tick()
        else:
            return WORK_DONE


def work_tick():
    global image
    global cur_x
    global cur_y
    cur = image.get_pixel(cur_x, cur_y)
    if cur <= 0:
        return tick_next_minute()
    else:
        image.set_pixel(cur_x, cur_y, cur - 1)
        display.show(image)
        return WORK


def work():
    global last_tick
    time = running_time() - last_tick
    if time >= WORK_TICK_MS:
        last_tick = last_tick + WORK_TICK_MS
        return work_tick()
    else:
        return WORK


def work_done_tick():
    global last_tick
    global image
    time = running_time() - last_tick
    if time >= BLINK_TICK_MS:
        last_tick = last_tick + BLINK_TICK_MS
        image = image.invert()
        display.show(image)


def work_done():
    work_done_tick()
    return WORK_DONE


def start_work():
    global image
    global cur_x
    global cur_y
    global last_tick

    image.fill(9)
    display.show(image)
    cur_x = 0
    cur_y = 0
    last_tick = running_time()
    return WORK

def toggle_hush(state):
    if state == HUSH:
        return start_work()
    else:
        display.clear()
        return HUSH

def check_buttons(state):
    global button_a
    global button_b
    hush = button_a.was_pressed()
    restart = button_b.was_pressed()

    if restart:
        return start_work()
    elif hush:
        return toggle_hush(state)
    else:
        return None

def handle_state(state):
    if state == WORK:
        return work()
    elif state == WORK_DONE:
        return work_done()
    else:
        return state


state = start_work()
while True:
    sleep(50)
    state = check_buttons(state) or handle_state(state)
