from pynput import *

def print_coord(x, y):
    print("Now at: {}".format((x, y)))


with mouse.Listener(on_move=print_coord) as listen:
    listen.join()


