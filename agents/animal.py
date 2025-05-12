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

    def update(self, world):
        dx = math.cos(math.radians(self.vision_angle)) * self.speed
        newx = self.position[0] + dx
        if newx >= world.width:
            self.vision_angle = 180 - self.vision_angle
            newx = world.width
        if newx <= 0:
            self.vision_angle = 180 - self.vision_angle
            newx = 0

        dy = math.sin(math.radians(self.vision_angle)) * self.speed
        newy = self.position[1] + dy
        if newy >= world.height:
            self.vision_angle = -self.vision_angle
            newy = world.height
        if newy <= 0:
            self.vision_angle = -self.vision_angle
            newy = 0
        self.position = (newx, newy)


