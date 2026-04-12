from core.camera import Camera
from typing import Optional

class G:
    ''' StateGame, storing variables
        precept:
            - use classmethod to load variables from main.py
            - don't create object of this class( g = G())
    '''
    #* const

    FPS: int = 0                # max fps
    WIDTH : int = 1632
    HEIGHT : int = 918
    cell_count: int = 4800      # 96 x 50б кол-во клеток
    MAP_COUNT_WIDTH: int = 192  # размер карты в клетках
    MAP_COUNT_HEIGHT: int = 100    

    MAP_WIDTH : int = 0     # размер карты в пикселях
    MAP_HEIGHT: int = 0     

    WHITE: tuple = ()
    BLACK: tuple = ()
    RED : tuple = ()
    GREEN: tuple = ()
    BLUE : tuple = ()

    IMAGE: dict =  {"numbers": {}, #словарь с изображениями
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


    camera : Optional['Camera'] = None  # камера, добавляем после определения размеров экрана

    update_timer: int = 0           # таймер обновления
    #* game var
    game: bool = False              # играем или сидим в менюшке
    LEVEL: int = - 1                # 0 = infifnite mode, -1 = not game
    MAPS: list = []                 # словарь со значением о всех клетках на карте
    OPT: int = 0                    # переменная что хотим поставить
    WAVE: int = 0                   # номер волны
    GAME_ZOMBIE: bool = False       # начали ли мы игру
    VOLUME_TURRENT : int = 0        # кол-во турелей
    VOLUME_WINDOW : int = 0         # кол-во окон
    VICTORY: bool = False           # на уровнях, выйграли или нет
    MAX_TURRENT: int = 25           # максимальное количество турелей
    MAX_WINDOW : int = 25           # максимальное количество шипов
    health:int = 5000               # здоровье базы

    help_open: bool = False         # открыли ли мы окно помощи
    level_open: bool = False        # открыли ли мы окно уровней
    setting_open: bool = False      # открыты ли настройки

    clicking: int = 0
    matrix_update_timer: int = 0

    running: bool = True            # игра запущена или нет

    Zom_x: int = 0                  # куда идут зомби
    Zom_y: int = 0                  # куда идут зомби

    VARIABLE: dict = {              # словарь с игровыми переменными 
            # что мы будем ставить
            "map": {"matrix": 0},
            "isolation": False,   # выделение
            "menu_game_1": False, # открытие/закрытие кнопок выход и т.п.
            "menu_game_2": False, # открытие/закрытие кнопок деврации и т.п.
            "menu_game_4": False, # открыти/закрытие кнопок выбора строительства
            }  
    @classmethod
    def stop_game(cls):
        cls.GAME_ZOMBIE = False 
        cls.LEVEL = -1
        cls.VICTORY = False

    @classmethod
    def reset_var_game(cls):
        cls.OPT = 0
        cls.MAPS = []
        cls.WAVE = 0
        cls.GAME_ZOMBIE = False
        cls.VOLUME_TURRENT = 0 
        cls.VOLUME_WINDOW = 0 
        cls.VICTORY = False 
        cls.MAX_TURRENT = 25 
        cls.MAX_WINDOW  = 25
        cls.help_open = False 
        cls.level_open = False 
        cls.setting_open = False 
        cls.VARIABLE: dict = {
            "map": {"matrix": 0},
            "isolation": False,   
            "menu_game_1": False, 
            "menu_game_2": False, 
            "menu_game_4": False,
            }  
        cls.health = 5000
        cls.world_mouse_x:int = 0
        cls.world_mouse_y:int = 0


    @classmethod
    def init_from_main(cls, colors: dict, screen_params: tuple, game_params:dict):
        '''load variable from main.py'''
        if colors:
            cls.WHITE = colors['WHITE']
            cls.BLACK = colors['BLACK']
            cls.RED = colors['RED']
            cls.GREEN = colors['GREEN']
            cls.BLUE = colors['BLUE']
        if screen_params:
            cls.WIDTH = screen_params[0]
            cls.HEIGHT  = screen_params[1]
            cls.GRID : int = cls.WIDTH//96
            cls.GAME_HEIGHT: int = cls.HEIGHT - cls.GRID * 4
            cls.MAP_WIDTH = cls.GRID * cls.MAP_COUNT_WIDTH
            cls.MAP_HEIGHT = cls.GRID * cls.MAP_COUNT_HEIGHT


        if game_params:
            cls.FPS = game_params['FPS']

    @classmethod
    def init_camera(cls):
        map_width_px = cls.MAP_COUNT_WIDTH * cls.GRID        # размер видимой области
        map_height_px = cls.MAP_COUNT_HEIGHT * cls.GRID   

        cls.camera = Camera(
            map_width = map_width_px,
            map_height = map_height_px,
            screen_width= cls.WIDTH,
            screen_height=cls.HEIGHT)
        
    @classmethod
    def init_font(cls):
        '''after init the screen'''
        import pygame
        cls.font_btn_wid_1 = pygame.font.SysFont('Arial', cls.WIDTH // 96)
        cls.f1 = pygame.font.Font(None, 36)


    @classmethod
    def start_game(cls):
        cls.WAVE = 0 # номер волны
        cls.GAME_ZOMBIE = True # начали ли мы игру
        cls.OPT = 0
        cls.MAPS = [bytearray( cls.MAP_COUNT_HEIGHT) for _ in range(cls.MAP_COUNT_WIDTH)]
        cls.VOLUME_TURRENT = 0 # кол-во турелей
        cls.VOLUME_WINDOW = 0 # кол-во окон
        cls.VICTORY = False # на уровнях, выйграли или нет
        cls.MAX_TURRENT = 25 # максимальное количество вещей
        cls.MAX_WINDOW  = 25