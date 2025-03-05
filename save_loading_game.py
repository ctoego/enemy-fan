import tkinter as tk
from tkinter import ttk  
import json
import os

def save_game():
    from main import MAPS, VOLUME_TURRENT, VOLUME_WINDOW
    root = tk.Tk()
    root.geometry("500x300")
    root.title("сохранение игры")
    root.resizable(0, 0) # размер окна
    #отключение верхней панели
    root.attributes("-toolwindow", True)
    #приоритет
    root.attributes("-topmost",True)


    # запрещаем закрывать окно
    def disable_event():    pass
    
    root.protocol("WM_DELETE_WINDOW", disable_event)
    lbl_1 = ttk.Label(root, text = "Введите название сохранения")
    entry_1 = ttk.Entry(root)
    def okey():
        file = {}
        file["MAPS"] = MAPS
        file["VOLUME_TURRENT"] = VOLUME_TURRENT
        file["VOLUME_WINDOW"] = VOLUME_WINDOW
        text = "./save/" + entry_1.get() + ".json"
        with open(text, 'w') as json_file:
            json.dump(file, json_file, indent=4) # запись в файл
        root.destroy()
    btn_1 = ttk.Button(root,text = "сохранить",command = okey)
    btn_2 = ttk.Button(root,text = "отмена",command = lambda: root.destroy())
    lbl_1.pack()
    entry_1.pack()
    btn_1.pack()
    btn_2.pack()
    root.mainloop()
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
        global data
        with open(cat_f, 'r',encoding='utf-8') as json_file:
            data = json.load(json_file)
        root.destroy()
        
        
    def find():
        
        for root, dirs, files in os.walk("./save/"):
            for file in files:
                if file.count(".json"):
                    cat_f = os.path.join(root, file)

                    btn_finder = ttk.Button(frame, text = file, command=lambda cat_f=cat_f: loading(cat_f)).pack()   
                

    find()
    root.mainloop()
    try:
        return data
    except: return None