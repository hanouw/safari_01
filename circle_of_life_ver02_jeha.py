import random
import os

class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0

    def move(self, direction):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1

    def breed(self, x, y):
        return Animal(x, y)


class CircleOfLife:
    def __init__(self):
        self.world_size = 20
        self.grid = [[' ' for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.occupancy = [[False for _ in range(self.world_size)] for _ in range(self.world_size)]
        self.zebras = []
        self.lions = []
        self.timestep = 0

        for _ in range(10):  # Initialize 10 zebras at random positions
            x, y = self.get_random_empty_coordinates()
            zebra = Animal(x, y)
            self.zebras.append(zebra)
            self.grid[y][x] = 'Z'
            self.occupancy[y][x] = True

        for _ in range(2):  # Initialize 2 lions at random positions
            x, y = self.get_random_empty_coordinates()
            lion = Animal(x, y)
            self.lions.append(lion)
            self.grid[y][x] = 'L'
            self.occupancy[y][x] = True
    
    def get_random_empty_coordinates(self):
        while True:
            x = random.randint(0, self.world_size - 1)
            y = random.randint(0, self.world_size - 1)
            if not self.occupancy[y][x]:
                return x, y

    def display(self):
        print(f'Clock: {self.timestep}')

        # Print column coordinates at the top
        print(' ', end='')
        for i in range(1, self.world_size + 1):
            if i < 10:
                print(f' {i}', end='  ')
            elif i >= 10:
                print(f' {i}', end=' ')
        print()

        for i, line in enumerate(self.grid):
            print('ㅡ' * (self.world_size * 2 + 1))
            # Print row coordinate at the left
            print(f'{i + 1}|', end='')
            for cell in line:
                print(f' {cell} |', end='')
            print()
        print('ㅡ' * (self.world_size * 2 + 1))
        print()


    def step_move(self):
        for zebra in self.zebras:
            direction = random.choice(['up', 'down', 'left', 'right'])
            new_x = zebra.x
            new_y = zebra.y

            if direction == 'up':
                new_y -= 1
            elif direction == 'down':
                new_y += 1
            elif direction == 'left':
                new_x -= 1
            elif direction == 'right':
                new_x += 1

            if self.is_valid_move(new_x, new_y):
                self.move_animal(zebra, new_x, new_y)

        for lion in self.lions:
            direction = self.get_lion_direction(lion)

            if direction is not None:
                x, y = self.get_target_coordinates(lion, direction)
                target = self.grid[y][x]

                if target == 'Z':  # Lion eats zebra
                    self.remove_zebra(x, y)
                elif target == ' ':  # Lion moves to an empty space
                    self.move_animal(lion, x, y)

    def is_valid_move(self, x, y):
        return 0 <= x < self.world_size and 0 <= y < self.world_size and not self.occupancy[y][x]

    def move_animal(self, animal, new_x, new_y):
        self.grid[animal.y][animal.x] = ' '  # Clear the current position
        self.occupancy[animal.y][animal.x] = False

        animal.x = new_x
        animal.y = new_y

        self.grid[animal.y][animal.x] = 'Z' if animal in self.zebras else 'L'  # Update the new position
        self.occupancy[animal.y][animal.x] = True

    def get_lion_direction(self, lion):
        directions = ['up', 'down', 'left', 'right']
        random.shuffle(directions)

        for direction in directions:
            x, y = self.get_target_coordinates(lion, direction)

            if self.is_valid_move(x, y):
                target = self.grid[y][x]
                if target == 'Z':
                    return direction
                elif target == ' ':
                    return direction

        return None

    def get_target_coordinates(self, animal, direction):
        x = animal.x
        y = animal.y

        if direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1

        return x, y

    def remove_zebra(self, x, y):
        for zebra in self.zebras:
            if zebra.x == x and zebra.y == y:
                self.zebras.remove(zebra)
                break

        self.move_animal(self.lions, x, y)  # Lion moves to the eaten zebra's position

    def step_breed(self):
        for zebra in self.zebras:
            zebra.age += 1

            if zebra.age >= 3:
                x, y = self.get_random_empty_coordinates()
                new_zebra = zebra.breed(x, y)
                self.zebras.append(new_zebra)
                self.grid[y][x] = 'Z'
                self.occupancy[y][x] = True
                zebra.age = 0

        for lion in self.lions:
            lion.age += 1

            if lion.age >= 8:
                x, y = self.get_random_empty_coordinates()
                new_lion = lion.breed(x, y)
                self.lions.append(new_lion)
                self.grid[y][x] = 'L'
                self.occupancy[y][x] = True
                lion.age = 0

    def step(self):
        self.step_move()
        self.step_breed()
        self.timestep += 1


#--------------------------------------------------------------------------------------------------------------------------


    def run_simulation(self):
        self.display()
        while True:
            key = input("Press 'n' to show the next step or 'q' to quit: ")
            if key == 'n':
                os.system('cls')
                self.step()
                self.display()
            elif key == 'q':
                print("Quitting the simulation.")
                break
            else:
                print("Invalid input. Please try again.")

safari = CircleOfLife()  # Create an instance of CircleOfLife

safari.run_simulation()  # Run the simulation