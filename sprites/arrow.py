import pygame

WALL_c = (200, 0, 200)
ROAD_c = (51, 51, 51)
TABLE_c = (200, 120, 0)
DOOR_c = (200, 120, 0)
WINDOW_c = (124, 220, 254)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Arrow(pygame.sprite.Sprite): #когда игрок берёт стену, предмет или т.п. около курсора получается 
    def __init__(self, mousex, mousey, GRID, color = (51, 51, 51)):  # number номер клетки на котором он стоит

        pygame.sprite.Sprite.__init__(self)
        self.size_image = GRID
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.Rect = pygame.Rect(mousex, mousey, GRID, GRID)
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = mousex, mousey
        self.side = "pu"
    def write_blackground(self):
        return self.side



    def update(self, grids_config, OPT, screen, GRID, MAPS, VOLUME_WINDOW, VOLUME_TURRENT,WAVE, mousex, mousey): 

        if OPT == 1: 

            if VOLUME_TURRENT < 25 + WAVE:
                number = grids_config(MAPS, GRID, mousex, mousey)
                if number:
                    
                    self.rect.x, self.rect.y = number[0] * GRID, number[1] * GRID
                    self.Rect = pygame.Rect(self.rect.x, self.rect.y, GRID, GRID)
                    
                    self.image.fill(TABLE_c)
                    screen.blit(self.image, self.Rect)
                    if self.size_image != GRID:
                        self.size_image = GRID
                        self.image = pygame.Surface((self.size_image, self.size_image))
                


        elif OPT == 2:
            
            if VOLUME_WINDOW < 25 + WAVE:
                
                number = grids_config(MAPS, GRID, mousex, mousey)
                
                if number:
                    self.rect.x, self.rect.y = number[0] * GRID, number[1] * GRID
                    self.Rect = pygame.Rect(self.rect.x, self.rect.y, GRID, GRID)
                    
                    self.image.fill(WINDOW_c)
                    screen.blit(self.image, self.Rect)
                    if self.size_image != GRID:
                        self.size_image = GRID
                        self.image = pygame.Surface((self.size_image, self.size_image))
            
        
