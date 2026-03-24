from time import time


def current_milli_time():
    return round(time() * 10 ** 3)