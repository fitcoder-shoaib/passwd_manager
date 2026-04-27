
import random
def en(tri):
    algo = ""
    for ch in tri:
        algo += ch + str(random.randint(1,9))
    return(algo)
def den(tri):
    return(tri[::2])