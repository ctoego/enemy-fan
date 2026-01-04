import pygame
import random
import ctypes # узнаём разрешение экрана
import sys
import os
import numpy as np



# мой код

from game_ui.menu import Button_1, Button_2
from game_ui.level import SurferLevel
from game_ui.set import SurferSetting
from game_ui.option import grids_config, img


from sprites.arrow import Arrow
from sprites.map import Map
from sprites.window import Window
from sprites.bullet import Bullet_1 # класс для выстрелов
from data.data import Data

# спрайты зомби в папке zombies
from sprites.zombie_1 import Zombie_1, Zombie_2, Zombie_3, Zombie_4




DATA = Data()

# кол-во клеток
cell_count = 4800 # 96 x 50
# переменные для отчёта изменения при перемещении камеры
grid_x = 0
grid_y = 0



CONFIG = DATA.SETTING 

if CONFIG["resolution"] == "auto":
    geom_disp = ctypes.windll.user32 #* получаем разрешение монитора
    geom_disp.SetProcessDPIAware()
    WIDTHS = geom_disp.GetSystemMetrics(0) # ширина
    HEIGHTS = geom_disp.GetSystemMetrics(1) # высота

    if WIDTHS < 2560 and WIDTHS >= 1920 and HEIGHTS < 1440 and HEIGHTS >= 1080:
        WIDTH = 1920
        HEIGHT = 1080


    else:

        WIDTH = 1632
        HEIGHT = 918
        

elif CONFIG["resolution"] == "1920x1080":
    WIDTH = 1920
    HEIGHT = 1080
    
else:   #* в любом случае выбираем это, так же это вызовет искажённый файл настроек
    WIDTH = 1632
    HEIGHT = 918


FPS = DATA.SETTING['FPS_max']
GRID = WIDTH//96

GAME_HEIGHT = HEIGHT - GRID * 4
# Задаем цвета

WHITE = DATA.COLOR['WHITE']
BLACK = DATA.COLOR['BLACK']
RED = DATA.COLOR['RED']
GREEN = DATA.COLOR['GREEN']
BLUE = DATA.COLOR['BLUE']


pygame.font.init()
# Создаем игру и окно
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
screen.set_alpha(None)  #* отключаем альфа канал для производительности
pygame.display.set_caption("Enemy fan")
clock = pygame.time.Clock()

f1 = pygame.font.Font(None, 36)

mousex, mousey = pygame.mouse.get_pos() # курсор

#сетка

game = False # запущена ли у нас игра

LEVEL = False # какой уровень 

IMAGE = {"numbers": {}, #словарь с изображениями
        "background":{"main": ""},
        "buttons": {}, #словарь с кнопками
        "intro":[],
        "zombie": {
            "1": {
                "left": [],
                "right":[]
            },
            "2": {
                "left": [],
                "right":[]
            }
        }
        } 



IMAGE = img(IMAGE, WIDTH, HEIGHT, GRID)
MAPS = {} # словарь со значением о всех клетках на карте
OPT = 0  # переменная что хотим поставить

Zom_x = WIDTH//2 - GRID*2   #*куда должны идти зомби, координаты базы
Zom_y = GAME_HEIGHT - GRID*4

obj_btn_1 = []  #   для кнопок
obj_btn_2 = []
obj_btn_3 = []  #   выбор уровней

fin = len(IMAGE["intro"])




class Matrix(pygame.sprite.DirtySprite):
    def __init__(self, x, y, IMAGE):
        super().__init__()
        self.dirty = 2
        self.count = 0
        self.IMAGE = IMAGE
        self.image = random.choice(IMAGE["numbers"])
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Увеличиваем интервалы обновления
        self.count_finish = random.randint(5, 15)  # Мс вместо циклов
        self.last_change = pygame.time.get_ticks()
        
        # Добавляем флаг видимости для оптимизации
        self.is_visible = True
    
    def update(self):
        self.count += 1
        if self.count >= self.count_finish:
            old_center = self.rect.center
            self.image = random.choice(self.IMAGE["numbers"])
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.count = 0
            self.count_finish = random.randint(20, 40)
            self.dirty = 1  # Помечаем как измененный

