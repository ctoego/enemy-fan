import pygame_gui
import pygame

import pygame.font


class SurferSetting():
    def __init__(self, GRID, CONFIG):
        '''Настройки'''
        self.ui_surface = pygame.Surface((GRID*80, GRID*40))  # Отдельная поверхность для UI
        self.ui_manager = pygame_gui.UIManager((GRID*96, GRID*56)) # рисует на основной поверхности
        self.grid = GRID
        
        self.button_action = {}
        self.ui_offset_x = GRID * 8 #* смещение относительно основной поверхности
        self.ui_offset_y = GRID * 7



        label_set = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID * 7, self.ui_offset_y + GRID * 2), (GRID*40, GRID*3)),
            text='Добро пожаловать в настройки',
            manager=self.ui_manager,


        )
        label_intro = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID, self.ui_offset_y + GRID * 6), (GRID*5, GRID*3)),
            text='Заставка',
            manager=self.ui_manager,
        )

        # Создаем кнопки
        button_intro = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID * 7, self.ui_offset_y + GRID * 6), (GRID*10, GRID*3)),
            text='Включено',
            manager=self.ui_manager,
            object_id='#check_button'
        )
        # Сохраняем ссылку на функцию через lambda
        self.button_action[button_intro] = lambda: button_intro.set_text('hello')

        label_fps = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID , self.ui_offset_y + GRID * 10), (GRID*5, GRID*3)),
            text='Ограничение fps',
            manager=self.ui_manager,
        )

        selection_list_fps = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect(self.ui_offset_x + GRID * 7, self.ui_offset_y + GRID * 10, GRID*10, GRID*3),
            options_list=['60', '90', '120', '140', '200'],
            starting_option='60',

            manager=self.ui_manager
        )
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
        
    
    def process(self, event):

        self.ui_manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_func = self.button_action.get(event.ui_element)
            if button_func:
                button_func()

    def is_exit_pressed(self):
        return not self.exit_pressed
    
    def exit(self):
        self.exit_pressed = True



#! используется для предотвращения потери переменной при открытии настроек или окна сохранить игру
def setting_error(): from main import CONFIG, screen, WIDTH, HEIGHT 