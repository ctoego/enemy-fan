import pygame
import random
import ctypes # узнаём разрешение экрана
import json
import sys
from tkinter import *


# мои коды
import set
import save_loading_game
from menu import Button_1, Button_2 # мои кнопки прочее


import option #файл для вынесения некоторых функций из основного кода
import sprite_build # спрайты различных построек

from bullet import Bullet_1 # класс для выстрелов


# спрайты зомби в папке zombies
from zombies.zombie_1 import Zombie_1, Zombie_2, Zombie_3, Zombie_4

try:
    with open('setting.json', 'r',encoding='utf-8') as json_file:
        CONFIG = json.load(json_file)
except FileNotFoundError:
    CONFIG = {      # настройки
            "FPS_see": True, # отображение фпс
            "matrix": False, # сетка
            "resolution": "ful", # разрешение экрана
            }  

if CONFIG["resolution"] == "ful":
    geom_disp = ctypes.windll.user32 # получаем разрешение монитора
    geom_disp.SetProcessDPIAware()
    WIDTH = geom_disp.GetSystemMetrics(0) # ширина
    HEIGHT = geom_disp.GetSystemMetrics(1) # высота
else:
    WIDTH = 1920
    HEIGHT = 1080

FPS = 60


# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.font.init()
# Создаем игру и окно
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT) )

pygame.display.set_caption("Enemy fan")
clock = pygame.time.Clock()

f1 = pygame.font.Font(None, 36)
mousex, mousey = pygame.mouse.get_pos() # курсор
GRID = 20
# кол-во клеток
cell_count = 5184 # 96 x 54
# переменные для отчёта изменения при перемещении камеры
grid_x = 0
grid_y = 0
#сетка

game = False # запущена ли у нас игра



IMAGE = {"numbers": {}, #словарь с изображениями
        "background":{"main": ""},
        "buttons": {}, #словарь с кнопками
        "decoration":{}, # словарь с кнопками декораций
        "interior": {}, # словарь с интерьером
        "build":{} # словарь с строительными блоками
        } 



IMAGE = option.img(IMAGE)
MAPS = {} # словарь со значением о всех клетках на карте
OPT = "0"  # переменная что хотим поставить



obj_btn_1 = []  #   для кнопок
obj_btn_2 = []



class Map(pygame.sprite.Sprite): # спрайты карты
    
    def __init__(self, x, y, number, color): # number - номер клетки
        pygame.sprite.Sprite.__init__(self)
        self.size_image = 25
        self.color = color
        self.color_n = color # дополнительный цвет
        if CONFIG["matrix"] == False:
            self.image = pygame.Surface((self.size_image, self.size_image))
            self.image.fill(self.color)
        else:
            image = random.choice(IMAGE["numbers"])
            self.image = pygame.transform.scale(image, (self.size_image, self.size_image))
            
            self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.number = number
        self.Rect = pygame.Rect(self.x, self.y, GRID, GRID)
        self.image_number = random.choice(IMAGE["numbers"])
    def update(self): # size отвечает за изменения изображений

        if VARIABLE["map"]["matrix"] == 1:
            image = random.choice(IMAGE["numbers"])
            self.image = pygame.transform.scale(image, (self.size_image, self.size_image))
            
            self.rect = self.image.get_rect()
        elif VARIABLE["map"]["matrix"] == 2: 
            self.image = pygame.Surface((self.size_image, self.size_image))
            self.image.fill(self.color)

        if game == False:self.kill()    #вышли из игры - удаляем спрайт




