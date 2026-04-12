import pygame

from game_ui.menu import Button_1, ImageButton
from core.log import Log
class SurferGame:
    def __init__(self, screen):
        from core.state_game import G
        '''интерфейс во время игры'''

        self.screen = screen

        self.open_game_menu_1 = False       # close level/game

        style = {   #различные цвета
                'normal': "#00f3e7",
                'hover': "#00f3f3b2",
                'pressed': '#252e25',
            }

        # ===== always displayed =======

        self.main_widget = []    # always displayed

        self.button_1_game = Button_1( x = G.GRID * 85, y = G.GRID * 50,
                        fillColors = style,
                        width = 4 * G.GRID, height = 3 * G.GRID,

                        text = "Меню",
                        onclickFunction = self.opn_game_menu_1)
        
        self.main_widget.append(self.button_1_game)

        # ===== card slots =======
        self.card_slots = []
        self.slot_1 = ImageButton(
            x = G.GRID * 30, y = G.GRID * 48,
            image_normal= G.IMAGE['card']
        )
        self.card_slots.append(self.slot_1)

        self.slot_2 = ImageButton(
            x = G.GRID * 40, y = G.GRID * 48,
            image_normal= G.IMAGE['card']
        )
        self.card_slots.append(self.slot_2)

        self.slot_3 = ImageButton(
            x = G.GRID * 50, y = G.GRID * 48,
            image_normal= G.IMAGE['card']
        )
        self.card_slots.append(self.slot_3)

        self.slot_4 = ImageButton(
            x = G.GRID * 60, y = G.GRID * 48,
            image_normal= G.IMAGE['card']
        )
        self.card_slots.append(self.slot_4)
        # ===== close level/game =======
        
        self.listing_close = []


        self.button_close_game = Button_1(
            fillColors = style,
            x = G.GRID * 85, y = G.GRID * 40,
                width = 8 * G.GRID, height = 3 * G.GRID,
                text = "Закрыть игру",
                onclickFunction = self.stop_game
        )
        self.listing_close.append(self.button_close_game)
        self.button_close_level = Button_1(
            fillColors = style,
            x = G.GRID * 85, y = G.GRID * 30,
                width = 8 * G.GRID, height = 3 * G.GRID,
                text = "Главное меню",
                onclickFunction = self.close_level
        )
        self.listing_close.append(self.button_close_level)

    def update(self):
        '''Обновление состояния слотов, сверх важный пункт'''
        from core.level_manager import LM
        from core.state_game import G
        c = 0
        for i in LM.selected_card:

            try:

                self.card_slots[c].configure(image_normal = G.IMAGE[i.image])
               # self.card_slots[c].image = G.IMAGE[i.image]
            except KeyError as e:
                Log.error('error', e)


    def opn_game_menu_1(self):
        self.open_game_menu_1 = not  self.open_game_menu_1
    
    def close_level(self):
        from core.state_game import G
        G.stop_game()
        G.game = False
    def stop_game(self):
        from core.state_game import G
        G.running = False
    def draw(self):
        '''Сначало рисуем, а потом обновляем ( для кнопок )'''

        for object in self.card_slots:
            object.process(self.screen)
        for object in self.main_widget:
            object.process(self.screen)
        if self.open_game_menu_1:

            for object in self.listing_close:  object.process(self.screen)
