import pygame
import pygame_gui

class SurferLevel():
    def __init__(self, GRID):
        '''выбор уровня'''
        self.ui_surface = pygame.Surface((GRID*80, GRID*40))  # Отдельная поверхность для UI
        self.ui_manager = pygame_gui.UIManager((GRID*96, GRID*56)) # рисуем не на отдельной поверхности
        self.grid = GRID
        
        self.button_action = {}
        self.ui_offset_x = GRID * 8 #* смещение относительно основной поверхности
        self.ui_offset_y = GRID * 7
        
        # Создаем кнопки
        button_lvl_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID, self.ui_offset_y + GRID * 2), (GRID*40, GRID*3)),
            text='Уровень 1',
            manager=self.ui_manager,
            object_id='#btn_lvl_1'
        )
        # Сохраняем ссылку на функцию через lambda
        self.button_action[button_lvl_1] = lambda: self.level(1)

        button_lvl_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID, self.ui_offset_y + GRID * 6), (GRID*40, GRID*3)),
            text='Уровень 2',
            manager=self.ui_manager,
            object_id='#btn_lvl_2'
        )
        self.button_action[button_lvl_2] = lambda: self.level(2)

        button_lvl_3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID, self.ui_offset_y + GRID * 10), (GRID*40, GRID*3)),
            text='Уровень 3',
            manager=self.ui_manager,
            object_id='#btn_lvl_3'
        )
        self.button_action[button_lvl_3] = lambda: self.level(3)

        button_lvl_4 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID, self.ui_offset_y + GRID * 14), (GRID*40, GRID*3)),
            text='Уровень 4',
            manager=self.ui_manager,
            object_id='#btn_lvl_4'
        )
        self.button_action[button_lvl_4] = lambda: self.level(4)
        
        # Кнопка возврата
        self.button_exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID*70, self.ui_offset_y + GRID * 32), (GRID*8, GRID*4)),
            text='Возврат',
            manager=self.ui_manager
        )
        self.button_action[self.button_exit] = self.exit
        # Для отслеживания состояния
        self.exit_pressed = False
        self.level_pressed = False

    
    def render(self, screen, dt):
        self.exit_pressed = False
        
        screen.blit(self.ui_surface, (self.grid * 8, self.grid * 7))
        self.ui_manager.update(dt)
        self.ui_manager.draw_ui(screen)
        
    
    def process(self, event, LEVEL):
        self.level_pressed = LEVEL
        self.ui_manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_func = self.button_action.get(event.ui_element)
            if button_func:
                button_func()
    
    # Метод для проверки, нажата ли кнопка возврата
    def is_exit_pressed(self):
        return not self.exit_pressed
    
    def exit(self):
        self.exit_pressed = True

    def is_level_pressed(self):
        return  self.level_pressed
    def level(self, level):
        self.level_pressed = level
        # Здесь можно добавить логику перехода на уровень
