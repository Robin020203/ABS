import random
from typing import List, Optional, Tuple
from ABS.agents.animal import Animal

class Prey(Animal):
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None,
                 vision_range: float = max(7.0, min(13.0, random.gauss(10, 1))),
                 vision_width: Optional[float] = None):
        super().__init__(world, position)
        if not vision_width:
            vision_width = 60 - (6.66 * (10 - vision_range))
        vision_mutation = random.gauss(0, 1)
        self.vision_range = max(7.0, min(13.0, vision_range + vision_mutation))
        self.vision_width = max(40.0, min(80.0, vision_width - (6.66 * vision_mutation)))
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