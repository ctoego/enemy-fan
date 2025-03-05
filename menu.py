import pygame
GREEN = (0, 255, 0)

pygame.init()




class Button_1(): #клас кнопка
    def __init__(self, x, y, width, height, listing , text='Button', onclickFunction = None, size_font = 40 ): #listing - в какой список вбиваем кнопку

        self.listing = listing
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction


        self.fillColors = {   #различные цвета
            'normal': '#00f300',
            'hover': '#3a8334',
            'pressed': '#252e25',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        font = pygame.font.SysFont('Arial', size_font) #шрифт
        self.buttonSurf = font.render(text, True, (20, 20, 20))

        self.alreadyPressed = False
        self.push = False
        self.listing.append(self)
    def loading_lis(self):  return self.listing
    
    def process(self): 
        from main import screen
        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover']) #есть ли внутри кнопки

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.push == False:
                    self.buttonSurface.fill(self.fillColors['pressed'])

                    
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





class Button_2(pygame.sprite.Sprite):
    def __init__(self, x, y,  command,label_text = "", label = False):
        pygame.sprite.Sprite.__init__(self)
        from main import WIDTH, HEIGHT
        self.image = pygame.Surface((WIDTH//38.4, HEIGHT//21.6))
        self.image.fill((109, 107, 83)) 
        self.rect = self.image.get_rect()


        self.rect.x = x
        self.rect.y = y
        self.command = command
        self.press = False
        self.label = label  # пометка при наведении курсора
        self.label_text = label_text    # текст пометки при наведении курсора
        font = pygame.font.SysFont('Arial', WIDTH//96) #шрифт
        self.label_text = font.render(label_text, True, (20, 20, 20))
    def update(self): 
        from main import screen
        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):# соприкосновение
            if self.label == True: # если пометка есть
                screen.blit(self.label_text, (self.rect.x, self.rect.y))

            if pygame.mouse.get_pressed()[0]  : # лкм
                try:
                    if self.press == False:
                        self.command()
                        self.press = True
                except AttributeError:  pass

            else: self.press = False
        
        

class Label_1(pygame.sprite.Sprite):  # информация об учинеке, когда нажимаешь на него
    def __init__(self, x, y, number_sp):
        from main import WIDTH, HEIGHT, PEOPLE
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((WIDTH//6.4, HEIGHT//2.2)) #ширина и высота тнформации
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((100, 100, 50))
        font = pygame.font.SysFont('Arial', WIDTH//96) #шрифт

        self.name = font.render("имя: " + PEOPLE[number_sp]["name"], True, (20, 20, 20))


    def draw(self):
        from main import screen, keys
        self.image.blit(self.name, [
            self.rect.width/8 - self.name.get_rect().width/8,
            self.rect.height/8 - self.name.get_rect().height/8
        ])
        screen.blit(self.image, self.rect)
        
        if keys[pygame.K_ESCAPE]:self.kill()






