from animal import Animal

def print_TODO(todo):
    print(f'moving to {direction}. <<< NOT IMPLEMENTED YET >>>')

class CircleOfLife:
    def __init__(self, world_size, num_zebras, num_lions):
        self.occupancy = [[False for _ in range(world_size)]
                          for _ in range(world_size)]
        print_TODO('get random empty coordinates')
        self.zebras = [Animal(0,0) for _ in range(num_zebras)]
        self.lions = [Animal(0,0) for _ in range(num_lions) ]
        print('Welcom to AIE Safari!')
        print(f'\tworld size = {world_size}')
        print(f'\number of zebras = {len(self.zeberas)}')


if __name__ == '__main__':
    safari = CircleOfLife(5,5,2)
