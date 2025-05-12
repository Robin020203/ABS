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


# FEEDBACK: ontkoppelen visualisatie en logic (eventueel met een dictionary)
# dictionary for visualisation
animal_to_object = {}

for predator in world.predators:
    pred_obj = sphere(pos=vector(predator.position[0], predator.position[1], 1), radius=1, color=color.red)
    animal_to_object[predator] = pred_obj

for prey in world.preys:
    prey_obj = sphere(pos=vector(prey.position[0], prey.position[1], 1), radius=0.5, color=color.green)
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

    for baby in world.newborns:
        if isinstance(baby, Predator):
            pred_obj = sphere(pos=vector(baby.position[0], baby.position[1], 1), radius=1, color=color.red)
            animal_to_object[baby] = pred_obj
        elif isinstance(baby, Prey):
            prey_obj = sphere(pos=vector(baby.position[0], baby.position[1], 1), radius=0.5, color=color.green)
            animal_to_object[baby] = prey_obj
    world.newborns = []


    to_remove_predators = []
    for predator in world.predators:
        if predator in animal_to_object:
            obj = animal_to_object[predator]
            obj.pos = vector(predator.position[0], predator.position[1], 1)
            if predator.dead:
                obj.visible = False
                to_remove_predators.append(predator)
                # del obj
                # del animal_to_object[predator]
                #world.predator_dies(predator) # else predator was visible after death
    for predator in to_remove_predators:
        del animal_to_object[predator]
        world.predator_dies(predator)

    to_remove_preys = []
    for prey in world.preys:
        if prey in animal_to_object:
            obj = animal_to_object[prey]
            obj.pos = vector(prey.position[0], prey.position[1], 1)
            if prey.dead:
                obj.visible = False
                to_remove_preys.append(prey)
                # del obj
                # del animal_to_object[prey]
                #world.prey_dies(prey) # else prey was visible after death
    for prey in to_remove_preys:
        del animal_to_object[prey]
        world.prey_dies(prey)

    ### TEST ### -> error

    #for predator in world.predators:
    #    sphere_obj = animal_to_object[predator]
    #    visible_preys = predator.look_for_prey(world.preys)
    #    if visible_preys:
    #        sphere_obj.color = color.blue  # HUNT MODE
    #    else:
    #        sphere_obj.color = color.red  # WANDER MODE

    #for prey in world.preys:
    #    sphere_obj = animal_to_object[prey]
    #    visible_predators = prey.look_for_predator(world.predators)
    #    if visible_predators:
    #        sphere_obj.color = color.yellow  # SCARED MODE
    #    else:
    #        sphere_obj.color = color.green  # WANDER MODE