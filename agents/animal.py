import random
import math
from typing import List, Optional, Tuple

# FEEDBACK: mobility class, zodat de mobility behaviour makkelijk kan worden ingeplugd
class Animal:
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None):
        self.world = world
        self.speed = 0.5
        self.position = position if position else self.world.random_position()
        self.vision_angle = random.uniform(0, 360)
        self.dead = False
        self.max_energy = 200
        self.energy = random.uniform(self.max_energy * 0.75, self.max_energy)
        self.rest_recovery_rate = 10
        self.recovery_target_energy = random.uniform(self.max_energy / 2, self.max_energy)
        self.resting = False
        self.energy_consumption = 0     #prey=0.5 and predator=1


    def update(self, world):

        if self.resting:
            self.energy += self.rest_recovery_rate
            if self.energy >= self.recovery_target_energy:
                self.energy = min(self.max_energy, self.energy)
                self.resting = False
            return # as long as self.resting = True, don't move

        if self.energy <= 0:
            self.resting = True
            return

        else:
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
            self.energy -= self.energy_consumption