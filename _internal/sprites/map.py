import pygame, random


class Map(pygame.sprite.Sprite): # спрайты карты
    '''Спрайт блока на карте, обазначается 0 в массиве'''
    def __init__(self, x, y, WIDTH, GRID): # number - номер клетки
        pygame.sprite.Sprite.__init__(self)
        color = random.choice([(0, 255, 0), (0, 250, 0), (0, 247, 0), (0, 243, 0)])
        self.size_image = WIDTH/76.8
        self.color = color
        self.color_n = color # дополнительный цвет
        
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.x = x * GRID
        self.y = y * GRID
        self.rect.x = self.x
        self.rect.y = self.y
        self.number = (x, y)
        self.Rect = pygame.Rect(self.x, self.y, GRID, GRID)
        
