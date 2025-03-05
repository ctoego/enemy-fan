import pygame
import random


class Zombie_1(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        from main import WIDTH, HEIGHT,GRID
        self.size_image = 25
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.image.fill((20, 140, 99))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,960)
        self.rect.y = 0
        self.speed = 0.5
        self.health = 100
        self.place_center = (WIDTH//2 - GRID//2, HEIGHT - GRID//2)

    def update(self):
        speed_curs_x = 0
        speed_curs_y = 0

        if self.rect.center[0] - self.place_center[0] > 0:
            speed_curs_x = 0
            speed_curs_x -= self.speed

        elif self.rect.center[0] - self.place_center[0] < 0:
            speed_curs_x = 0
            speed_curs_x += self.speed

        if self.rect.center[1] - self.place_center[1] > 10:
            speed_curs_y = 0
            speed_curs_y -= self.speed


        elif self.rect.center[1] - self.place_center[1] < -10:
            speed_curs_y = 0
            speed_curs_y += self.speed

        self.rect.x += speed_curs_x
        self.rect.y += speed_curs_y

        from main import game, all_sprites_window, all_sprites_bullet
        if game == False:self.kill()    #вышли из игры - удаляем спрайт


        if pygame.sprite.spritecollide(self, all_sprites_window, False):
            self.health -= 1
        else: self.speed = 0.5
        if pygame.sprite.spritecollide(self, all_sprites_bullet, False):
            self.health -= 50
       
        if self.health <= 0: self.kill()

class Zombie_2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        from main import GRID, WIDTH, HEIGHT
        self.image = pygame.Surface((GRID, GRID))
        self.image.fill((50, 145, 113)) 
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-200, -50)
        self.speed = 1
        self.health = 140
        self.place_center = (WIDTH//2 - GRID//2, HEIGHT - GRID//2)

    def update(self):
        speed_curs_x = 0
        speed_curs_y = 0

        if self.rect.center[0] - self.place_center[0] > 0:
            speed_curs_x = 0
            speed_curs_x -= self.speed

        elif self.rect.center[0] - self.place_center[0] < 0:
            speed_curs_x = 0
            speed_curs_x += self.speed

        if self.rect.center[1] - self.place_center[1] > 10:
            speed_curs_y = 0
            speed_curs_y -= self.speed


        elif self.rect.center[1] - self.place_center[1] < -10:
            speed_curs_y = 0
            speed_curs_y += self.speed

        self.rect.x += speed_curs_x
        self.rect.y += speed_curs_y
        from main import game,  all_sprites_window, all_sprites_bullet
        if game == False:self.kill()    #вышли из игры - удаляем спрайт

        if pygame.sprite.spritecollide(self, all_sprites_window, False):
            self.health -= 2
        else: self.speed = 1
        if pygame.sprite.spritecollide(self, all_sprites_bullet, False):
            self.health -= 50

        if self.health <= 0: self.kill()

class Zombie_3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        from main import GRID, WIDTH, HEIGHT
        self.image = pygame.Surface((GRID, GRID))
        self.image.fill((50, 145, 99)) 
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-200, -50)
        self.speed = 1
        self.health = 260
        self.place_center = (WIDTH//2 - GRID//2, HEIGHT - GRID//2)

    def update(self):
        speed_curs_x = 0
        speed_curs_y = 0

        if self.rect.center[0] - self.place_center[0] > 0:
            speed_curs_x = 0
            speed_curs_x -= self.speed

        elif self.rect.center[0] - self.place_center[0] < 0:
            speed_curs_x = 0
            speed_curs_x += self.speed

        if self.rect.center[1] - self.place_center[1] > 10:
            speed_curs_y = 0
            speed_curs_y -= self.speed


        elif self.rect.center[1] - self.place_center[1] < -10:
            speed_curs_y = 0
            speed_curs_y += self.speed

        self.rect.x += speed_curs_x
        self.rect.y += speed_curs_y
        from main import game,  all_sprites_window, all_sprites_bullet
        if game == False:self.kill()    #вышли из игры - удаляем спрайт

        if pygame.sprite.spritecollide(self, all_sprites_window, False):
            self.health -= 2
        else: self.speed = 1
        if pygame.sprite.spritecollide(self, all_sprites_bullet, False):
            self.health -= 50

        if self.health <= 0: self.kill()



class Zombie_4(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        from main import GRID, WIDTH, HEIGHT
        self.image = pygame.Surface((GRID, GRID))
        self.image.fill((50, 145, 99)) 
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-200, -50)
        self.speed = 1
        self.health = 520
        self.place_center = (WIDTH//2 - GRID//2, HEIGHT - GRID//2)

    def update(self):
        speed_curs_x = 0
        speed_curs_y = 0

        if self.rect.center[0] - self.place_center[0] > 0:
            speed_curs_x = 0
            speed_curs_x -= self.speed

        elif self.rect.center[0] - self.place_center[0] < 0:
            speed_curs_x = 0
            speed_curs_x += self.speed

        if self.rect.center[1] - self.place_center[1] > 10:
            speed_curs_y = 0
            speed_curs_y -= self.speed


        elif self.rect.center[1] - self.place_center[1] < -10:
            speed_curs_y = 0
            speed_curs_y += self.speed

        self.rect.x += speed_curs_x
        self.rect.y += speed_curs_y
        from main import game,  all_sprites_window, all_sprites_bullet
        if game == False:self.kill()    #вышли из игры - удаляем спрайт

        if pygame.sprite.spritecollide(self, all_sprites_window, False):
            self.health -= 1
        else: self.speed = 1
        if pygame.sprite.spritecollide(self, all_sprites_bullet, False):
            self.health -= 50

        if self.health <= 0: self.kill()