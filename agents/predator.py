import random
import util
import math
from typing import Optional, Tuple
#from ABS.agents.animal import Animal
from agents.animal import Animal


class Predator(Animal):
    def __init__(self,
                 world,
                 position: Optional[Tuple[float, float]] = None,
                 vision_range: float = util.clip(17.0, 23.0, 20 + random.gauss(0, 1)), #max(17.0, min(23.0, random.gauss(20, 1))),
                 vision_width: Optional[float] = None):
        super().__init__(world, position)
        if not vision_width:
            vision_width = 20 + (3.33 * (20 - vision_range))
        vision_mutation = random.gauss(0, 1)
        # FEEDBACK: max + min -> clip function
        # ophopen van density aan de clipped edges van de gaussian
        #self.vision_range = max(17.0, min(23.0, vision_range + vision_mutation))
        self.vision_range = util.clip(17.0, 23.0, vision_range + vision_mutation)
        #self.vision_width = max(10.0, min(30.0, vision_width - (3.33 * vision_mutation)))
        self.vision_width = util.clip(10.0, 30.0, vision_width - (3.33 * vision_mutation))
        self.energy_consumption = 0.5 # how much energy spent each timestep when moving normally
        self.hunger = 0 # timesteps since last meal
        self.max_hunger = random.uniform(100, 300) # timesteps before dying of hunger
        self.reproduction_threshold = 3 #amount of prey to eat in order to reproduce
        self.eaten_prey = 0
        self.smell_strength = 6.0

        #CONE VISUAL
        #self.cone_position = (self.position[0] + math.cos(math.radians(self.vision_angle)) * self.vision_range,
        #                      self.position[1] + math.sin(math.radians(self.vision_angle)) * self.vision_range)


    def look_for_prey(self, preys):
        visible_preys = []
        if not self.resting:
            for prey in preys:
                dx = prey.position[0] - self.position[0]
                dy = prey.position[1] - self.position[1]
                distance = math.hypot(dx, dy) # 2D distance between predator and prey

                if distance <= self.vision_range:
                    angle_to_prey = math.degrees(math.atan2(dy, dx))
                    angle_diff = (angle_to_prey - self.vision_angle + 360) % 360
                    if angle_diff > 180:
                        angle_diff = 360 - angle_diff # smallest corner

                    if angle_diff <= self.vision_width / 2: # difference has to be smaller than width/2
                        visible_preys.append((prey, distance)) # because its visible now
        return visible_preys

    def smell_prey(self, preys):
        if not self.resting:
            for prey in preys:
                dx = prey.position[0] - self.position[0]
                dy = prey.position[1] - self.position[1]
                distance = math.hypot(dx, dy)

                if distance <= self.smell_strength:
                    self.vision_angle = math.degrees(math.atan2(dy,dx))

    def jump_attack(self, preys, world):
        visible_preys = self.look_for_prey(preys)
        if not visible_preys:
            return

        # search closest pray in vision
        closest_prey = None
        closest_distance = None
        for prey, distance in visible_preys:
            if closest_prey is None or distance < closest_distance:
                closest_prey = prey
                closest_distance = distance

        chance = 1 - (closest_distance / self.vision_range) ** 2 #exponential chance
        if chance < 0.1:
            chance = 0.1

        #if random.random() <= chance and self.energy > 50:
        if self.energy > 50:
            self.position = closest_prey.position
            if random.random() <= chance:
                closest_prey.dead = True
                #world.prey_dies(closest_prey)
                self.hunger = 0
                self.eaten_prey += 1

        self.energy -= 50
        if self.energy <= 0:
            self.energy = 0



    def update(self, world):
        self.smell_prey(world.preys)
        self.jump_attack(world.preys, world)
        super().update(world)

        #CONE VISUAL
        #self.cone_position = (self.position[0] + math.cos(math.radians(self.vision_angle)) * self.vision_range,
        #                      self.position[1] + math.sin(math.radians(self.vision_angle)) * self.vision_range)


        self.energy -= self.energy_consumption
        self.hunger += 1

        if self.hunger > self.max_hunger:
            self.dead = True

        if self.eaten_prey >= self.reproduction_threshold:
            self.reproduce(world)
            self.eaten_prey = 0

    def reproduce(self, world):
        new_predator = Predator(world,
                                self.position,
                                self.vision_range,
                                self.vision_width)
        # new_prey.vision_angle = random.uniform(0, 360)
        world.add_predator(new_predator)
        world.newborns.append(new_predator)




