import os
import random

class CircleOfLife:
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

    def display(self):
        print(f'time step: {self.timestep}')

        # 행 번호 표시하기
        print(' ', end='')
        for i in range(1, self.world_size + 1):
            if i < 10:
                print(f' {i}', end='  ')
            elif i >= 10:
                print(f' {i}', end=' ')
        print()

        for i, line in enumerate(self.grid): # 열 번호 표시하기
            print('ㅡ' * (self.world_size * 2 + 1))
            if i < 9:
                print(f'{i + 1} |', end='')
            else:
                print(f'{i + 1}|', end='')
            for cell in line:
                print(f' {cell} |', end='')
            print()
        print('ㅡ' * (self.world_size * 2 + 1))
        print()

    def step_move(self):
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
                for zebra in self.zebras:
                    if zebra.x == lion.x and zebra.y == lion.y:
                        self.zebras.remove(zebra)

                lion.survival_count += 1
                lion.hungry_count = 0
                if lion.hungry_count == 3:
                    self.kill_lion(lion)

            if lion.survival_count == 8:
                self.reproduce_lion(lion)
                

            if not possible_directions:
                if lion.x == 0 and lion.y == 0:
                    direction = random.choice(['down', 'right'])
                elif lion.x == self.world_size and lion.y == self.world_size:
                    direction = random.choice(['up', 'left'])
                elif lion.x == 0 and lion.y == self.world_size:
                    direction = random.choice(['up', 'right'])
                elif lion.x == self.world_size and lion.y == 0:
                    direction = random.choice(['left', 'down'])
    #--------------------------------------------------------------
                elif lion.x == 0 and (lion.y != 0 or lion.y != world_size):
                    direction = random.choice(['up', 'down', 'right'])
                elif lion.x == self.world_size and (lion.y != 0 or lion.y != self.world_size):
                    direction = random.choice(['up', 'down', 'left'])

                elif (lion.x != 0 or lion.x != self.world_size) and lion.y == 0:
                    direction = random.choice(['down', 'left', 'right'])
                elif (lion.x != 0 or lion.x != self.world_size) and lion.y == self.world_size:
                    direction = random.choice(['up', 'left', 'right'])
    #---------------------------------------------------------------
                else:
                    direction = random.choice(['up', 'down', 'left', 'right'])

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
                

                if lion.survival_count == 8:
                    self.reproduce_lion(lion)

                lion.hungry_count += 1

            if lion.hungry_count >= 3:
                self.kill_lion(lion)

        for zebra in self.zebras:
            if zebra.x == 0 and zebra.y == 0:
                direction = random.choice(['down', 'right'])
            elif zebra.x == self.world_size and zebra.y == self.world_size:
                direction = random.choice(['up', 'left'])
            elif zebra.x == 0 and zebra.y == self.world_size:
                direction = random.choice(['up', 'right'])
            elif zebra.x == self.world_size and zebra.y == 0:
                direction = random.choice(['left', 'down'])
#--------------------------------------------------------------
            elif zebra.x == 0 and (zebra.y != 0 or zebra.y != world_size):
                direction = random.choice(['up', 'down', 'right'])
            elif zebra.x == self.world_size and (zebra.y != 0 or zebra.y != self.world_size):
                direction = random.choice(['up', 'down', 'left'])

            elif (zebra.x != 0 or zebra.x != self.world_size) and zebra.y == 0:
                direction = random.choice(['down', 'left', 'right'])
            elif (zebra.x != 0 or zebra.x != self.world_size) and zebra.y == self.world_size:
                direction = random.choice(['up', 'left', 'right'])
#---------------------------------------------------------------
            else:
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
                    possible_directions.append((new_x, new_y))

        if possible_directions:
            new_x, new_y = random.choice(possible_directions)
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

                # 환경 경계 처리
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


    def run_simulation(self):
        self.display()
        while True:
            if len(self.zebras) == 0:
                print("Zebra가 멸종되었습니다")
                break
            if len(self.lions) == 0:
                print("Lion이 멸종되었습니다")
                break   

            key = input("아무 버튼이나 눌러서 다음 timestep을 실행하거나 'q'를 눌러 마치세요: ")
            if key == 'q':
                print("시뮬레이션을 종료합니다.")
                break
            else:
                os.system('cls')
                self.step_move()
                self.display()
                print(f'남은 lion 수: {len(self.lions)}, 남은 zebra 수: {len(self.zebras)}')

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
num_zebras = 20
num_lions = 7

world = CircleOfLife(world_size, num_zebras, num_lions)
world.run_simulation()
