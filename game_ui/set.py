import pygame_gui
import pygame

import pygame.font


class SurferSetting():
    def __init__(self, GRID,  DATA):
        '''Настройки'''
        self.data = DATA
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
            relative_rect=pygame.Rect((self.ui_offset_x + GRID, self.ui_offset_y + GRID * 6), (GRID*8, GRID*3)),
            text='Заставка',
            manager=self.ui_manager,
        )

        # Создаем кнопки
        self.button_intro = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID * 12, self.ui_offset_y + GRID * 6), (GRID*10, GRID*3)),
            text=self.read_parapetr(DATA.SETTING['intro'], 0),
            manager=self.ui_manager,
            object_id='#check_button'
        )
        # Сохраняем ссылку на функцию через lambda
        self.button_action[self.button_intro] = lambda: (self.read_parapetr(self.button_intro, 3), self.edit_setting())

        label_fps_1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID , self.ui_offset_y + GRID * 10), (GRID*8, GRID*3)),
            text='Ограничение fps',
            manager=self.ui_manager,
        )

        self.selection_list_fps = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect(self.ui_offset_x + GRID * 12, self.ui_offset_y + GRID * 10, GRID*10, GRID*3),
            options_list=['60', '90', '120', '140', '200'],
            starting_option = str(DATA.SETTING['FPS_max']),

            manager=self.ui_manager
        )
        self.button_action[self.selection_list_fps] = lambda: self.edit_setting()

        label_fps_2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID , self.ui_offset_y + GRID * 14), (GRID*8, GRID*3)),
            text='показ fps',
            manager=self.ui_manager,
        )

        self.button_fps = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID * 12, self.ui_offset_y + GRID * 14), (GRID*10, GRID*3)),
            text = self.read_parapetr(DATA.SETTING['FPS_see'], 0),
            manager=self.ui_manager,
            object_id='#check_button'
        )

        self.button_action[self.button_fps] = lambda: (self.read_parapetr(self.button_fps, 3), self.edit_setting())

        
        label_resolution = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID , self.ui_offset_y + GRID * 18), (GRID*8, GRID*3)),
            text='Разрешение',
            manager = self.ui_manager,
        )
        print( DATA.SETTING['resolution'])
        self.selection_resolution = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect(self.ui_offset_x + GRID * 12, self.ui_offset_y + GRID * 18, GRID*10, GRID*3),
            options_list=["1920x1080", "1632x918", "auto"],
            starting_option = DATA.SETTING['resolution'],

            manager=self.ui_manager
        )
        self.button_action[self.selection_resolution] = lambda: self.edit_setting()
        
        # Кнопка возврата
        self.button_exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.ui_offset_x + GRID*70, self.ui_offset_y + GRID * 32), (GRID*8, GRID*4)),
            text='Возврат',
            manager=self.ui_manager
        )
        self.button_action[self.button_exit] = self.exit

        self.label_resert = pygame_gui.elements.UILabel( #* предупреждение о изменение настроек
            relative_rect=pygame.Rect((self.ui_offset_x + GRID , self.ui_offset_y + GRID * 32), (GRID*20, GRID*3)),
            text='',
            manager=self.ui_manager,
        )

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
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            button_func = self.button_action.get(event.ui_element)
            if button_func:
                button_func()

    def is_exit_pressed(self):
        return not self.exit_pressed

    def exit(self):
        self.exit_pressed = True

    def edit_setting(self):
        t = {
                'FPS_see':self.read_parapetr(self.button_fps, 1),
                'intro': self.read_parapetr(self.button_intro, 1),
                'resolution': self.selection_resolution.selected_option[0],
                'FPS_max': self.selection_list_fps.selected_option[0]
        }
        self.label_resert.set_text("Настройки будут применены после перезапуска.")
        self.data.take_setting(t)

    def read_parapetr(self, object, value):
        '''Conversion to a Boolean value'''
        if value == 1:
            if object.text == 'включено': return True
            else:  return False
        elif value == 0:
            if object: return 'включено'
            else: return 'выключено'
        else:
            if object.text == 'включено': object.set_text('выключено') 
            else: object.set_text('включено')

