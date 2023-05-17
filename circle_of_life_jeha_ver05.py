import os
import random

class World:
    def __init__(self, world_size, num_zebras, num_lions):
        self.world_size = world_size
        self.grid = [[' ' for _ in range(world_size)] for _ in range(world_size)]
        self.occupancy = [[False for _ in range(world_size)] for _ in range(world_size)]
        self.zebras = []
        self.lions = []
        self.timestep = 0

        for _ in range(num_zebras):
            self.add_zebra()
        
        for _ in range(num_lions):
            self.add_lion()

    def add_zebra(self):
        x = random.randint(0, self.world_size - 1)
        y = random.randint(0, self.world_size - 1)

        while self.occupancy[y][x]:
            x = random.randint(0, self.world_size - 1)
            y = random.randint(0, self.world_size - 1)

        zebra = Zebra(x, y)
        self.grid[y][x] = 'Z'
        self.occupancy[y][x] = True
        self.zebras.append(zebra)

    def add_lion(self):
        x = random.randint(0, self.world_size - 1)
        y = random.randint(0, self.world_size - 1)

        while self.occupancy[y][x]:
            x = random.randint(0, self.world_size - 1)
            y = random.randint(0, self.world_size - 1)

        lion = Lion(x, y)
        self.grid[y][x] = 'L'
        self.occupancy[y][x] = True
        self.lions.append(lion)

    def step_move(self):
        for zebra in self.zebras:
            direction = random.choice(['up', 'down', 'left', 'right'])
            new_x = zebra.x
            new_y = zebra.y

            if direction == 'up':
                new_y = (new_y - 1) % self.world_size
            elif direction == 'down':
                new_y = (new_y + 1) % self.world_size
            elif direction == 'left':
                new_x = (new_x - 1) % self.world_size
            elif direction == 'right':
                new_x = (new_x + 1) % self.world_size

            if not self.occupancy[new_y][new_x]:
                self.grid[zebra.y][zebra.x] = ' '
                self.grid[new_y][new_x] = 'Z'
                self.occupancy[zebra.y][zebra.x] = False
                self.occupancy[new_y][new_x] = True
                zebra.x = new_x
                zebra.y = new_y
                zebra.survival_count += 1

                if zebra.survival_count == 3:
                    self.reproduce_zebra(zebra)

        for lion in self.lions:
            possible_directions = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    new_x = (lion.x + dx) % self.world_size
                    new_y = (lion.y + dy) % self.world_size

                    if self.grid[new_y][new_x] == 'Z':
                        possible_directions.append((dx, dy))

            if possible_directions:
                dx, dy = random.choice(possible_directions)
                new_x = (lion.x + dx) % self.world_size
                new_y = (lion.y + dy) % self.world_size

                self.grid[lion.y][lion.x] = ' '
                self.grid[new_y][new_x] = 'L'
                self.occupancy[lion.y][lion.x] = False
                self.occupancy[new_y][new_x] = True
                lion.x = new_x
                lion.y = new_y
                lion.survival_count += 1

                if lion.survival_count == 8:
                    self.reproduce_lion(lion)

            else:
                direction = random.choice(['up', 'down', 'left', 'right'])
                new_x = lion.x
                new_y = lion.y

                if direction == 'up':
                    new_y = (new_y - 1) % self.world_size
                elif direction == 'down':
                    new_y = (new_y + 1) % self.world_size
                elif direction == 'left':
                    new_x = (new_x - 1) % self.world_size
                elif direction == 'right':
                    new_x = (new_x + 1) % self.world_size

                if not self.occupancy[new_y][new_x]:
                    self.grid[lion.y][lion.x] = ' '
                    self.grid[new_y][new_x] = 'L'
                    self.occupancy[lion.y][lion.x] = False
                    self.occupancy[new_y][new_x] = True
                    lion.x = new_x
                    lion.y = new_y
                    lion.survival_count += 1

                    if lion.survival_count == 8:
                        self.reproduce_lion(lion)

                    if lion.survival_count == 3:
                        lion.hungry_count += 1
                        if lion.hungry_count == 3:
                            self.kill_lion(lion)

        self.timestep += 1



    def reproduce_zebra(self, zebra):
        possible_directions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = zebra.x + dx
                new_y = zebra.y + dy

                # Wrap around
                new_x = new_x % self.world_size
                new_y = new_y % self.world_size

                if not self.occupancy[new_y][new_x]:
                    self.grid[new_y][new_x] = 'Z'
                    self.occupancy[new_y][new_x] = True
                    new_zebra = Zebra(new_x, new_y)
                    self.zebras.append(new_zebra)
                    zebra.survival_count = 0

    def reproduce_lion(self, lion):
        possible_directions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = lion.x + dx
                new_y = lion.y + dy

                # Wrap around
                new_x = new_x % self.world_size
                new_y = new_y % self.world_size

                if not self.occupancy[new_y][new_x]:
                    possible_directions.append((new_x, new_y))

        if possible_directions:
            new_x, new_y = random.choice(possible_directions)
            self.grid[new_y][new_x] = 'L'
            self.occupancy[new_y][new_x] = True
            new_lion = Lion(new_x, new_y)
            self.lions.append(new_lion)
            lion.survival_count = 0

    def kill_lion(self, lion):
        self.grid[lion.y][lion.x] = ' '
        self.occupancy[lion.y][lion.x] = False
        self.lions.remove(lion)

    def print_world(self):
        print("Time step:", self.timestep)
        for row in self.grid:
            print(' '.join(row))
        print()

    def run_simulation(self):
        self.print_world()
        while True:
            key = input("Press any button to show the next step or 'q' to quit: ")
            if key == 'q':
                print("Quitting the simulation.")
                break
            else:
                os.system('cls')
                self.step_move()
                self.print_world()

class Zebra:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.survival_count = 0

class Lion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.survival_count = 0
        self.hungry_count = 0

world_size = 20
num_zebras = 5
num_lions = 3
num_steps = 10

world = World(world_size, num_zebras, num_lions)
world.run_simulation()


               
