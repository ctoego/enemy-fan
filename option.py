import pygame
import tkinter as tk
from tkinter import ttk  
from tkinter import *
import random
import json, os
"""файл для вынесения некоторых функций из основного кода"""



# загрузка изображений
def img(IMAGE):
    from main import WIDTH, HEIGHT, GRID
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
    for i in range(0, 10): IMAGE["numbers"][i] = number[i]
    background_1 = pygame.image.load("./image/background.png").convert()
    background_1 = pygame.transform.scale(background_1, (WIDTH, HEIGHT))
    IMAGE["background"]["main"] = background_1


    return IMAGE

# вычисление сетки

def grids_config(): # находим клетку на которой находится курсор
    
    from main import MAPS, GRID, mousex, mousey

    for y in MAPS:
        if mousey - MAPS[y]["y"] <= GRID and mousex - MAPS[y]["x"] <= GRID:
            return y

def grids_config_yours(mousex, mousey): # находим клетку со своими параметрами
    from main import MAPS, GRID

    for y in MAPS:
        if mousey - MAPS[y]["y"] <= GRID and mousex - MAPS[y]["x"] <= GRID:
            return y

def loading_game():
    root = tk.Tk()
    root.geometry("500x300")
    root.title("загрузка игры")
    root.resizable(0, 0) # размер окна
    #отключение верхней панели
    root.attributes("-toolwindow", True)
    #приоритет
    root.attributes("-topmost",True)


    canvas = tk.Canvas(root, width=500, height=300, scrollregion=(0, 0, 1000, 1000))
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    canvas.place(x=0, y=0)
                # Создаем скроллбары
    scrollbar_v = tk.Scrollbar(root, orient=tk.VERTICAL)
    scrollbar_h = tk.Scrollbar(root, orient=tk.HORIZONTAL)

                # Связываем скроллбары с Canvas
    canvas.configure(yscrollcommand=scrollbar_v.set)
    canvas.configure(xscrollcommand=scrollbar_h.set)
    scrollbar_v.configure(command=canvas.yview)
    scrollbar_h.configure(command=canvas.xview)

                # Добавляем скроллбары в окно
    scrollbar_v.pack(side=tk.RIGHT,ipady=10, padx=10, fill=tk.Y)
    scrollbar_h.pack(side=tk.BOTTOM,ipady=10, padx=10, fill=tk.X)
                    
                # Создаем рамку для Canvas
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')
    def loading(cat_f):   

        with open(cat_f, 'r',encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
        
        root.destroy()
    def find():
         
        for root, dirs, files in os.walk("./save/"):
            for file in files:
                if file.count(".json"):
                    cat_f = os.path.join(root, file)

                    btn_finder = ttk.Button(frame, text = file, command=lambda cat_f=cat_f: loading(cat_f)).pack()   
                

    find()
    root.mainloop()
