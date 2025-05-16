import random
import math
from typing import Tuple

class Mobility:
    def __init__(self, speed: float = 0.5):
        self.speed = speed

    def move(self, current_position: Tuple[float, float], current_angle: float) -> Tuple[Tuple[float, float], float]:
        return current_position, current_angle

class Brownian_motion(Mobility):
    def __init__(self, speed: float = 0.5, angle_change: float = 30.0):
        super().__init__(speed)
        self.angle_change = angle_change

    def move(self, current_position: Tuple[float, float], current_angle: float) -> Tuple[Tuple[float, float], float]:
        new_angle = (current_angle + random.uniform(-self.angle_change, self.angle_change)) % 360

        dx = math.cos(math.radians(current_angle)) * self.speed
        dy = math.sin(math.radians(current_angle)) * self.speed
        new_x = current_position[0] + dx
        new_y = current_position[1] + dy

        return (new_x, new_y), new_angle

class Straight_motion(Mobility):
    def __init__(self, speed: float = 0.5):
        super().__init__(speed)

    def move(self, current_position: Tuple[float, float], current_angle: float) -> Tuple[Tuple[float, float], float]:
        dx = math.cos(math.radians(current_angle)) * self.speed
        dy = math.sin(math.radians(current_angle)) * self.speed
        new_x = current_position[0] + dx
        new_y = current_position[1] + dy

        return (new_x, new_y), current_angle


