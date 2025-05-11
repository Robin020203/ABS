import random
from typing import List, Optional, Tuple
from ABS.agents.animal import Animal

class Prey(Animal):
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None,
                 vision_range: Optional[int] = None,
                 vision_width: Optional[int] = None):
        super().__init__(world, position)
        self.vision_range = 0 #TODO
        self.vision_width = 0 #TODO
        self.energy_consumption = 1
        self.time_alive = 0
        self.reproduction_threshold = 50 # after this amount of timesteps, the prey reproduces

    def update(self, world):
        self.energy -= self.energy_consumption
        self.time_alive += 1

        if self.time_alive >= self.reproduction_threshold:
            self.reproduce()

    def reproduce(self):
        pass #TODO