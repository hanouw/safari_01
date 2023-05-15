class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0

    def move(self, direction):
        print(f'moving to {direction}. <<< NOT IMPLEMENTED YET >>>')
        self.x += 1#------------------------------예시

    def breed(self, x, y):
        return Animal(x,y)

