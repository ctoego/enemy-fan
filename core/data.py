import json, toml, sys, time
from core.log import Log
class Data:
    
        
    SETTING: dict = {}
    SAVE: dict = {}
    CONFIG:dict = {}
    COLOR: dict = {}
    STYLE: dict = {}
    Log.init(__file__)


    try:
        with open('./data/config.toml', 'r', encoding='utf-8') as f:  
            CONFIG = toml.load(f)  
        COLOR = CONFIG['color']
    except:
        Log.critical('data.py class Data: Error open or read config.toml. Stopping the program.')
        time.sleep(5)
        sys.exit()
    try:
        with open('./data/style.toml', 'r', encoding='utf-8') as f:  
            STYLE = toml.load(f)  
    except:
        Log.critical('data.py class Data: Error open or read style.toml. Stopping the program.')
        time.sleep(5)
        sys.exit()

    try:
        with open('./data/setting.json', 'r', encoding='utf-8') as f:
            SETTING =  json.load(f)
    except:
        Log.warning('data.py class Data: Error open or read setting.json. Reset the game setting.')
        SETTING = {
                "FPS_see": True,
                "intro": True,
                "resolution": "1632x918",
                "FPS_max": 120
                }

    try:
        with open('./data/savegame.json', 'r',encoding='utf-8') as f:
            SAVE = json.load(f)
    except:
        print(f'Error: data.py class Data: Error open or read savegame.json. Reset the game progress.')
        SAVE = {   "level": {
                    "1": False,
                    "2": False,
                    "3": False,
                    "4": False
                    },
                "score": 0
            }
        with open('./data/savegame.json', 'w',encoding='utf-8') as f:
            json.dump(SAVE, f, indent=4)
    @classmethod
    def loading_level(cls, number: int):
        try:
            with open(f'./data/levels/level_{number}.toml', 'r', encoding='utf-8') as f:  
                return toml.load(f)  
        except:
            print(f'Error: data.py class Data: Error open or read ./data/level/level_{number}.toml')

    @classmethod
    def loading_enemy(cls):
        try:
            with open(f'./data/enemy.toml', 'r', encoding='utf-8') as f:  
                return toml.load(f)  
        except:
            print(f'Error: data.py class Data: Error open or read enemy.toml')
            return {}


    @classmethod
    def save_setting(cls):
        try:
            with open('./data/setting.json', 'w',encoding='utf-8') as f:
                json.dump(cls.SETTING, f, indent=4)
        except:
            print(f"Error: data.py class Data: Error open or write setting.json at saving the setting. No stop program.")



    @classmethod
    def save_game(cls):
        '''Сохранение результатов игрока'''
        try:
            with open('./data/savegame.json', 'w',encoding='utf-8') as f:
                json.dump(cls.SAVE, f, indent=4)
        except:
            print(f"Error: data.py class Data: Error open or write savegame.json at saving the game. No stop program.")

    @classmethod
    def take_setting(cls, object):
        '''taking the new data setting from set.py'''

        cls.SETTING = object
        cls.save_setting()

