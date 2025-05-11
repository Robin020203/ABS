import random
from typing import List, Optional, Tuple
from ABS.agents.animal import Animal


class Predator(Animal):
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None,
                 vision_range: Optional[int] = None,
                 vision_width: Optional[int] = None):
        super().__init__(world, position)
        self.vision_range = 0 #yet to be implemented
        self.vision_width = 0 #yet to be implemented
        self.energy_consumption = 2 # how much energy spent each timestep when moving normally
        self.hunger = 0 # timesteps since last meal
        self.max_hunger = 50 # timesteps before dying of hunger
        self.reproduction_threshold = 3 #amount of prey to eat in order to reproduce

    def update(self, world):
        self.energy -= self.energy_consumption
        self.hunger += 1

        if self.hunger > self.max_hunger:
            world.predator_dies(self)

        # prey = self.look_for_prey(self)

        # if prey:

        # else:
        #   self.wander()