class Turret_1(pygame.sprite.Sprite): # выделение
    def __init__(self, number_grid):  
        pygame.sprite.Sprite.__init__(self)
        self.number_grid = number_grid
        self.size_image_x = GRID
        self.size_image_y = GRID
        self.image = pygame.Surface((self.size_image_x, self.size_image_y))
        self.image.fill((200, 120, 0))
        self.rect = self.image.get_rect()
        self.rect.x = MAPS[number_grid]["x"]
        self.rect.y = MAPS[number_grid]["y"]
        self.time_s = 60 # через какое время может стрелять турэль
        self.time = 60
    def update(self, keys):
        if game == False or MAPS[self.number_grid]["sprites"] == False:self.kill()    #вышли из игры - удаляем спрайт
        self.time += 1
        if self.time >= self.time_s and keys[pygame.K_q]:
            global all_sprites_bullet
            bul = Bullet_1(self.rect.x, self.rect.y, mousex, mousey)
            all_sprites_bullet.add(bul)
            self.time = 0


class Window(pygame.sprite.Sprite): # окна
    
    def __init__(self,  number):
        pygame.sprite.Sprite.__init__(self)
        from main import MAPS
        self.size_image = 25
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.image.fill((114, 200, 244))
        self.rect = self.image.get_rect()
        self.number = number

        self.rect.x = MAPS[self.number]["x"]
        self.rect.y = MAPS[self.number]["y"]

    def update(self): # size отвечает за изменения изображений


        if game == False or MAPS[self.number]["sprites"] == False:self.kill()    #вышли из игры - удаляем спрайт


