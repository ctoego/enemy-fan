import pygame
import option
WALL_c = (200, 0, 200)
ROAD_c = (51, 51, 51)
TABLE_c = (200, 120, 0)
DOOR_c = (200, 120, 0)
WINDOW_c = (124, 220, 254)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)




class Arrow(pygame.sprite.Sprite): #когда игрок берёт стену, предмет или т.п. около курсора получается 
    def __init__(self,  color = (51, 51, 51)):  # number номер клетки на котором он стоит
        from main import mousex, mousey, GRID
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



    def update(self): 
        from main import  OPT, screen, GRID, MAPS, game

        
        if OPT == "road":
            if self.size_image != GRID:
                self.size_image = GRID
                self.image = pygame.Surface((self.size_image, self.size_image))
            self.number = option.grids_config()
            self.Rect = pygame.Rect(MAPS[self.number]["x"], MAPS[self.number]["y"], GRID, GRID)
            self.rect.x, self.rect.y = MAPS[self.number]["x"], MAPS[self.number]["y"]
            self.image.fill(ROAD_c)
            screen.blit(self.image, self.Rect)

        elif OPT == "wall":
            self.number = option.grids_config()
            self.Rect = pygame.Rect(MAPS[self.number]["x"], MAPS[self.number]["y"], GRID, GRID)
            self.rect.x, self.rect.y = MAPS[self.number]["x"], MAPS[self.number]["y"]
            self.image.fill(WALL_c)
            screen.blit(self.image, self.Rect)
            if self.size_image != GRID:
                self.size_image = GRID
                self.image = pygame.Surface((self.size_image, self.size_image))
        elif OPT == "turret_1": 

            self.number = option.grids_config()
            self.Rect = pygame.Rect(MAPS[self.number]["x"], MAPS[self.number]["y"], GRID, GRID)
            self.rect.x, self.rect.y = MAPS[self.number]["x"], MAPS[self.number]["y"]
            self.image.fill(TABLE_c)
            screen.blit(self.image, self.Rect)
            if self.size_image != GRID:
                self.size_image = GRID
                self.image = pygame.Surface((self.size_image, self.size_image))

        elif OPT == "door":
            self.number = option.grids_config()
            self.Rect = pygame.Rect(MAPS[self.number]["x"], MAPS[self.number]["y"], GRID, GRID)
            self.rect.x, self.rect.y = MAPS[self.number]["x"], MAPS[self.number]["y"]
            self.image.fill(DOOR_c)
            screen.blit(self.image, self.Rect)
            if self.size_image != GRID:
                self.size_image = GRID
                self.image = pygame.Surface((self.size_image, self.size_image))

        elif OPT == "window":
            self.number = option.grids_config()
            self.Rect = pygame.Rect(MAPS[self.number]["x"], MAPS[self.number]["y"], GRID, GRID)
            self.rect.x, self.rect.y = MAPS[self.number]["x"], MAPS[self.number]["y"]
            self.image.fill(WINDOW_c)
            screen.blit(self.image, self.Rect)
            if self.size_image != GRID:
                self.size_image = GRID
                self.image = pygame.Surface((self.size_image, self.size_image))
