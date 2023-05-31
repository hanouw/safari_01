from animal_jeha import Animal


def print_TODO(todo):
    print(f'<<< NOT IMPLEMENTED: {todo} >>>')

class CircleOfLife:
    def __init__(self, world_size, num_zebras, num_lions):
        self.occupancy = [[False for _ in range(world_size)]
                          for _ in range(world_size)]
        print_TODO('get random empty coordinates')
        self.zebras = [Animal(0,0) for _ in range(num_zebras)]
        self.lions = [Animal(0,0) for _ in range(num_lions) ]
        self.timestep = 0
        print('Welcom to AIE Safari!')
        print(f'\tworld size = {world_size}')
        print(f'\tnumber of zebras = {len(self.zebras)}')
        print(f'\tnumber of zebras = {len(self.zebras)}')

    def __init__(self, world_size, num_zebras, num_lions):
        for position in world_size:
            date = 1
            print(f"  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 time step = {date}")
            print(num_zebras,num_lions)
            date += 1


    def display(self):
        print(f'Clock: {self.timestep}')
        print_TODO('display()')
        key = input('enter [q] to quit:')
        if key == 'q':
            exit()
        for animal in self.zeras:
            self.grid[animal.y][animal.x] = 'Z'
        for animal in self.liones:
            self.grid[animal.y][animal.x] = 'L'
        for line in self.grid:
            print(line)

    def step_move(self):
        print_TODO('step_move()')
        for zebra in self.zebras:
            print_TODO('get empty neighbor')
            direction = 'left'
            zebra.move(direction)
        for lion in self.lions:
            print_TODO('get neighboring zebra')
            print_TODO('move to zebra if found, else move to empty')
            print_TODO('get empty neighbor')
            direction = 'left'
            lion.move(direction)

    def step_breed(self):
        print_TODO('step_breed()')
        for animal in self.zebras + self.lions:
            print_TODO('get empty neighbor')
            x, y = 0,0
            animal.breed(x,y)



if __name__ == '__main__':
    safari = CircleOfLife(5,5,2)
    safari.display()
    safari.step_move()
    safari.step_breed()



'''
import os
os.system('cls')
# 모든 출력 사항 지우기
'''