
import pygame


class Window(pygame.sprite.Sprite): # окна
    
    def __init__(self,  number, GRID):
        pygame.sprite.Sprite.__init__(self)
        
        self.size_image = 20
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.image.fill((114, 200, 244))
        self.rect = self.image.get_rect()
        self.number = number
        self.health = 500
        self.rect.x = number[0] * GRID
        self.rect.y = number[1] * GRID

    def update(self, MAPS):

        if MAPS[self.number[0], self.number[1]] == False or self.health <= 0:self.kill()    #если нет в списке -> удаляем

