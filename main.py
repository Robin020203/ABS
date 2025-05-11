from world import World
from agents.predator import Predator
from agents.prey import Prey

class Main:
    def __init__(self):
        self.world = World()
        self.number_of_predators = 10
        self.number_of_prey = 50

    def initialize_population(self):
        for i in range(self.number_of_predators):
            self.world.add_predator(Predator(self.world))
        for i in range(self.number_of_prey):
            self.world.add_prey(Prey(self.world))

    def run(self, timesteps: int = 1000):
        self.initialize_population()

        for i in range(timesteps):
            self.world.update()

if __name__ == '__main__':
    sim = Main()
    sim.run()

