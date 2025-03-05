import pygame_widgets
import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import json
def setting():

    pygame.font.init()
    from main import CONFIG, screen, WIDTH, HEIGHT
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render('Показ FPS', True, (180, 0, 0))
    if CONFIG["FPS_see"] == False: n_dropd_1 = "выключен"
    else: n_dropd_1 = "включён"
    dropdown_1 = Dropdown(
        screen, WIDTH//5, HEIGHT//6, 200, 100, name = n_dropd_1,
        choices=[
            "выключен",
            "включён"
        ],
        borderRadius=3, colour=pygame.Color('green'), values=[False, True], direction='down', textHAlign='left'
    )
    text2 = f1.render('Матрица', True, (180, 0, 0))
    if CONFIG["matrix"] == False: n_dropd_2 = "выключен"
    else: n_dropd_2 = "включён"
    dropdown_2 = Dropdown(
        screen, WIDTH//5, HEIGHT//3, 200, 100, name = n_dropd_2,
        choices=[
            "выключен",
            "включён"
        ],
        borderRadius=3, colour=pygame.Color('green'), values=[False, True], direction='down', textHAlign='left'
    )
    text3 = f1.render('разрешение', True, (180, 0, 0))
    if CONFIG["resolution"] == "ful": n_dropd_3 = "полный экран"
    else: n_dropd_3 = "1920x1080"
    dropdown_3 = Dropdown(
        screen, WIDTH//2, HEIGHT//6, 200, 100, name = n_dropd_3,
        choices=[
            "полный экран",
            "1920x1080"
        ],
        borderRadius=3, colour=pygame.Color('green'), values=["полный экран", "1920x1080"], direction='down', textHAlign='left'
    )

    def stop_setting():

        if dropdown_1.getSelected() != None:CONFIG["FPS_see"] = dropdown_1.getSelected()
        if dropdown_2.getSelected() != None:CONFIG["matrix"] = dropdown_2.getSelected()
        if dropdown_3.getSelected() != None:CONFIG["resolution"] = dropdown_3.getSelected()
        with open('setting.json', 'w',encoding='utf-8') as json_file:json.dump(CONFIG, json_file, indent=4)



    button = Button(
        screen, WIDTH//1.07, HEIGHT//1.07, 100, 50, text = "Сохранить", fontSize=30,
        margin=20, inactiveColour = (255, 0, 0), pressedColour=(0, 255, 0),
        radius=5, onClick=stop_setting, font=pygame.font.SysFont('calibri', 10),
        textVAlign='bottom'
    )
    textF = f1.render("Мало врагов? Нажми F2.", True, (180, 0, 0))
    textV = f1.render('версия: 0.1, "Милая"', True, (180, 0, 0))
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: break

        screen.fill((255, 255, 255))
        screen.blit(text1, (WIDTH//11, HEIGHT//6))
        screen.blit(text2, (WIDTH//11, HEIGHT//3))
        screen.blit(text3, (WIDTH//2.5, HEIGHT//6))
        screen.blit(textF, (WIDTH//5, HEIGHT//1.5))
        screen.blit(textV, (WIDTH//5, HEIGHT//1.35))
        pygame_widgets.update(events)
        pygame.display.update()

#! используется для предотвращения потери переменной при открытии настроек или окна сохранить игру
def setting_error(): from main import CONFIG, screen, WIDTH, HEIGHT 