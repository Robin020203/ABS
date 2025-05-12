import random
import math
from typing import List, Optional, Tuple


class Animal:
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None):
        self.world = world
        self.speed = 0.5
        self.position = position if position else self.world.random_position()
        self.vision_angle = random.uniform(0, 360)
        self.energy = 100
        self.object = None
        self.dead = False

    def update(self, world):
        dx = math.cos(math.radians(self.vision_angle)) * self.speed
        new_x = self.position[0] + dx
        if new_x >= world.width:
            self.vision_angle = 180 - self.vision_angle
            new_x = world.width
        if new_x <= 0:
            self.vision_angle = 180 - self.vision_angle
            new_x = 0

        dy = math.sin(math.radians(self.vision_angle)) * self.speed
        new_y = self.position[1] + dy
        if new_y >= world.height:
            self.vision_angle = -self.vision_angle
            new_y = world.height
        if new_y <= 0:
            self.vision_angle = -self.vision_angle
            new_y = 0
        self.position = (new_x, new_y)


