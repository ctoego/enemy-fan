import pygame
from core.state_game import G
from core.sprite_group import SG
from sprites.bullet import Bullet_1

class SimpleCannon(pygame.sprite.Sprite): 
    '''Простенькая пушка, стреляет при нажатие на Q'''
    def __init__(self, number_grid):  
        pygame.sprite.Sprite.__init__(self)
        self.number_grid = number_grid
        self.size_image_x = G.GRID
        self.size_image_y = G.GRID
        self.image = pygame.Surface((self.size_image_x, self.size_image_y))
        self.image.fill((200, 120, 0))
        self.rect = self.image.get_rect()
        self.rect.x = number_grid[0] * G.GRID
        self.rect.y = number_grid[1] * G.GRID
        self.time_s = 60 # через какое время может стрелять турэль
        self.time = 60

        self.update_rate = 60  # Частота обновления (Гц)
        self.update_interval = 1000.0 / 60  # Интервал в мс
        
        self.last_update = pygame.time.get_ticks()

        self.direction = 1
    def update(self, keys):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_update
        
        if elapsed >= self.update_interval:

            if  G.MAPS[self.number_grid[0]][ self.number_grid[1]] != 2:self.kill()    #если нет в списке -> удаляем
            self.time += 1
            if self.time >= self.time_s and keys[pygame.K_q]:
                bul = Bullet_1(self.rect.x, self.rect.y, G.world_mouse_x, G.world_mouse_y, G.GRID)      #type: ignore
                SG.all_sprites_bullet.add(bul)
                self.time = 0
            self.last_update = current_time

class SimpleCannonCard:
    '''Карта при выборе'''
    image = "card_w"     #! дописать
    text = 'Простая пушка'
    sprite = SimpleCannon