class Turret_1(pygame.sprite.Sprite): 
    def __init__(self, number_grid):  
        pygame.sprite.Sprite.__init__(self)
        self.number_grid = number_grid
        self.size_image_x = GRID
        self.size_image_y = GRID
        self.image = pygame.Surface((self.size_image_x, self.size_image_y))
        self.image.fill((200, 120, 0))
        self.rect = self.image.get_rect()
        self.rect.x = number_grid[0] * GRID
        self.rect.y = number_grid[1] * GRID
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

            if  MAPS[self.number_grid[0], self.number_grid[1]] != 2:self.kill()    #если нет в списке -> удаляем
            self.time += 1
            if self.time >= self.time_s and keys[pygame.K_q]:
                global all_sprites_bullet
                bul = Bullet_1(self.rect.x, self.rect.y, mousex, mousey, GRID)
                all_sprites_bullet.add(bul)
                self.time = 0
            self.last_update = current_time





class Spawn(pygame.sprite.Sprite): # спрайт спавна наших юнитов( распологается на краю карты)
    def __init__(self, health):

        pygame.sprite.Sprite.__init__(self)
        self.size_image = GRID*4
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.image.fill((200, 120, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (Zom_x, Zom_y)
        self.health = health
        

        self.update_rate = 60  # Частота обновления (Гц)
        self.update_interval = 1000.0 / 60  # Интервал в мс
        
        self.last_update = pygame.time.get_ticks()

        self.direction = 1
    def update(self, all_sprites_zobies):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_update
        
        if elapsed >= self.update_interval:
            if pygame.sprite.spritecollideany(self, all_sprites_zobies):
                self.health -= 15
            self.last_update = current_time






def cret_new_game():

    
    global MAPS, VARIABLE,  all_sprites_map, WAVE, VOLUME_TURRENT, VOLUME_WINDOW, GAME_ZOMBIE, OPT, MAX_TURRENT, MAX_WINDOW, VICTORY



    VARIABLE = { # словарь с игровыми переменными 
            # что мы будем ставить
            "map": {"matrix": 0},
            "isolation": False, # выделение
            "menu_game_1": False, # открытие/закрытие кнопок выход и т.п.
            "menu_game_2": False, # открытие/закрытие кнопок деврации и т.п.
            
            "menu_game_4": False, # открыти/закрытие кнопок выбора строительства
            }  


    WAVE = 0 # номер волны
    GAME_ZOMBIE = True # начали ли мы игру
    OPT = 0
    MAPS = np.zeros((96, 50))   # двумерный массив numpy 
    all_sprites_map = pygame.sprite.Group()

    for x in range(96):
        for y in range(50):
            map = Map(x, y, WIDTH, GRID)
            all_sprites_map.add(map)




    VOLUME_TURRENT = 0 # кол-во турелей
    VOLUME_WINDOW = 0 # кол-во окон

    
    VICTORY = False # на уровнях, выйграли или нет
    MAX_TURRENT = 25 # максимальное количество вещей
    MAX_WINDOW  = 25
    # создаём новые группы спрайтов
    global  all_sprites_bullet
    global  all_sprites_spawn, all_sprites_window, all_sprites_zobies, all_sprites_turent


    all_sprites_window = pygame.sprite.Group()

    all_sprites_spawn = pygame.sprite.Group() # один на карту, куда идут юниты

    all_sprites_zobies = pygame.sprite.Group() # зомби
    all_sprites_bullet = pygame.sprite.Group() # снаряды
    all_sprites_turent = pygame.sprite.Group() # турели 
    global spawn
    spawn = Spawn(5000)
    all_sprites_spawn.add(spawn)
    z = Zombie_1(GRID, DATA, IMAGE)
    all_sprites_zobies.add(z)


def help(): 

    text = ["Помощь:", "Твоя задача защититься от врагов.", "У тебя для защиты есть несколько средств.",
            "1) Турели, при нажатии на Q начинает стрелять в сторону курсора.",
            "2) Битые стёкла, наносят небольшой урон. Не стоит на них полагаться.",
            "Враги всегда идут в одно место.",
            "Мало зомби? Просто нажми F2.",
            "Удачи"]
    pygame.draw.rect(screen, (196, 241, 149, 10), (GRID * 19, 10, GRID * 55, GRID * 17))
    i = 1
    for  line in text:
        text_surface = f1.render(line, True, (10, 10, 10))
        screen.blit(text_surface, (GRID * 20, GRID * i))
        i += 2


# курсор
arrow = Arrow(mousex, mousey, GRID)
all_sprites_arrow = pygame.sprite.Group();  all_sprites_arrow.add(arrow)



def open_game_menu_1(): 
    global VARIABLE
    if VARIABLE["menu_game_1"] == True: VARIABLE["menu_game_1"] = False
    else: VARIABLE["menu_game_1"] = True


button_1_game = Button_2(WIDTH//1.07, HEIGHT//1.13, WIDTH, HEIGHT,  open_game_menu_1)


button_open_turrent_1 = Button_2(WIDTH//3.5, HEIGHT//1.07, WIDTH, HEIGHT, None, "турели", True)



all_sprites_decoration_btn = pygame.sprite.Group()


button_open_window = Button_2(WIDTH//2.9, HEIGHT//1.07, WIDTH, HEIGHT, None, "битое стекло", True)



all_sprites_menu_game = pygame.sprite.Group()
all_sprites_menu_game.add(button_1_game,   button_open_turrent_1,  button_open_window)




def stop_game():    #! глобальная переменная
    global game; game = False
def full_stop_game(): sys.exit()#* Закрываем игру


btn_2_game = Button_1(WIDTH//1.5, HEIGHT//1.1 ,WIDTH//10 , HEIGHT//13 ,obj_btn_1,"выйти в меню", stop_game, 30 );obj_btn_1 = btn_2_game.loading_lis()    # ЗАБИРАЕМ СПИСОК

btn_3_game = Button_1(WIDTH//1.2, HEIGHT//1.1 ,WIDTH//10 , HEIGHT//13 ,obj_btn_1,"рабочий стол", full_stop_game, 30);obj_btn_1 = btn_3_game.loading_lis()    # ЗАБИРАЕМ СПИСОК


surf = pygame.Surface((WIDTH, GRID*5))

# прозрачная поверхность на главном меню, чтоб фон глаза не резал
surf_m = pygame.Surface((WIDTH, HEIGHT))



# кнопки в главном меню с текстом
def run_game(level): 
    
    cret_new_game() # создаём поле
    global game, LEVEL
    game = True
    LEVEL = level

btn_1_menu = Button_1(WIDTH//2, HEIGHT//2 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2,"бесконечность", lambda: (run_game(0)), 27);   obj_btn_2 = btn_1_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК
# кнопки в главном меню с текстом


def help_game():
    global help_open
    if help_open == True: help_open = False
    else: help_open = True #* открытие окна помощи

btn_2_menu = Button_1(WIDTH//2, HEIGHT//1.7 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2,"помощь", help_game);obj_btn_2 = btn_2_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК
def setting_game(): # TODO открытие настроек
    global setting_open
    setting_open = not setting_open

btn_3_menu = Button_1(WIDTH//3, HEIGHT//2 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2, "настройки", setting_game);   obj_btn_2 = btn_3_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК

def exit_game(): sys.exit() #* выход из игры

btn_4_menu = Button_1(WIDTH//3, HEIGHT//1.7 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2,"выход", exit_game); obj_btn_2 = btn_4_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК





def level_game(): 
    global level_open
    if level_open == True: level_open = False
    else: level_open = True #* открытие окна уровней
btn_6_menu = Button_1(WIDTH//1.2, HEIGHT//1.2 ,WIDTH//12 , HEIGHT//15 ,obj_btn_2,"уровни", level_game); obj_btn_2 = btn_6_menu.loading_lis()



help_open = False # открыли ли мы окно помощи
level_open = False # открыли ли мы окно уровней
setting_open = False # открыты ли настройки

all_sprites_matrix = pygame.sprite.Group()

def matrix(all_sprites_matrix):
    x_f = 0
    y_f = 0
    counter = 0
    for i in range(1296):     # создание матрицы на главном
        if counter >= 48:   x_f, y_f, counter = 0, y_f + GRID*2, 0

        map = Matrix(x_f, y_f, IMAGE)
        all_sprites_matrix.add(map)

        x_f +=GRID*2 # перемещаем на одну клетку
        counter +=1
    return all_sprites_matrix

all_sprites_matrix = matrix(all_sprites_matrix)

def endless_mode_render(screen):    # отрисовка
    all_sprites_map.draw(screen)
    all_sprites_spawn.draw(screen)

    all_sprites_window.draw(screen)
    all_sprites_turent.draw(screen)
    all_sprites_zobies.draw(screen)
    all_sprites_bullet.draw(screen)

def endless_mode_update_sprites():  # обновление спрайтов
    all_sprites_map.update()
    all_sprites_spawn.update(all_sprites_zobies)
    all_sprites_turent.update(keys)
    all_sprites_zobies.update(all_sprites_window, all_sprites_bullet)
    all_sprites_bullet.update(all_sprites_zobies, GRID, WIDTH, HEIGHT)
    
    
# очищаем группы спрайтов
def clear_sprites_group(all_sprites_map, all_sprites_window, all_sprites_spawn, all_sprites_turent, all_sprites_zobies,all_sprites_bullet):
    for sprite in all_sprites_map:
        sprite.kill()
        del sprite
    for sprite in all_sprites_window:
        sprite.kill()
        del sprite
    for sprite in all_sprites_spawn:
        sprite.kill()
        del sprite
    for sprite in all_sprites_turent:
        sprite.kill()
        del sprite
    for sprite in all_sprites_zobies:
        sprite.kill()
        del sprite
    for sprite in all_sprites_bullet:
        sprite.kill()
        del sprite


    return all_sprites_map, all_sprites_window, all_sprites_spawn, all_sprites_turent, all_sprites_zobies,all_sprites_bullet

class Create_zombie():
    @staticmethod
    def new_WAVE(all_sprites_zobies):
        if LEVEL == 0:
            if WAVE > 2:
                
                for i in range(random.randint(0, WAVE)):
                    zomb = Zombie_3(GRID, DATA, IMAGE)
                    all_sprites_zobies.add(zomb)
                for i in range(random.randint(0, WAVE)):
                    zomb = Zombie_2(GRID, DATA, IMAGE)
                    all_sprites_zobies.add(zomb)
            if WAVE > 5:
                rn = random.randint(0, WAVE)
                for i in range(rn):
                    zomb = Zombie_4(GRID, DATA, IMAGE)
                    all_sprites_zobies.add(zomb)
            if WAVE > 0:
                for i in range(random.randint(0, WAVE**2)):
                    zomb = Zombie_2(GRID, DATA, IMAGE)
                    all_sprites_zobies.add(zomb)
            
        elif LEVEL == 1: 
            enemy = [Zombie_1, Zombie_2, Zombie_3]
            for i in range(int(WAVE**1.5)):
                zomb = random.choice(enemy)(GRID, DATA, IMAGE)
                all_sprites_zobies.add(zomb)
        
        elif LEVEL == 2: 
            for i in range(int(WAVE**1.5)):
                zomb = random.choice([Zombie_1, Zombie_2])(GRID, DATA, IMAGE)
                all_sprites_zobies.add(zomb)
            for i in range(WAVE):
                zomb = random.choice([Zombie_3, Zombie_4])(GRID, DATA, IMAGE)
                all_sprites_zobies.add(zomb)

        return all_sprites_zobies

# TODO классы менюшек(выбора уровня, настроек)
surferlevel = SurferLevel(GRID) 
surfersetting = SurferSetting(GRID, DATA) 

clicking = 0



if DATA.SETTING['intro']:   
    for number in range(1, len(os.listdir("./image/intro"))):   # TODO заставка
        for event in pygame.event.get():
            
            # check for closing window
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        im = pygame.image.load(f"./image/intro/({number}).jpg").convert()
        im = pygame.transform.scale(im, (WIDTH, HEIGHT))
        clock.tick(30)
        screen.blit(im, (0, 0)) # фон 
        pygame.display.flip()  # Добавлен update экрана
    while True:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT: pygame.quit()
        if pygame.mouse.get_pressed()[0] : break  #TODO ждём пока пользователь не дочитает
        screen.fill((191, 0, 1))
        screen.blit(f1.render("Нажми на курсор.", True, (169, 218, 227)), (GRID*40 , GRID))
        screen.blit(f1.render("Всё будет хорошо.", True, (169, 218, 227)), (GRID , GRID*4))
        screen.blit(f1.render("Они уже здесь.", True, (169, 218, 227)), (GRID*10 , GRID*40))
        screen.blit(f1.render("«В одиночестве есть своя очень странная красота». — Лив Тайлер", True, (169, 218, 227)), (GRID*20 , GRID*10))
        
        screen.blit(f1.render("«Вчера я был умным, поэтому я хотел изменить мир. Сегодня я мудр, поэтому меняюсь я сам» — Майя Энджелоу", True, (169, 218, 227)), (GRID*10 , GRID*20))
        screen.blit(f1.render("«Я стала замечать гравитацию ещё в детстве» — Камерон Диаз", True, (169, 218, 227)), (GRID*20 , GRID*30))
        screen.blit(f1.render("«Спокойные люди имеют самые громкие мысли». — Стивен Хокинг", True, (169, 218, 227)), (GRID*40 , GRID*40))
        pygame.display.flip()


# Цикл игры
running = True
while running:
    
    mousex, mousey = pygame.mouse.get_pos() # курсор
    keys = pygame.key.get_pressed() # другой метод обработки нажатий
    # Держим цикл на правильной скорости

    dt = clock.tick(FPS) / 1000.0            # Разница во времени между кадрами (dt)
    
    # Ввод процесса (события)
    for event in pygame.event.get():
        
        # check for closing window
        if event.type == pygame.QUIT:   running = False
        if level_open:
            surferlevel.process(event, LEVEL)
            level_open = surferlevel.is_exit_pressed()
            
            if surferlevel.is_level_pressed != False:
                LEVEL = surferlevel.is_level_pressed()
                if LEVEL != False: 
                    level_open = False
                    run_game(LEVEL)
        if setting_open == True:
            surfersetting.process(event)
            setting_open = surfersetting.is_exit_pressed()


        if pygame.mouse.get_pressed()[0] and game == True:
            if (VOLUME_TURRENT < MAX_TURRENT or VOLUME_WINDOW < MAX_WINDOW):#TODO c каждой волной повышаем допустимое значение
                if OPT == 1:
                    if VOLUME_TURRENT < MAX_TURRENT:  #TODO c каждой волной повышаем допустимое значение
                        number_sp = grids_config(MAPS, GRID, mousex, mousey)
                        if number_sp:
                            if MAPS[number_sp[0]][number_sp[1]] == 0: 

                                player = Turret_1(number_sp)
                                MAPS[number_sp[0], number_sp[1]] = 2
                                all_sprites_turent.add(player)
                                VOLUME_TURRENT += 1


                elif OPT == 2:
                    if VOLUME_WINDOW < MAX_WINDOW:
                        number_sp = grids_config(MAPS, GRID, mousex, mousey)
                        if number_sp:
                            if MAPS[number_sp[0]][number_sp[1]] == 0:  # если на клетке уже есть  спрайт - ничего не делаем

                                win = Window(number_sp, GRID)
                                MAPS[number_sp[0], number_sp[1]] = 3
                                all_sprites_window.add(win)
                                VOLUME_WINDOW += 1

            if game == True:
                # выбираем турели
                if button_open_turrent_1.rect.collidepoint(mousex, mousey): 
                    OPT = 1
                elif button_open_window.rect.collidepoint(mousex, mousey): 
                    OPT = 2




    if game == True: 
        if GAME_ZOMBIE == True:
            if keys[pygame.K_DELETE]: # удаление объекта
                number_sp = grids_config(MAPS, GRID, mousex, mousey)
                
                if MAPS[number_sp[0], number_sp[1]] == 2: VOLUME_TURRENT -=1; MAPS[number_sp[0], number_sp[1]] = 0
                elif MAPS[number_sp[0], number_sp[1]] == 3: VOLUME_WINDOW -=1; MAPS[number_sp[0], number_sp[1]] = 0


                all_sprites_window.update(MAPS)


            # Обновление
            endless_mode_update_sprites()
            # Рендеринг


            endless_mode_render(screen)

            all_sprites_arrow.update(grids_config, OPT, screen, GRID, MAPS, VOLUME_WINDOW, VOLUME_TURRENT, WAVE, mousex, mousey)    #* что у нас на курсоре

            
            if keys[pygame.K_ESCAPE]: lbl = 0; OPT = 0; OPTCURSOR = "" #заменяем переменную

            if str(all_sprites_zobies) == "<Group(0 sprites)>": 
                all_sprites_zobies = Create_zombie.new_WAVE(all_sprites_zobies)
                WAVE += 1
                MAX_TURRENT +=1
                MAX_WINDOW += 1

            if spawn.health <= 0:   #* Завершение игры
                GAME_ZOMBIE = False 
                (   all_sprites_map, all_sprites_window,    #* выдаёт пустые группы
                    all_sprites_spawn, all_sprites_turent,
                    all_sprites_zobies,all_sprites_bullet) = clear_sprites_group(
                        all_sprites_map, all_sprites_window,
                        all_sprites_spawn, all_sprites_turent,
                        all_sprites_zobies,all_sprites_bullet)
            
            elif WAVE > 10 and LEVEL != 0: #*если не на уровнях -> завершаем игру
                VICTORY = True
                GAME_ZOMBIE = False 
                DATA.SAVE["level"][f'{LEVEL}'] = True
                LEVEL = False
                DATA.save_game()
            if keys[pygame.K_F2]: #? если очень хочется, можно создать ещё зомби
                zomb = Zombie_2(GRID, DATA, IMAGE)
                all_sprites_zobies.add(zomb)

            
            screen.blit(f1.render(f'Волна: {WAVE}', True, (180, 0, 0)), (10, GRID*5))

            screen.blit(f1.render(f'Доступно битых окон: {MAX_WINDOW - VOLUME_WINDOW}', True, (180, 0, 0)), (10, GRID*7))

            screen.blit(f1.render(f'Доступно орудий: {MAX_TURRENT - VOLUME_TURRENT}', True, (180, 0, 0)), (10, GRID*9))
            screen.blit(f1.render(f'Здоровье: {spawn.health}', True, (180, 0, 0)), (10, GRID*11))

        elif VICTORY:
            pygame.draw.rect(screen, (64, 128, 255), (0, 0, WIDTH, HEIGHT))
            screen.blit(f1.render("Победа!!!", True, (180, 0, 0)), (WIDTH//2, HEIGHT//2))
            VARIABLE["menu_game_1"] = True
        else:
            pygame.draw.rect(screen, (64, 128, 255), (0, 0, WIDTH, HEIGHT))
            WAVE_text = f1.render("Ты проиграл!", True, (180, 0, 0))
            screen.blit(WAVE_text, (WIDTH//2, HEIGHT//2))
            VARIABLE["menu_game_1"] = True



        surf.fill(RED)  # Заполнение фона, цвет


        screen.blit(surf, (0, HEIGHT- 90))
        if VARIABLE["menu_game_1"]:
            for object in obj_btn_1:  object.process()

        # обнолвляем и выводим кнопки в одном месте
        all_sprites_menu_game.draw(screen)
        all_sprites_menu_game.update()
        if VARIABLE["menu_game_2"]:
            all_sprites_decoration_btn.draw(screen)
            all_sprites_decoration_btn.update()




    else: # если не играем

        all_sprites_matrix.update()
        changed_rects = all_sprites_matrix.draw(screen)
        pygame.display.update(changed_rects)  # Обновляем только измененные области
        surf_m.fill(BLACK)  # Заполнение фона, цвет

        surf_m.set_alpha(100)# прозрачность

        screen.blit(surf_m, (0, 0))
        if level_open: surferlevel.render(screen, dt)
        elif setting_open: surfersetting.render(screen, dt)
        else:
            for object in obj_btn_2:  object.process(screen)  # рисуем кнопки
            if help_open == True: help()


    if CONFIG["FPS_see"] == True:

        fps_text = f1.render(f"fps: {int(clock.get_fps())}", True, (180, 0, 0))
        screen.blit(fps_text, (10, 10))
    if keys[pygame.K_F7]: FPS = 200
    if keys[pygame.K_F8]: FPS = 60
    if keys[pygame.K_F6]: print(all_sprites_zobies)
    if keys[pygame.K_F1]: WAVE = 10
    pygame.display.flip()   # обновляем все поверхности



pygame.quit()
sys.exit()
