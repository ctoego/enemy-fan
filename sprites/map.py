import pygame, random


class Map(pygame.sprite.Sprite): # спрайты карты
    '''Спрайт блока на карте, обазначается 0 в массиве'''
    def __init__(self, x, y, GRID): # number - номер клетки
        pygame.sprite.Sprite.__init__(self)
        color = random.choice([(0, 255, 0), (0, 250, 0), (0, 247, 0), (0, 243, 0)])

        self.color = color
        
        self.image = pygame.Surface((GRID, GRID))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.cell_x = x
        self.cell_y = y

        self.grid_x = x
        self.grid_y = y
        self.rect.x = x * GRID
        self.rect.y = y * GRID
        self.number = (x, y)
        self.Rect = pygame.Rect(self.grid_x, self.grid_y, GRID, GRID)