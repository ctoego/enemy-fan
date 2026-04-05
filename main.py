import pygame
import random
import ctypes # узнаём разрешение экрана
import sys
import os




# my code
from core.state_game import G
from core.console import DevConsole
from core.level_manager import LM
from core.sprite_group import SG

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
from sprites.zombies import ZM, Zombie_1, Zombie_2


DATA = Data()

LM.init_enemy(DATA.loading_enemy())

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





G.init_from_main(
    colors = DATA.COLOR,
    screen_params = (WIDTH, HEIGHT),
    game_params = {
        'FPS': int(DATA.SETTING['FPS_max'])
    }
)
G.init_camera()
G.Zom_x = G.WIDTH//2 - G.GRID*2   #*куда должны идти зомби, координаты базы
G.Zom_y = G.GAME_HEIGHT - G.GRID*4


del WIDTH
del HEIGHT



pygame.font.init()
# Создаем игру и окно
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((G.WIDTH, G.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
screen.set_alpha(None)  #* отключаем альфа канал для производительности
pygame.display.set_caption("Enemy fan")
clock = pygame.time.Clock()

f1 = pygame.font.Font(None, 36)

mousex, mousey = pygame.mouse.get_pos() # курсор


console = DevConsole(screen, G.WIDTH, G.HEIGHT) # консоль
#сетка

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



IMAGE = img(IMAGE,G.WIDTH, G.HEIGHT, G.GRID)

ZM.update_variable()        # обновляем данные для зомби

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
        self.next_change = pygame.time.get_ticks() + random.randint(200, 500)
    
    def update(self):
        if pygame.time.get_ticks() >= self.next_change:
            old_center = self.rect.center
            self.image = random.choice(self.IMAGE["numbers"])
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.next_change = pygame.time.get_ticks() + random.randint(200, 500)
            self.dirty = 1


class Turret_1(pygame.sprite.Sprite): 
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
                bul = Bullet_1(self.rect.x, self.rect.y, mousex, mousey, G.GRID)
                SG.all_sprites_bullet.add(bul)
                self.time = 0
            self.last_update = current_time


class Spawn(pygame.sprite.Sprite): # спрайт спавна наших юнитов( распологается на краю карты)
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.size_image = G.GRID * 4
        self.image = pygame.Surface((self.size_image, self.size_image))
        self.image.fill((200, 120, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (G.Zom_x, G.Zom_y)
        

        self.update_rate = 60  # Частота обновления (Гц)
        self.update_interval = 1000.0 / 60  # Интервал в мс
        
        self.last_update = pygame.time.get_ticks()

        self.direction = 1
    def update(self, all_sprites_zobies):  
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_update
        
        if elapsed >= self.update_interval:
            if pygame.sprite.spritecollideany(self, all_sprites_zobies):
                G.health -= 15
            self.last_update = current_time


def cret_new_game(level):

    G.reset_var_game()
    G.start_game()


    SG.clear_sprites_group()  # пересоздаём группы спрайтов
    SG.init_chunks()

    for x in range(G.MAP_COUNT_WIDTH):
        for y in range(G.MAP_COUNT_HEIGHT):
            map = Map(x, y, G.GRID)
            SG.all_sprites_map.add(map)

    SG.rebuild_all_chunks()
    global spawn
    
    spawn = Spawn()
    SG.all_sprites_spawn.add(spawn)
    
    z = Zombie_1()

    SG.all_sprites_zobies.add(z)

    if level >= -1:
        s = DATA.loading_level(level)
        if s:
            LM.new_level(s)


cret_new_game(-1)     #? вызываем, чтобы потом с первого раза начиналась игра

def help(): 

    text = ["Помощь:", "Твоя задача защититься от врагов.", "У тебя для защиты есть несколько средств.",
            "1) Турели, при нажатии на Q начинает стрелять в сторону курсора.",
            "2) Битые стёкла, наносят небольшой урон. Не стоит на них полагаться.",
            "Враги всегда идут в одно место.",
            "Мало зомби? Просто нажми F2.",
            "Удачи"]
    pygame.draw.rect(screen, (196, 241, 149, 10), (G.GRID * 19, 10, G.GRID * 55, G.GRID * 17))
    i = 1
    for  line in text:
        text_surface = f1.render(line, True, (10, 10, 10))
        screen.blit(text_surface, (G.GRID * 20, G.GRID * i))
        i += 2


# курсор
arrow = Arrow(mousex, mousey, G.GRID)
SG.all_sprites_arrow.add(arrow)



def open_game_menu_1(): 
    if G.VARIABLE["menu_game_1"] == True: G.VARIABLE["menu_game_1"] = False
    else: G.VARIABLE["menu_game_1"] = True


button_1_game = Button_2(G.WIDTH//1.07, G.HEIGHT//1.13, G.WIDTH, G.HEIGHT,  open_game_menu_1)


button_open_turrent_1 = Button_2(G.WIDTH//3.5, G.HEIGHT//1.07, G.WIDTH, G.HEIGHT, None, "турели", True)






button_open_window = Button_2(G.WIDTH//2.9, G.HEIGHT//1.07, G.WIDTH, G.HEIGHT, None, "битое стекло", True)




SG.all_sprites_menu_game.add(button_1_game,   button_open_turrent_1,  button_open_window)




def stop_game():   
    G.game = False
def full_stop_game(): sys.exit()#* Закрываем игру


btn_2_game = Button_1(G.WIDTH//1.5, G.HEIGHT//1.1 ,G.WIDTH//10 , G.HEIGHT//13 ,obj_btn_1,"выйти в меню", stop_game, 30 );obj_btn_1 = btn_2_game.loading_lis()    # ЗАБИРАЕМ СПИСОК

btn_3_game = Button_1(G.WIDTH//1.2, G.HEIGHT//1.1 , G.WIDTH//10 , G.HEIGHT//13 ,obj_btn_1,"рабочий стол", full_stop_game, 30);obj_btn_1 = btn_3_game.loading_lis()    # ЗАБИРАЕМ СПИСОК


surf = pygame.Surface((G.WIDTH, G.GRID*5))

# прозрачная поверхность на главном меню, чтоб фон глаза не резал
surf_m = pygame.Surface((G.WIDTH, G.HEIGHT))



# кнопки в главном меню с текстом
def run_game(level): 
    G.LEVEL = level
    cret_new_game(level) # создаём поле
    G.game = True
    

btn_1_menu = Button_1(G.WIDTH//2, G.HEIGHT//2 , G.WIDTH//9 , G.HEIGHT//13 ,obj_btn_2,"бесконечность", lambda: (run_game(0)), 27);   obj_btn_2 = btn_1_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК
# кнопки в главном меню с текстом


def help_game():

    if G.help_open == True: G.help_open = False
    else: G.help_open = True #* открытие окна помощи

btn_2_menu = Button_1(G.WIDTH//2, G.HEIGHT//1.7 , G.WIDTH//9 , G.HEIGHT//13 ,obj_btn_2,"помощь", help_game);obj_btn_2 = btn_2_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК
def setting_game(): # TODO открытие настроек
    G.setting_open = not G.setting_open

btn_3_menu = Button_1(G.WIDTH//3, G.HEIGHT//2 , G.WIDTH//9 , G.HEIGHT//13 ,obj_btn_2, "настройки", setting_game);   obj_btn_2 = btn_3_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК

def exit_game(): sys.exit() #* выход из игры

btn_4_menu = Button_1(G.WIDTH//3, G.HEIGHT//1.7 , G.WIDTH//9 , G.HEIGHT//13 ,obj_btn_2,"выход", exit_game); obj_btn_2 = btn_4_menu.loading_lis()    # ЗАБИРАЕМ СПИСОК





def level_game(): 

    if G.level_open : G.level_open = False
    else: G.level_open = True #* открытие окна уровней
btn_6_menu = Button_1(G.WIDTH//1.2, G.HEIGHT//1.2 , G.WIDTH//12 , G.HEIGHT//15 ,obj_btn_2,"уровни", level_game); obj_btn_2 = btn_6_menu.loading_lis()




def matrix():
    x_f = 0
    y_f = 0
    counter = 0
    for _ in range(1296):     # создание матрицы на главном
        if counter >= 48:   x_f, y_f, counter = 0, y_f + G.GRID*2, 0

        map = Matrix(x_f, y_f, IMAGE)
        SG.all_sprites_matrix.add(map)

        x_f += G.GRID*2 # перемещаем на одну клетку
        counter +=1

matrix()



def endless_mode_update_sprites():  # обновление спрайтов
    SG.all_sprites_map.update()
    SG.all_sprites_spawn.update(SG.all_sprites_zobies)
    SG.all_sprites_turent.update(keys)
    SG.all_sprites_zobies.update(SG.all_sprites_window, SG.all_sprites_bullet)
    SG.all_sprites_bullet.update(SG.all_sprites_zobies, G.GRID, G.WIDTH, G.HEIGHT)




# TODO классы менюшек(выбора уровня, настроек)
surferlevel = SurferLevel(G.GRID) 
surfersetting = SurferSetting(G.GRID, DATA) 



if DATA.SETTING['intro']:   
    for number in range(1, len(os.listdir("./image/intro"))):   # TODO заставка
        for event in pygame.event.get():
            
            # check for closing window
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        im = pygame.image.load(f"./image/intro/({number}).jpg").convert()
        im = pygame.transform.scale(im, (G.WIDTH, G.HEIGHT))
        clock.tick(30)
        screen.blit(im, (0, 0)) # фон 
        pygame.display.flip()  # Добавлен update экрана
    while True:
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT: pygame.quit()
        if pygame.mouse.get_pressed()[0] : break  #TODO ждём пока пользователь не дочитает
        screen.fill((191, 0, 1))
        screen.blit(f1.render("Нажми на курсор.", True, (169, 218, 227)), (G.GRID*40 , G.GRID))
        screen.blit(f1.render("Всё будет хорошо.", True, (169, 218, 227)), (G.GRID , G.GRID*4))
        screen.blit(f1.render("Они уже здесь.", True, (169, 218, 227)), (G.GRID*10 , G.GRID*40))
        screen.blit(f1.render("«В одиночестве есть своя очень странная красота». — Лив Тайлер", True, (169, 218, 227)), (G.GRID*20 , G.GRID*10))
        
        screen.blit(f1.render("«Вчера я был умным, поэтому я хотел изменить мир. Сегодня я мудр, поэтому меняюсь я сам» — Майя Энджелоу", True, (169, 218, 227)), (G.GRID*10 , G.GRID*20))
        screen.blit(f1.render("«Я стала замечать гравитацию ещё в детстве» — Камерон Диаз", True, (169, 218, 227)), (G.GRID*20 , G.GRID*30))
        screen.blit(f1.render("«Спокойные люди имеют самые громкие мысли». — Стивен Хокинг", True, (169, 218, 227)), (G.GRID*40 , G.GRID*40))
        pygame.display.flip()


# Цикл игры

while G.running:
    
    mousex, mousey = pygame.mouse.get_pos() # курсор
    keys = pygame.key.get_pressed() # другой метод обработки нажатий
    # Держим цикл на правильной скорости

    dt = clock.tick(G.FPS) / 1000.0            # Разница во времени между кадрами (dt)
    
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_m and G.camera:
                G.camera.toggle_mode()
            
            if G.camera and G.camera.mode == "manual":
                if event.key == pygame.K_a:
                    G.camera.move(-10, 0)
                elif event.key == pygame.K_d:
                    G.camera.move(10, 0)
                elif event.key == pygame.K_w:
                    G.camera.move(0, -10)
                elif event.key == pygame.K_s:
                    G.camera.move(0, 10)

            if event.key == pygame.K_F12:  
                console.toggle()
        console_handled = console.handle_event(event)   # TODO консоль
        # Если консоль обработала событие - пропускаем остальную логику
        if console_handled:
            continue
        
        # check for closing window
        if event.type == pygame.QUIT:   G.running = False
        if G.level_open:

            surferlevel.process(event, G.LEVEL)
            G.level_open = surferlevel.is_exit_pressed()
            
            if surferlevel.is_level_pressed != -1:
                G.LEVEL = surferlevel.is_level_pressed()
                if G.LEVEL != -1: 
                    G.level_open = False
                    run_game(G.LEVEL)
        if G.setting_open:
            surfersetting.process(event)
            G.setting_open = surfersetting.is_exit_pressed()
        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_ESCAPE:
                G.level_open = False
                G.setting_open = False

        if pygame.mouse.get_pressed()[0] and G.game:

            if (G.VOLUME_TURRENT < G.MAX_TURRENT or G.VOLUME_WINDOW < G.MAX_WINDOW):#TODO c каждой волной повышаем допустимое значение
                if G.OPT == 1:
                    if G.VOLUME_TURRENT < G.MAX_TURRENT:  #TODO c каждой волной повышаем допустимое значение
                        number_sp = grids_config(G.MAPS, G.GRID, world_mouse_x, world_mouse_y)  # type: ignore
                        if number_sp:
                            if G.MAPS[number_sp[0]][number_sp[1]] == 0: 

                                player = Turret_1(number_sp)
                                G.MAPS[number_sp[0]][ number_sp[1]] = 2
                                SG.all_sprites_turent.add(player)
                                G.VOLUME_TURRENT += 1
                                SG.mark_cell_dirty(number_sp[0], number_sp[1])

                elif G.OPT == 2:
                    if G.VOLUME_WINDOW < G.MAX_WINDOW:
                        number_sp = grids_config(G.MAPS, G.GRID, world_mouse_x, world_mouse_y)  # type: ignore
                        if number_sp:
                            if G.MAPS[number_sp[0]][number_sp[1]] == 0:  # если на клетке уже есть  спрайт - ничего не делаем

                                win = Window(number_sp, G.GRID)
                                G.MAPS[number_sp[0]][ number_sp[1]] = 3
                                SG.all_sprites_window.add(win)
                                G.VOLUME_WINDOW += 1
                                SG.mark_cell_dirty(number_sp[0], number_sp[1])

            if G.game:
                # выбираем турели
                if button_open_turrent_1.rect.collidepoint(mousex, mousey): 
                    G.OPT = 1
                elif button_open_window.rect.collidepoint(mousex, mousey): 
                    G.OPT = 2




    if G.game: 
        if G.GAME_ZOMBIE:
            if G.camera is not None:
                world_mouse_x = mousex + G.camera.x
                world_mouse_y = mousey + G.camera.y
                G.camera.update(world_mouse_x, world_mouse_y)
            else:  
                print(f'Играем без камеры')
                world_mouse_x = mousex
                world_mouse_y = mousey

            if keys[pygame.K_DELETE]: # удаление объекта
                number_sp = grids_config(G.MAPS, G.GRID, world_mouse_x, world_mouse_y)
                
                if G.MAPS[number_sp[0]][ number_sp[1]] == 2:
                    G.VOLUME_TURRENT -=1
                    G.MAPS[number_sp[0]][ number_sp[1]] = 0
                    SG.mark_cell_dirty(number_sp[0], number_sp[1])
                elif G.MAPS[number_sp[0]][ number_sp[1]] == 3:
                    G.VOLUME_WINDOW -=1
                    G.MAPS[number_sp[0]][ number_sp[1]] = 0
                    SG.mark_cell_dirty(number_sp[0], number_sp[1])


                SG.all_sprites_window.update(G.MAPS)



            # Обновление
            endless_mode_update_sprites()
            # Рендеринг


            SG.endless_mode_render(screen)

            SG.all_sprites_arrow.update(grids_config, G.OPT, screen, G.GRID, G.MAPS, G.VOLUME_WINDOW, G.VOLUME_TURRENT, G.WAVE, mousex, mousey)    #* что у нас на курсоре

            
            if keys[pygame.K_ESCAPE]: lbl = 0; G.OPT = 0; OPTCURSOR = "" #заменяем переменную

            if keys[pygame.K_1]: G.OPT = 1    #hotkeys for control 
            if keys[pygame.K_2]: G.OPT = 2

            if str(SG.all_sprites_zobies) == "<Group(0 sprites)>": 
                LM.new_WAVE(G.WAVE)
                G.WAVE += 1
                G.MAX_TURRENT +=1
                G.MAX_WINDOW += 1



            if G.health <= 0:   #* Завершение игры
                G.GAME_ZOMBIE = False 
                G.LEVEL = -1
                SG.clear_sprites_group()

            
            if G.WAVE > LM.count_wave and G.LEVEL != 0: #*если на уровнях -> завершаем игру

                
                G.VICTORY = True
                G.GAME_ZOMBIE = False 
                DATA.SAVE["level"][f'{G.LEVEL}'] = True
                G.LEVEL = -1
                DATA.save_game()
                

            if keys[pygame.K_F2]: #? если очень хочется, можно создать ещё зомби
                zomb = Zombie_2()
                SG.all_sprites_zobies.add(zomb)

            
            screen.blit(f1.render(f'Волна: {G.WAVE} из {LM.count_wave}', True, (180, 0, 0)), (10, G.GRID*5))

            screen.blit(f1.render(f'Доступно битых окон: {G.MAX_WINDOW - G.VOLUME_WINDOW}', True, (180, 0, 0)), (10, G.GRID*7))

            screen.blit(f1.render(f'Доступно орудий: {G.MAX_TURRENT - G.VOLUME_TURRENT}', True, (180, 0, 0)), (10, G.GRID*9))
            screen.blit(f1.render(f'Здоровье: {G.health}', True, (180, 0, 0)), (10, G.GRID*11))

        elif G.VICTORY:
            pygame.draw.rect(screen, (64, 128, 255), (0, 0, G.WIDTH, G.HEIGHT))
            screen.blit(f1.render("Победа!!!", True, (180, 0, 0)), (G.WIDTH//2, G.HEIGHT//2))
            G.VARIABLE["menu_game_1"] = True
        else:
            pygame.draw.rect(screen, (64, 128, 255), (0, 0, G.WIDTH, G.HEIGHT))
            WAVE_text = f1.render("Ты проиграл!", True, (180, 0, 0))
            screen.blit(WAVE_text, (G.WIDTH//2, G.HEIGHT//2))
            G.VARIABLE["menu_game_1"] = True



        surf.fill(G.RED)  # Заполнение фона, цвет


        screen.blit(surf, (0, G.HEIGHT- 90))
        if G.VARIABLE["menu_game_1"]:
            for object in obj_btn_1:  object.process(screen)

        # обнолвляем и выводим кнопки в одном месте
        SG.all_sprites_menu_game.draw(screen)
        SG.all_sprites_menu_game.update(screen)
        if G.VARIABLE["menu_game_2"]:
            SG.all_sprites_decoration_btn.draw(screen)
            SG.all_sprites_decoration_btn.update()




    else: # если не играем

        if pygame.time.get_ticks() - G.matrix_update_timer > 20:  
            SG.all_sprites_matrix.update()
            G.matrix_update_timer = pygame.time.get_ticks()
        changed_rects = SG.all_sprites_matrix.draw(screen)
        pygame.display.update(changed_rects)  # Обновляем только измененные области
        surf_m.fill(G.BLACK)  # Заполнение фона, цвет

        surf_m.set_alpha(100)# прозрачность

        screen.blit(surf_m, (0, 0))
        if G.level_open: surferlevel.render(screen, dt)
        elif G.setting_open: surfersetting.render(screen, dt)
        else:
            for object in obj_btn_2:  object.process(screen)  # рисуем кнопки
            if G.help_open == True: help()


    if CONFIG["FPS_see"] == True:

        fps_text = f1.render(f"fps: {int(clock.get_fps())}", True, (180, 0, 0))
        screen.blit(fps_text, (10, 10))
    if keys[pygame.K_F7]: G.FPS = 200       #! нужно поменять
    if keys[pygame.K_F8]: G.FPS = 60
    if keys[pygame.K_F6]: print(SG.all_sprites_zobies)
    if keys[pygame.K_F1]: G.WAVE = 10

    console.draw()
    pygame.display.flip()   # обновляем все поверхности



pygame.quit()
sys.exit()