class Spawn(pygame.sprite.Sprite): # спрайт спавна наших юнитов( распологается на краю карты)
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.size_image = GRID*2
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.image.fill((200, 120, 0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2 - GRID
        self.rect.y = HEIGHT - GRID

    def update(self, game): 
        if game == False:self.kill()    #вышли из игры - удаляем спрайт


def cret_new_game():

    
    global MAPS, VARIABLE,  all_sprites_map, WAWE, VOLUME_TURRENT, VOLUME_WINDOW, GAME_ZOMBIE, OPT




    VARIABLE = { # словарь с игровыми переменными 
            # что мы будем ставить
            "map": {"matrix": 0},
            "isolation": False, # выделение
            "menu_game_1": False, # открытие/закрытие кнопок выход и т.п.
            "menu_game_2": False, # открытие/закрытие кнопок деврации и т.п.
            "menu_game_3": False, # открытие/закрытие кнопок выбора интерьера(парты и т.д.)
            "menu_game_4": False, # открыти/закрытие кнопок выбора строительства
            }  


    WAWE = 0 # номер волны
    GAME_ZOMBIE = True # начали ли мы игру
    OPT = 0
    MAPS = {} # словарь со значением о всех клетках на карте
    all_sprites_map = pygame.sprite.Group()
    x_f = 0
    y_f = 0
    counter = 0
    for i in range(cell_count):
        if counter >= WIDTH/GRID:   x_f, y_f, counter = 0, y_f + GRID, 0
        color = random.choice([(0, 255, 0), (0, 250, 0), (0, 247, 0), (0, 243, 0)])
        map = Map(x_f, y_f, str(i), color)
        all_sprites_map.add(map)
        
        # добавляем блок в словарь
        MAPS[str(i)] = {
            "x": "",
            "y": "",
            "sprites": False, # есть ли тут что-то
            "window":{"location": False},
            "turrent_1":{"location": False}
            }
        MAPS[str(i)]["x"] = x_f
        MAPS[str(i)]["y"] = y_f

        x_f +=GRID # перемещаем на одну клетку
        counter +=1



    VOLUME_TURRENT = 0 # кол-во турелей
    VOLUME_WINDOW = 0 # кол-во окон
    # создаём новые группы спрайтов
    global   all_sprites_bullet, all_sprites_road
    global all_sprites_wall, all_sprites_spawn, all_sprites_window, all_sprites_zobies, all_sprites_turent


    all_sprites_window = pygame.sprite.Group()

    all_sprites_spawn = pygame.sprite.Group() # один на карту, куда идут юниты

    all_sprites_zobies = pygame.sprite.Group() # зомби
    all_sprites_bullet = pygame.sprite.Group() # снаряды
    all_sprites_turent = pygame.sprite.Group() # турели 
    global spawn
    spawn = Spawn()
    all_sprites_spawn.add(spawn)
    z = Zombie_1()
    all_sprites_zobies.add(z)


def help(): 

    text = ["Помощь:", "Твоя задача защититься от врагов.", "У тебя для защиты есть несколько средств.",
            "1) Турели, при нажатии на Q начинает стрелять в сторону курсора.",
            "2) Битые стёкла, наносят небольшой урон. Не стоит на них полагаться.",
            "Враги всегда идут в одно место.",
            "Мало зомби? Просто нажми F2.",
            "Удачи"]

    for i, line in enumerate(text):
        text_surface = f1.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (0, i * 36))


# курсор, вдруг что-то взяли
arrow = sprite_build.Arrow()
all_sprites_arrow = pygame.sprite.Group();  all_sprites_arrow.add(arrow)



def open_game_menu_1(): 
    global VARIABLE
    if VARIABLE["menu_game_1"] == True: VARIABLE["menu_game_1"] = False
    else: VARIABLE["menu_game_1"] = True



button_1_game = Button_2(WIDTH//1.07, HEIGHT//1.13,  open_game_menu_1)





def menu_turrent_turrent_1(): 
    global OPT
    OPT = "turret_1"
button_open_turrent_1 = Button_2(WIDTH//3.5, HEIGHT//1.07,  menu_turrent_turrent_1, "турели", True)



all_sprites_decoration_btn = pygame.sprite.Group()


def open_game_menu_window(): global OPT; OPT = "window"
button_open_window = Button_2(WIDTH//2.9, HEIGHT//1.07,  open_game_menu_window, "битое стекло", True)

# открытие меню выбора интерьера


all_sprites_menu_game = pygame.sprite.Group()
all_sprites_menu_game.add(button_1_game,   button_open_turrent_1,  button_open_window)






def save_game():    save_loading_game.save_game() #*сохранение игры

def stop_game():
    global game; game = False
def full_stop_game(): sys.exit()#* Закрываем игру
btn_1_game = Button_1(WIDTH//2, HEIGHT//1.1 ,WIDTH//10 , HEIGHT//13 ,obj_btn_1,"сохранить макет", save_game,30);obj_btn_1 = btn_1_game.loading_lis()    # ЗАБИРАЕМ СПИСОК

btn_2_game = Button_1(WIDTH//1.5, HEIGHT//1.1 ,WIDTH//10 , HEIGHT//13 ,obj_btn_1,"выйти в меню", stop_game, 30 );obj_btn_1 = btn_2_game.loading_lis()    # ЗАБИРАЕМ СПИСОК

btn_3_game = Button_1(WIDTH//1.2, HEIGHT//1.1 ,WIDTH//10 , HEIGHT//13 ,obj_btn_1,"рабочий стол", full_stop_game, 30);obj_btn_1 = btn_3_game.loading_lis()    # ЗАБИРАЕМ СПИСОК


surf = pygame.Surface((WIDTH, 90))

# прозрачная поверхность на главном меню, чтоб фон глаза не резал
surf_m = pygame.Surface((WIDTH, HEIGHT))



# кнопки в главном меню с текстом
def run_game(): 
    cret_new_game() # создаём поле
    global game
    game = True

btn_1_menu = Button_1(WIDTH//2, HEIGHT//2 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2,"новая игра", run_game);   obj_btn_2 = btn_1_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК
# кнопки в главном меню с текстом
def loading_game():  #* загрузка игры
    try:
        global MAPS, VOLUME_TURRENT, VOLUME_WINDOW, game, all_sprites_window, all_sprites_turent
        file = save_loading_game.loading_game() #* загрузка игры
        cret_new_game()

        MAPS_op = file["MAPS"]
        for i in range(cell_count):

            if MAPS_op[str(i)]["sprites"] == True:
                if MAPS_op[str(i)]["window"]["location"] == True: # если есть окно
                    win = Window(str(i))
                    all_sprites_window.add(win)
                    MAPS[str(i)]["sprites"] = True
                    MAPS[str(i)]["window"]["location"] = True
                elif MAPS_op[str(i)]["turret_1"]["location"] == True: # если есть турель
                    tur = Turret_1(str(i))
                    all_sprites_turent.add(tur)
                    MAPS[str(i)]["sprites"] = True
                    MAPS[str(i)]["turrent_1"]["location"] = True
        VOLUME_TURRENT = file["VOLUME_TURRENT"] # количество турелей
        VOLUME_WINDOW = file["VOLUME_WINDOW"] # количество окон
        game = True # запускаем игру

    except: pass # можем не загрузить, а просто закрыть из-за этого вылетет ошибка

btn_2_menu = Button_1(WIDTH//2, HEIGHT//1.7 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2,"загрузить макет", loading_game,30 );obj_btn_2 = btn_2_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК
def setting_game(): set.setting() #* открываем настройки

btn_3_menu = Button_1(WIDTH//3, HEIGHT//2 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2, "настройки", setting_game);   obj_btn_2 = btn_3_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК
def exit_game(): sys.exit() #* выход из игры

btn_4_menu = Button_1(WIDTH//3, HEIGHT//1.7 ,WIDTH//9 , HEIGHT//13 ,obj_btn_2,"выход", exit_game); obj_btn_2 = btn_4_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК

def help_game():
    global help_open
    if help_open == True: help_open = False
    else: help_open = True #* открытие окна помощи
btn_5_menu = Button_1(WIDTH//100, HEIGHT//1.2 ,WIDTH//12 , HEIGHT//15 ,obj_btn_2,"помощь", help_game); obj_btn_2 = btn_4_menu.loading_lis()
set.setting_error() #! используется для предотвращения потери переменной при открытии настроек или окна сохранить игру, х.з. почему

help_open = False # открыли ли мы окно помощи

# Цикл игры
running = True
while running:
    mousex, mousey = pygame.mouse.get_pos() # курсор
    keys = pygame.key.get_pressed() # другой метод обработки нажатий
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:   running = False


        if pygame.mouse.get_pressed()[0] and game == True:

            if OPT == "turret_1":
                number_sp = option.grids_config()

                if MAPS[number_sp]["sprites"] == True: pass # если на клетке уже есть  спрайт - ничего не делаем
                else:
                    if VOLUME_TURRENT < 15:
                        player = Turret_1(number_sp)
                        MAPS[number_sp]["turret_1"] = {"location": True}
                        all_sprites_turent.add(player)
                        VOLUME_TURRENT += 1
                        MAPS[number_sp]["sprites"] = True

            elif OPT == "window":
                number_sp = option.grids_config()
                if  MAPS[number_sp]["sprites"] ==  True: pass # если на клетке уже есть  спрайт - ничего не делаем
                else:
                    if VOLUME_WINDOW < 25:
                        win = Window(number_sp)
                        MAPS[number_sp]["window"] = {"location": True}
                        all_sprites_window.add(win)
                        VOLUME_WINDOW +=1
                        MAPS[number_sp]["sprites"] = True





    if game == True:
        if GAME_ZOMBIE == True:
            if keys[pygame.K_DELETE]: # удаление объекта
                number_sp = option.grids_config()
                if MAPS[number_sp]["turrent_1"]["location"] == True: VOLUME_TURRENT -=1
                elif MAPS[number_sp]["window"]["location"] == True: VOLUME_WINDOW -=1
                MAPS[number_sp]["sprites"] = False
                MAPS[number_sp]["turret_1"] = {"location": False}
                MAPS[number_sp]["window"] = {"location": False}


            # Обновление
            all_sprites_map.update()

            all_sprites_window.update()

            all_sprites_turent.update(keys)
            all_sprites_zobies.update()
            all_sprites_bullet.update(keys)
            # Рендеринг

        # Рендеринг



            all_sprites_map.draw(screen)

            all_sprites_window.draw(screen)
            all_sprites_spawn.draw(screen)
            all_sprites_turent.draw(screen)
            all_sprites_zobies.draw(screen)
            all_sprites_bullet.draw(screen)
            all_sprites_arrow.update()


        


            # отсылка на матрицу
            if keys[pygame.K_F1]: 
                VARIABLE["map"]["matrix"] = 1
                all_sprites_map.update()
                VARIABLE["map"]["matrix"] = 0
            else: VARIABLE["map"]["matrix"] = 0
            if keys[pygame.K_F5]: # выкл. эффект матрицы
                VARIABLE["map"]["matrix"] = 2 
                all_sprites_map.update()
                VARIABLE["map"]["matrix"] = 0
            
            if keys[pygame.K_ESCAPE]: lbl = 0; OPT = ""; OPTCURSOR = "" #заменяем переменную

            if str(all_sprites_zobies) == "<Group(0 sprites)>": 

                for i in range(10): 
                    zomb = Zombie_1()
                    all_sprites_zobies.add(zomb)

                    rn = random.randint(0, WAWE**2)

                    for i in range(rn):
                        zomb = Zombie_2()
                        all_sprites_zobies.add(zomb)
                if WAWE > 5:
                    rn = random.randint(0, WAWE)
                    for i in range(rn):
                        zomb = Zombie_3()
                        all_sprites_zobies.add(zomb)
                if WAWE > 10:
                    rn = random.randint(0, WAWE)
                    for i in range(rn):
                        zomb = Zombie_4()
                        all_sprites_zobies.add(zomb)
                WAWE += 1

            if pygame.sprite.spritecollide(spawn, all_sprites_zobies, False): GAME_ZOMBIE = False ; print(9999)# мы проиграли
            if keys[pygame.K_F2]: 
                zomb = Zombie_2()
                all_sprites_zobies.add(zomb)

            wawe_text = f1.render(str(WAWE), True,     (180, 0, 0))
            screen.blit(wawe_text, (10, HEIGHT//7))
        else:
            for i in range(10):
                pygame.draw.rect(screen, (64, 128, 255), (0, 0, WIDTH, HEIGHT), i)
                wawe_text = f1.render("Ты проиграл!", True, (180, 0, 0))
                screen.blit(wawe_text, (WIDTH//2, HEIGHT//2))
                wawe_text = f1.render("Вы можете сохранить игру и запустить в режиме мекета!", True, (180, 0, 0))
                screen.blit(wawe_text, (WIDTH//2, HEIGHT//1.5))
        surf.fill(BLACK)  # Заполнение фона, цвет

        surf.set_alpha(100)# прозрачность

        screen.blit(surf, (0, HEIGHT-  90))
        if VARIABLE["menu_game_1"] == True:
            for object in obj_btn_1:  object.process()
        
        # обнолвляем и выводим кнопки в одном месте
        all_sprites_menu_game.draw(screen)
        all_sprites_menu_game.update()
        if VARIABLE["menu_game_2"] == True:
            all_sprites_decoration_btn.draw(screen)
            all_sprites_decoration_btn.update()
    else: # если не играем
        screen.blit(IMAGE["background"]["main"],(0,0))
        surf_m.fill(BLACK)  # Заполнение фона, цвет

        surf_m.set_alpha(100)# прозрачность
        
        screen.blit(surf_m, (0, 0))
        for object in obj_btn_2:  object.process()  # рисуем кнопки
        if help_open == True: help()

    if CONFIG["FPS_see"] == True:
        fps = clock.get_fps()
        fps_text = f1.render(str(int(fps)), True,     (180, 0, 0))
        screen.blit(fps_text, (10, 10))
    if keys[pygame.K_F7]: FPS = 120
    if keys[pygame.K_F8]: FPS = 60

    pygame.display.flip()   # обновляем все поверхности


pygame.quit()

