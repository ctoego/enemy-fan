import pygame, random
from core.data import Data

class Map(pygame.sprite.Sprite): # спрайты карты
    '''Спрайт блока на карте, обазначается 0 в массиве'''
    def __init__(self, x, y, GRID, style: str): 
        pygame.sprite.Sprite.__init__(self)
        try:
            self.bg_color = random.choice(Data.STYLE[style]['bg_color'])
        except KeyError:
            print(f"Error:  map.py class Map: I can't see the color")
            self.bg_color = (24, 243, 46)

        self.image = pygame.Surface((GRID, GRID))
        try:
            self.image.fill(self.bg_color)
        except ValueError:
            self.image.fill((24, 243, 46))
            print(f"Error:  map.py class Map: invalid color")
        self.rect = self.image.get_rect()

        self.cell_x = x
        self.cell_y = y

        self.grid_x = x
        self.grid_y = y
        self.rect.x = x * GRID
        self.rect.y = y * GRID
        self.number = (x, y)
        self.Rect = pygame.Rect(self.grid_x, self.grid_y, GRID, GRID)