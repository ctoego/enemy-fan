import pygame
import os


"""файл для вынесения некоторых функций из основного кода"""



# загрузка изображений
def img(IMAGE, WIDTH, HEIGHT, GRID):

    # матрица
    ns_0 = pygame.image.load("./image/matrix/s_0.jpg").convert()
    ns_1 = pygame.image.load("./image/matrix/s_1.jpg").convert()
    ns_2 = pygame.image.load("./image/matrix/s_2.jpg").convert()
    ns_3 = pygame.image.load("./image/matrix/s_3.jpg").convert()
    ns_4 = pygame.image.load("./image/matrix/s_4.jpg").convert()
    ns_5 = pygame.image.load("./image/matrix/s_5.jpg").convert()
    ns_6 = pygame.image.load("./image/matrix/s_6.jpg").convert()
    ns_7 = pygame.image.load("./image/matrix/s_7.jpg").convert()
    ns_8 = pygame.image.load("./image/matrix/s_8.jpg").convert()
    ns_9 = pygame.image.load("./image/matrix/s_9.jpg").convert()
    number = [ns_0 ,ns_1 ,ns_2, ns_3, ns_4,ns_5, ns_6, ns_7, ns_8, ns_9]
    counter = 0
    for t in number:
        im = pygame.transform.scale(t, (GRID*2, GRID*2))
        IMAGE["numbers"][counter] = im
        counter += 1
    
    background_1 = pygame.image.load("./image/background.png").convert()
    background_1 = pygame.transform.scale(background_1, (WIDTH, HEIGHT))
    IMAGE["background"]["main"] = background_1
    w = []
    for number in range(1, len(os.listdir("./image/zombie_1/left"))):
        im = pygame.image.load(f"./image/zombie_1/left/({number}).png").convert_alpha()
        w.append(im)
    IMAGE["zombie"]["1"]['left'] = w
    w = []
    for number in range(1, len(os.listdir("./image/zombie_1/right"))):
        im = pygame.image.load(f"./image/zombie_1/right/({number}).png").convert_alpha()
        w.append(im)
    IMAGE["zombie"]["1"]['right'] = w
    
    w = []
    for number in range(1, len(os.listdir("./image/zombie_2/left"))):
        im = pygame.image.load(f"./image/zombie_2/left/({number}).png").convert_alpha()
        w.append(im)
    IMAGE["zombie"]["2"]['left'] = w
    w = []
    for number in range(1, len(os.listdir("./image/zombie_2/right"))):
        im = pygame.image.load(f"./image/zombie_2/right/({number}).png").convert_alpha()
        w.append(im)
    IMAGE["zombie"]["2"]['right'] = w


    return IMAGE

# вычисление сетки

def grids_config(MAPS, GRID, mousex, mousey): # находим клетку на которой находится курсор

    rows, cols = MAPS.shape
    if mousex//GRID < 0 or mousex//GRID >= rows:
        return False
    if mousey//GRID < 0 or mousey//GRID >= cols:
        return False
    return mousex//GRID, mousey//GRID



