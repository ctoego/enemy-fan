import json, toml, sys, time

class Data:
    def __init__(self):
        
        self.SETTING = self.loading_setting()
        self.SAVE = self.loading_game()
        self.CONFIG = self.loading_config()
        self.COLOR = self.CONFIG['Color']

    
    def loading_config(self):
        try:
            with open('./data/config.toml', 'r', encoding='utf-8') as f:
                return toml.load(f)  
        except:
            print('data.py class Data: Error open or read config.toml. Stopping the program.')
            time.sleep(5)
            sys.exit()

    def loading_setting(self):
        try:
            with open('./data/setting.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except :
            print(f'data.py class Data: Error open or read setting.json')
            return {
                    "FPS_see": True,
                    "intro": True,
                    "resolution": "1632x918",
                    "FPS_max": 120
                    }
        
    def save_setting(self):
        try:
            with open('./data/setting.json', 'w',encoding='utf-8') as f:
                json.dump(self.SETTING, f, indent=4)
        except:
            print(f"data.py class Data: Error open or write setting.json at saving the setting. No stop program.")

    def reset_game(self):
        '''Сброс прогресса'''
        p = {   "level": {
                    "1": False,
                    "2": False,
                    "3": False,
                    "4": False
                    },
                "score": 0
            }
        with open('./data/savegame.json', 'w',encoding='utf-8') as f:
            json.dump(p, f, indent=4)
        return p

    def loading_game(self):
        try:
            with open('./data/savegame.json', 'r',encoding='utf-8') as f:
                return json.load(f)
        except:
            print(f'data.py class Data: Error open or read savegame.json. Reset the game progress.')
            return self.reset_game()


    def save_game(self):
        '''Сохранение результатов игрока'''

        with open('./data/savegame.json', 'w',encoding='utf-8') as f:
            json.dump(self.SAVE, f, indent=4)


    def take_setting(self, object):
        '''taking the new data setting from set.py'''

        self.SETTING = object
        self.save_setting()

