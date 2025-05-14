import random
import util
import math
from typing import Optional, Tuple
#from ABS.agents.animal import Animal
from agents.animal import Animal

class Prey(Animal):
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None,
                 vision_range: float = util.clip(7.0, 13.0, 10 + random.gauss(0, 1)), #max(7.0, min(13.0, random.gauss(10, 1))),
                 vision_width: Optional[float] = None):
        super().__init__(world, position)
        if not vision_width:
            vision_width = 180 + (6.66 * (10 - vision_range))
        vision_mutation = random.gauss(0, 1)
        # FEEDBACK: max + min -> clip function
        # ophopen van density aan de clipped edges van de gaussian
        #self.vision_range = max(7.0, min(13.0, vision_range + vision_mutation))
        self.vision_range = util.clip(7.0, 13.0, vision_range + vision_mutation)
        #self.vision_width = max(40.0, min(80.0, vision_width - (6.66 * vision_mutation)))
        self.vision_width = util.clip(40.0, 80.0, vision_width - (6.66 * vision_mutation))
        self.energy_consumption = 0.5
        self.time_alive = 0
        self.reproduction_threshold = random.uniform(200, 600)


    def look_for_predator(self, predators):
        visible_predators = []
        for predator in predators:
            dx = predator.position[0] - self.position[0]
            dy = predator.position[1] - self.position[1]
            distance = math.hypot(dx, dy) # 2D distance between predator and prey

            if distance <= self.vision_range:
                angle_to_predator = math.degrees(math.atan2(dy, dx))
                angle_diff = (angle_to_predator - self.vision_angle + 360) % 360
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff # smallest corner

                if angle_diff <= self.vision_width / 2: # difference has to be smaller than width/2
                    visible_predators.append((predator, distance)) # because its visible now
        return visible_predators

    def run_away_from_predators(self, predators):
        visible_predators = self.look_for_predator(predators)
        if not visible_predators or self.resting:
            return
        # average positions away from enemies
        avg_x = sum(predator.position[0] for predator, distance in visible_predators) / len(visible_predators)
        avg_y = sum(predator.position[1] for predator, distance in visible_predators) / len(visible_predators)

        # vector away from enemies
        dx = self.position[0] - avg_x
        dy = self.position[1] - avg_y
        length = math.hypot(dx, dy)

        if length > 0:
            dx = dx / length * self.speed
            dy = dy / length * self.speed
            self.position = (self.position[0] + dx, self.position[1] + dy)
            self.vision_angle = math.degrees(math.atan2(dy, dx))


    def update(self, world):
        self.run_away_from_predators(world.predators)
        super().update(world)
        self.energy -= self.energy_consumption
        self.time_alive += 1

        if self.time_alive >= self.reproduction_threshold:
            self.reproduce(world)
            self.time_alive = 0

        #if self.energy <= 0:
        #    self.dead = True

    def reproduce(self, world):
        number_of_babies = random.randint(1, 4) #random between 1 and 4 babies
        for baby in range(number_of_babies):
            new_prey = Prey(world,
                            self.position,
                            self.vision_range,
                            self.vision_width)
            #new_prey.vision_angle = random.uniform(0, 360)
            world.add_prey(new_prey)
            world.newborns.append(new_prey)