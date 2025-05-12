import random
from typing import List, Optional, Tuple
from ABS.agents.animal import Animal


class Predator(Animal):
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None,
                 vision_range: float = max(17.0, min(23.0, random.gauss(20, 1))),
                 vision_width: Optional[float] = None):
        super().__init__(world, position)
        if not vision_width:
            vision_width = 20 + (3.33 * (20 - vision_range))
        vision_mutation = random.gauss(0, 0.5)
        self.vision_range = max(17.0, min(23.0, vision_range + vision_mutation))
        self.vision_width = max(10.0, min(30.0, vision_width - (3.33 * vision_mutation)))
        self.energy_consumption = 2 # how much energy spent each timestep when moving normally
        self.hunger = 0 # timesteps since last meal
        self.max_hunger = 50 # timesteps before dying of hunger
        self.reproduction_threshold = 3 #amount of prey to eat in order to reproduce
        self.eaten_prey = 0


    def update(self, world):
        super().update(world)
        self.energy -= self.energy_consumption
        self.hunger += 1

        #if self.hunger > self.max_hunger:


        if self.eaten_prey >= self.reproduction_threshold:
            self.reproduce(world)
            self.eaten_prey = 0

        # prey = self.look_for_prey(self)

        # if prey:

        # else:
        #   self.wander()

    def reproduce(self, world):
        world.add_predator(Predator(world,
                                    self.position,
                                    self.vision_range,
                                    self.vision_width))




