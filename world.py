import random
from typing import List
from agents.predator import Predator
from agents.prey import Prey

class World:
    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height
        self.predators: List[Predator] = []
        self.preys: List[Prey] = []
        self.timestep: int = 0

    def add_predator(self, predator: Predator):
        self.predators.append(predator)

    def add_prey(self, prey: Prey):
        self.preys.append(prey)

    def predator_dies(self, predator: Predator):
        if predator in self.predators:
            self.predators.remove(predator)

    def prey_dies(self, prey: Prey):
        if prey in self.preys:
            self.preys.remove(prey)

    def randomposition(self):
        return (random.random() * self.width, random.random() * self.height)

    def update(self):
        self.timestep += 1

        for predator in self.predators:
            predator.update(self)

        for prey in self.preys:
            prey.update(self)

        self.update_reproduction()

    def update_reproduction(self):
        pass



