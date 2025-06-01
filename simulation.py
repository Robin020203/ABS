from vpython import *
#import math #cone visual
from agents.predator import Predator
from agents.prey import Prey
from world import World
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

plot_update_interval = 20
frame_counter = 0
plt.switch_backend('TkAgg')
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))
fig.canvas.manager.window.attributes('-topmost', 1)
ax.set_title('Population')
ax.set_xlabel('Time')
ax.set_ylabel('Population')

time_data = []
prey_data = []
predator_data = []

line_prey, = ax.plot([], [], 'g-', label='Prey')
line_predator, = ax.plot([], [], 'r-', label='Predator')
ax.legend()

scene = canvas()
#initialize world
world = World()
number_of_predators = 5
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

#animal_to_cone = {}    #CONE VISUAL

for predator in world.predators:
    pred_obj = sphere(pos=vector(predator.position[0], predator.position[1], 1), radius=1, color=color.red)

    #cone_obj = cone(pos=vector(predator.cone_position[0],          #CONE VISUAL
    #                           predator.cone_position[1],
    #                           1),
    #                axis=vector(math.cos(math.radians(predator.vision_angle)) * -1,
    #                                           math.sin(math.radians(predator.vision_angle)) * -1,
    #                                           0),
    #                radius=predator.vision_width / 2,
    #                color=color.purple)

    #cone_obj = cylinder(pos=vector(predator.position[0],  #SMELL VISUAL
    #                               predator.position[1],
    #                               1),
    #                    axis=vector(0,0,1),
    #                    radius=7,
    #                    length=1,
    #                    color=color.purple,
    #                    opacity=0.5)

    animal_to_object[predator] = pred_obj

    #animal_to_cone[predator] = cone_obj                            #CONE VISUAL

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
try:
    while True:
        rate(30)
        frame_counter += 1
        world.update()

        if frame_counter % plot_update_interval == 0:
            time_data.append(world.timestep)
            prey_data.append(len(world.preys))
            predator_data.append(len(world.predators))

            line_prey.set_data(time_data, prey_data)
            line_predator.set_data(time_data, predator_data)

            if world.timestep > ax.get_xlim()[1] * 0.8:
                ax.set_xlim(0, world.timestep * 1.1)

            current_max = max(max(prey_data[-100:]), max(predator_data[-100:])) if prey_data and predator_data else 1
            if current_max > ax.get_ylim()[1] * 0.8:
                ax.set_ylim(0, current_max * 1.1)

            fig.canvas.draw()
            fig.canvas.flush_events()

        for baby in world.newborns:
            if isinstance(baby, Predator):
                pred_obj = sphere(pos=vector(baby.position[0], baby.position[1], 1), radius=1, color=color.red)
                animal_to_object[baby] = pred_obj
                number_of_predators += 1
            elif isinstance(baby, Prey):
                prey_obj = sphere(pos=vector(baby.position[0], baby.position[1], 1), radius=0.5, color=color.green)
                animal_to_object[baby] = prey_obj
                number_of_prey += 1
        world.newborns = []


        to_remove_predators = []
        for predator in world.predators:
            if predator in animal_to_object:
                obj = animal_to_object[predator]
                obj.pos = vector(predator.position[0], predator.position[1], 1)

                #if predator in animal_to_cone:                             #CONE VISUAL
                #    cone = animal_to_cone[predator]
                #    cone.pos = vector(predator.position[0], predator.position[1], 1)   #SMELL
                #    cone.pos = vector(predator.cone_position[0], predator.cone_position[1], 1) #VISION
                #    cone.axis = vector(math.cos(math.radians(predator.vision_angle)) * -1,
                #                       math.sin(math.radians(predator.vision_angle)) * -1,
                #                       0)

                if predator.dead:
                    obj.visible = False
                    to_remove_predators.append(predator)
                    # del obj
                    # del animal_to_object[predator]
                    #world.predator_dies(predator) # else predator was visible after death
        for predator in to_remove_predators:
            del animal_to_object[predator]
            world.predator_dies(predator)
            number_of_predators -= 1

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
            number_of_prey -= 1

        ### TEST ###

        if world.predators:
            for predator in world.predators:
                sphere_obj = animal_to_object[predator]
                if predator.resting:
                    sphere_obj.color = color.white  # REST MODE
                else:
                    visible_preys = predator.look_for_animals(world.preys)
                    if visible_preys:
                        sphere_obj.color = color.blue  # HUNT MODE
                    else:
                        sphere_obj.color = color.red  # WANDER MODE

        if world.preys:
            for prey in world.preys:
                sphere_obj = animal_to_object[prey]
                if prey.resting:
                    sphere_obj.color = color.white # REST MODE
                else:
                    visible_predators = prey.look_for_predator(world.predators)
                    if visible_predators:
                        sphere_obj.color = color.yellow  # SCARED MODE
                    else:
                        sphere_obj.color = color.green  # WANDER MODE
except Exception as e:
    print(f"Simulation ended: {str(e)}")
finally:
    plt.close("all")
