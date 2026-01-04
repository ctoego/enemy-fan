import pygame

class Bullet_1(pygame.sprite.Sprite):
    '''Снаряды'''
    def __init__(self, x, y, x_place, y_place, GRID ):
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((GRID, GRID))
        self.image.fill((0, 0, 0 ))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.place_center = x_place, y_place
        self.ok = False
        self.speed_curs_x_h = 0
        self.speed_curs_y_h = 0
        self.time = 0   # сколько живёт пуля

        self.update_rate = 30  # Частота обновления (Гц)
        self.update_interval = 1000.0 / 90  # Интервал в мс
        
        self.last_update = pygame.time.get_ticks()

        self.direction = 1
    def update(self, all_sprites_zobies, GRID, WIDTH, HEIGHT):
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_update
        
        if elapsed >= self.update_interval:

            if pygame.sprite.spritecollideany(self, all_sprites_zobies) or self.time > 70: self.kill()    #если попали в зомби - удаляем спрайт
            if abs(self.rect.center[0] - self.place_center[0]) <= 20 and abs(self.rect.center[1] - self.place_center[1]) <= 20:
                self.ok = True

            if self.ok == False:
                speed_curs_x =  (self.place_center[0] - self.rect.center[0])//(GRID)
                speed_curs_y =(self.place_center[1] - self.rect.center[1])//(GRID)
                self.rect.center = self.rect.center[0] + speed_curs_x, self.rect.center[1] + speed_curs_y
                self.speed_curs_x_h = speed_curs_x
                self.speed_curs_y_h = speed_curs_y
            else:
                speed_curs_x = self.speed_curs_x_h
                speed_curs_y = self.speed_curs_y_h
            
                self.rect.x += speed_curs_x
                self.rect.y += speed_curs_y


            if self.rect.center[0] < -100 or self.rect.center[0] > WIDTH + 100 or self.rect.center[1] < -100 or self.rect.center[1] > HEIGHT + 100: self.kill()

            

            self.time +=1
            self.last_update = current_time
