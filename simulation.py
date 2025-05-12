from vpython import *
from agents.predator import Predator
from agents.prey import Prey
from world import World

scene = canvas()
#initialize world
world = World()
number_of_predators = 10
number_of_prey = 50


field = box(pos=vector(world.width / 2, world.height / 2, 0),
            size=vector(world.width , world.height, 1),
            color=color.white)

#initialize population
for i in range(number_of_predators):
    world.add_predator(Predator(world))
for i in range(number_of_prey):
    world.add_prey(Prey(world))

#visualise animals
predator_objects = []
prey_objects = []

# FEEDBACK: ontkoppelen visualisatie en logic (eventueel met een dictionary)
# dictionary for visualisation
animal_to_object = {}

for predator in world.predators:
    pred_obj = sphere(pos=vector(predator.position[0], predator.position[1], 1), radius=1, color=color.red)
    predator_objects.append(pred_obj)
    animal_to_object[predator] = pred_obj

for prey in world.preys:
    prey_obj = sphere(pos=vector(prey.position[0], prey.position[1], 1), radius=0.5, color=color.green)
    prey_objects.append(prey_obj)
    animal_to_object[prey] = prey_obj


# scene setup
scene.title = "Predator-Prey model"
scene.height = 800
scene.width = 800
scene.background = color.black
scene.center = vector(world.width / 2, world.height / 2, 0)

# main loop
while True:
    rate(30)
    world.update()

    for predator in world.predators:
        obj = animal_to_object[predator]
        obj.pos = vector(predator.position[0], predator.position[1], 1)
        if predator.dead:
            obj.visible = False
            del obj
        #TODO

    for prey in world.preys:
        obj = animal_to_object[prey]
        obj.pos = vector(prey.position[0], prey.position[1], 1)
        # if prey.dead:
        # TODO

