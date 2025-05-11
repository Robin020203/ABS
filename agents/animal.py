import random
from typing import List, Optional, Tuple


class Animal:
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None):
        self.world = world
        self.speed = 1
        self.position = position if position else self.world.random_position()
        self.vision_angle = random.uniform(0, 360)
        self.energy = 100

