import random

def clip(min, max, value): # , mutation, mu, sigma):
    #new_value = value + mutation
    #if new_value > max or new_value < min:
    #    return clip(min, max, value, random.gauss(mu, sigma), mu, sigma)
    #else:
    #    return new_value

    average = (min + max) / 2
    if value > max:
        return random.uniform(average, max)
    elif value < min:
        return random.uniform(min, average)
    else:
        return value