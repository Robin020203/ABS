import random

def clip(min, max, value):
    average = (min + max) / 2
    if value > max:
        return random.uniform(average, max)
    elif value < min:
        return random.uniform(min, average)
    else:
        return value