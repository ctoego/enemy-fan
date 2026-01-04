import pygame
import random
import math

class BaseZombie(pygame.sprite.Sprite):
    """Оптимизированный базовый класс для зомби с анимацией"""
    
    def __init__(self, size, color, speed, health, animations = None):
        super().__init__()
        from main import WIDTH, Zom_x, Zom_y, HEIGHT
        
        # Оптимизация: используем словарь анимаций
        self.animations = animations  
        self.current_anim = 'right'  # Начальная анимация
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 2  # Каждые 4 обновления - новый кадр
        
        self.width = WIDTH
        if animations:
            # Берем первый кадр первой анимации
            self.image = animations['right'][0]
            self.anim = True
            self.anim_frames = animations['right']  # Текущие кадры
        else:
            # Статичное изображение
            self.image = pygame.Surface((size, size))
            self.image.fill(color)
            self.anim = False
            self.anim_frames = None
        
        # Создаем rect только один раз
        self.rect = self.image.get_rect()
        side = random.randint(0, 2)  # 0: верх, 1: право, 2: лево
        
        if side == 0:  # Верх
            self.rect.x = random.randint(-50, WIDTH + 50)
            self.rect.y = random.randint(-200, -50)
        elif side == 1:  # Право
            self.rect.x = random.randint(WIDTH + 10, WIDTH + 100)
            self.rect.y = random.randint(-50, int(HEIGHT//1.5))

        else:  # Лево
            self.rect.x = random.randint(-100, -10)
            self.rect.y = random.randint(-50, int(HEIGHT//1.5))
        self.x = self.rect.x
        self.y = self.rect.y

        target_offset_x = random.randint(-40, 40)  # Случайное смещение по X
        target_offset_y = random.randint(-60, 60)  # Случайное смещение по Y

        # Характеристики
        self.speed = speed
        self.health = health
        self.place_center = (Zom_x + target_offset_x, Zom_y + target_offset_y)
        self.base_speed = speed
        self.window_damage = 1
        self.bullet_damage = 50
        
        # Оптимизация: предрассчитанные значения
        self.half_width = self.rect.width // 2
        self.half_height = self.rect.height // 2
        
        # Оптимизация: кэширование предыдущих значений
        self.last_dx = 0
        self.last_dy = 0


        # Время
        self.last_update = pygame.time.get_ticks()
    
    def update_direction(self, speed_x):
        """Определяем направление и меняем анимацию"""
        if not self.animations:
            return
        
        old_direction = self.current_anim
        
        # Определяем направление по движению
        if speed_x < 0:
            self.current_anim = 'right'
        elif speed_x > 0:
            self.current_anim = 'left'
        # Если стоит на месте, не меняем направление
        
        # Если направление изменилось, обновляем кадры
        if old_direction != self.current_anim:
            self.anim_frames = self.animations[self.current_anim]
            self.anim_index = 0  # Начинаем анимацию сначала
    
    def update_animation(self):
        """Оптимизированное обновление анимации"""
        if not self.anim or not self.anim_frames:
            return
        
        self.anim_timer += 1
        
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            
            # Переход к следующему кадру
            next_index = self.anim_index + 1
            if next_index >= len(self.anim_frames):
                next_index = 0
            
            # Меняем кадр только если он действительно изменился
            if next_index != self.anim_index:
                self.anim_index = next_index
                
                # Оптимизация: сохраняем старую позицию без пересчета center
                old_x, old_y = self.rect.x, self.rect.y
                
                # Меняем изображение
                self.image = self.anim_frames[self.anim_index]
                
                # Восстанавливаем позицию напрямую (быстрее чем через center)
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = old_x, old_y

    def calculate_movement_optimized(self):

        dx = self.place_center[0] - self.rect.centerx
        dy = self.place_center[1] - self.rect.centery

        angle = math.atan2(dy, dx)

        vy = round(self.speed * math.sin(angle))
        vx = round(self.speed * math.cos(angle))
        return vx , vy
    
    def update(self, all_sprites_window, all_sprites_bullet):
        """Оптимизированное обновление"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_update
        
        if elapsed >= 16:  # ~60 FPS, фиксированный интервал быстрее чем деление
            # Получаем движение
            speed_x, speed_y = self.calculate_movement_optimized()
            
            # Определяем направление для анимации
            self.update_direction(speed_x)
            
            # Движение
            self.rect.x += speed_x
            self.rect.y += speed_y
            
            # Обновляем анимацию
            self.update_animation()
            
            # Проверяем столкновения
            self.health -= self.check_window_collisions(all_sprites_window)
            
            # Столкновения с пулями
            bullet_hit = self.check_bullet_collisions(all_sprites_bullet)
            if bullet_hit:
                self.health -= self.bullet_damage
            
            # Проверка здоровья
            if self.health <= 0:
                self.kill()
                return
            
            self.last_update = current_time
    
    def check_window_collisions(self, all_sprites_window):
        """Оптимизированная проверка столкновений с окнами"""
        # Быстрая проверка с rect-пересечением перед точной проверкой
        for window in all_sprites_window:
            if self.rect.colliderect(window.rect):
                return self.window_damage
        self.speed = self.base_speed
        return 0
    
    def check_bullet_collisions(self, all_sprites_bullet):
        """Оптимизированная проверка столкновений с пулями"""
        # Используем маску для более точной проверки если нужно
        for bullet in all_sprites_bullet:
            if self.rect.colliderect(bullet.rect):
                bullet.kill()
                return True
        return False


class Zombie_1(BaseZombie):
    """Быстрый, но слабый зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):

        super().__init__(

            animations = IMAGE['zombie']['1'],

            size = 25,
            color = (20, 140, 99),
            speed = DATA.CONFIG['Zombie_1']['speed'],
            health = DATA.CONFIG['Zombie_1']['health']
        )
        

        self.window_damage = DATA.CONFIG['Zombie_1']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_1']['bullet_damage']


class Zombie_2(BaseZombie):
    """Средний зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):
        
        super().__init__(
            size=GRID,
            animations = IMAGE['zombie']['2'],
            color = (50, 145, 113),
            speed = DATA.CONFIG['Zombie_2']['speed'],
            health = DATA.CONFIG['Zombie_2']['health']
        )
        self.window_damage = DATA.CONFIG['Zombie_2']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_2']['bullet_damage']


class Zombie_3(BaseZombie):
    """Тяжелый зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):

        super().__init__(
            size=GRID,
            color=(50, 145, 99),
            speed = DATA.CONFIG['Zombie_3']['speed'],
            health = DATA.CONFIG['Zombie_3']['health']
        )
        self.window_damage = DATA.CONFIG['Zombie_3']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_3']['bullet_damage']


class Zombie_4(BaseZombie):
    """Босс-зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):

        super().__init__(
            size=GRID,
            color=(50, 145, 99),
            speed = DATA.CONFIG['Zombie_4']['speed'],
            health = DATA.CONFIG['Zombie_4']['health']
        )
        self.window_damage = DATA.CONFIG['Zombie_4']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_4']['bullet_damage']

class Zombie_5(BaseZombie):
    """Босс-зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):

        super().__init__(
            size=GRID,
            color=(50, 145, 99),
            speed = DATA.CONFIG['Zombie_5']['speed'],
            health = DATA.CONFIG['Zombie_5']['health']
        )
        self.window_damage = DATA.CONFIG['Zombie_5']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_5']['bullet_damage']

class Zombie_6(BaseZombie):
    """Босс-зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):

        super().__init__(
            size=GRID,
            color=(50, 145, 99),
            speed = DATA.CONFIG['Zombie_6']['speed'],
            health = DATA.CONFIG['Zombie_6']['health']
        )
        self.window_damage = DATA.CONFIG['Zombie_6']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_6']['bullet_damage']


class Zombie_7(BaseZombie):
    """Босс-зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):

        super().__init__(
            size=GRID,
            color=(50, 145, 99),
            speed = DATA.CONFIG['Zombie_7']['speed'],
            health = DATA.CONFIG['Zombie_7']['health']
        )
        self.window_damage = DATA.CONFIG['Zombie_7']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_7']['bullet_damage']


class Zombie_8(BaseZombie):
    """Босс-зомби"""
    
    def __init__(self, GRID, DATA, IMAGE):

        super().__init__(
            size=GRID,
            color=(50, 145, 99),
            speed = DATA.CONFIG['Zombie_8']['speed'],
            health = DATA.CONFIG['Zombie_8']['health']
        )
        self.window_damage = DATA.CONFIG['Zombie_8']['window_damage']
        self.bullet_damage = DATA.CONFIG['Zombie_8']['bullet_damage']