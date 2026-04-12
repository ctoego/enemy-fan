import pygame


GREEN = (0, 255, 0)

from core.log import Log



class Button_1(): #клас кнопка
    def __init__(self, x, y, width, height,  text='Button', onclickFunction = None,
                size_font: int = 40,
                edit_size = True,
                fillColors: dict | None = None ): 


        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction

        if fillColors:
            if isinstance(fillColors, dict):
                self.fillColors = fillColors
        else:
            self.fillColors = {   #различные цвета
                'normal': '#00f300',
                'hover': '#3a8334',
                'pressed': '#252e25',
            }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        font = pygame.font.SysFont('Arial', size_font) #шрифт
        self.buttonSurf = font.render(text, True, (20, 20, 20))

        # ==== адаптируем размер шрифта ====
        if edit_size:
            while (self.buttonSurf.get_width() > width - 20 or 
                self.buttonSurf.get_height() > height - 20) and size_font > 10:
                size_font -= 2
                font = pygame.font.SysFont('Arial', size_font)
                self.buttonSurf = font.render(text, True, (20, 20, 20))

        self.alreadyPressed = False
        self.push = False

    
    def process(self, screen): 

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover']) #есть ли внутри кнопки

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.push == False:
                    self.buttonSurface.fill(self.fillColors['pressed'])

                    if self.onclickFunction:
                        self.onclickFunction()
                    self.push = True


            else:
                self.alreadyPressed = False
                self.push = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

class ImageButton():
    def __init__(   self, x, y,  image_normal, image_hover=None, 
                    image_pressed=None, onclickFunction=None):

        self.x = x
        self.y = y
        self.onclickFunction = onclickFunction
        
        # Загружаем изображения
        self.image_normal = image_normal
        self.width = self.image_normal.get_width()
        self.height = self.image_normal.get_height()
        
        self.image_hover = image_hover if image_hover else self.image_normal
        self.image_pressed = image_pressed if image_pressed else self.image_normal
        
        self.buttonSurface = self.image_normal
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.push = False
    
    def process(self, screen):
        mousePos = pygame.mouse.get_pos()
        
        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]:
                if not self.push:
                    self.buttonSurface = self.image_pressed
                    if self.onclickFunction:
                        self.onclickFunction()
                    self.push = True
                else:
                    self.buttonSurface = self.image_pressed
            else:
                self.buttonSurface = self.image_hover
                self.push = False
        else:
            self.buttonSurface = self.image_normal
            self.push = False
        
        screen.blit(self.buttonSurface, self.buttonRect)

    def configure(self, x: int | None= None, y: int | None= None, image_normal = None, image_hover=None, 
                    image_pressed=None, onclickFunction=None):
        '''EditButton parameter changes'''
        if x: self.x = x
        if y: self.y = y
        if image_normal:    self.image_normal = image_normal
        self.image_hover = image_hover if image_hover else self.image_normal
        self.image_pressed = image_pressed if image_pressed else self.image_normal


        if onclickFunction:
            if callable(onclickFunction):
                self.onclickFunction = onclickFunction

        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)


class Button(pygame.sprite.Sprite):
    def __init__(   self, x, y, width, height,
                    command = None,
                    text = None,
                    image = None,
                    color = (109, 107, 83),
                    label_text = None):
        from core.state_game import G
        pygame.sprite.Sprite.__init__(self)
        ''' кнопка
            width, height - размеры кнопки относительно G.GRID
            x, y - location
            label_text - text on hover'''
        
        if image:
            try:
                self.image = pygame.Surface(image)
                self.rect = self.image.get_rect()
            except Exception as e: 
                Log.warning('class Button:', e)
                self.image = pygame.Surface((G.GRID, G.GRID))
                self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((G.GRID * width, G.GRID * height))
            try:
                self.image.fill(color) 
            except Exception as e:
                Log.warning('class Button:', e)
                self.image.fill( (109, 107, 83) )
            self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if callable(command):
            self.command = command
        else: self.command = None
        self.press = False
        self.text = ''

        if isinstance(text, str):
            self.text = G.font_btn_wid_1.render(text, True, (20, 20, 20))

        self.label = False
        if isinstance(label_text, str):     # текст пометки при наведении курсора
            self.label_text = G.font_btn_wid_1.render(label_text, True, (20, 20, 20))
            self.label = True

    def update(self, screen): 
        if self.text:
            screen.blit(self.text, (self.rect.x, self.rect.y))        # type: ignore

        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):    # type: ignore
            if self.label: # если пометка есть
                screen.blit(self.label_text, (self.rect.x, self.rect.y))    # type: ignore

            if pygame.mouse.get_pressed()[0]  : # лкм
                try:
                    if self.press == False and self.command != None:
                        self.command()
                        self.press = True
                        print('press')
                except AttributeError:  pass

            else: self.press = False