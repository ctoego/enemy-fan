
import pygame
'''
    Console
'''


class DevConsole:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.visible = False
        self.input_text = ""
        self.history = []
        self.font = pygame.font.Font(None, 24)
        
        # Цвета
        self.bg_color = (0, 0, 0, 180)  # черный с прозрачностью
        self.text_color = (0, 255, 0)   # зеленый текст
        
    def toggle(self):
        """Открыть/закрыть консоль"""
        self.visible = not self.visible
        if self.visible:
            self.input_text = ""
    
    def handle_event(self, event):
        """Обработка ввода"""
        if not self.visible:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Enter - выполнить команду
                self.execute_command(self.input_text)
                self.input_text = ""
                return True
            elif event.key == pygame.K_BACKSPACE:  # Backspace
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_ESCAPE:  # Esc - закрыть
                self.visible = False
            else:
                # Добавляем символ
                self.input_text += event.unicode
        return True
    
    def execute_command(self, command):
        """Выполнить команду"""
        if not command:
            return
        
        # Добавляем в историю
        self.history.append(f"> {command}")
        
        # Разбираем команду
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]

        # Доступные команды
        if cmd == "help":
            self.history.extend([
                "Доступные команды:",
                "  help - показать помощь",
                "  clear - очистить консоль",
                "  wave [число] - установить волну",
                "  health [число] - установить здоровье",
                "  killall - убить всех зомби",
                "  godmode - бессмертие базы",
                "  fps [число] - изменить FPS",
                "  exit/close - закрыть консоль",
                "  screen - информация экрана"
            ])

        elif cmd == "clear":
            self.history.clear()
        elif cmd == "screen":
            from core.state_game import G
            try:
                self.history.append(f"Камера: карта { G.MAP_COUNT_WIDTH * G.GRID }x{G.MAP_COUNT_HEIGHT * G.GRID }")
                self.history.append(f"Камера: экран { G.WIDTH }x{ G.HEIGHT }")
            except:
                self.history.append("Неизвестная ошибочка")
        elif cmd == "wave" and args:

            try:
                from core.state_game import G
                G.WAVE = int(args[0])
                self.history.append(f"Волна установлена на {G.WAVE}")
            except:
                self.history.append("Ошибка: нужно число")
        
        elif cmd == "health" and args:
            try:
                from core.state_game import G
                G.health = int(args[0])
                self.history.append(f"Здоровье базы: {G.health}")
            except:
                self.history.append("Ошибка: нужно число")
        
        elif cmd == "spawn" and args:
            count = int(args[1]) if len(args) > 1 else 1
            self.history.append(f"Создано {count} зомби (пока заглушка)")
            # Здесь код создания зомби
        
        elif cmd == "killall":
            self.history.append("Все зомби убиты")
            from core.sprite_group import SG
            SG.all_sprites_zobies.empty()
        
        elif cmd == "godmode":
            from core.state_game import G
            G.health = 9999999
            self.history.append("Godmode активирован!")
        
        elif cmd == "fps" and args:
            try:
                from core.state_game import G
                G.FPS = int(args[0])
                self.history.append(f"FPS установлен на {G.FPS}")
            except:
                self.history.append("Ошибка: нужно число")
        
        elif cmd in ["exit", "close"]:
            self.visible = False
        
        else:
            self.history.append(f"Неизвестная команда: {cmd}. Введите 'help'")
        
        # Ограничиваем историю
        if len(self.history) > 20:
            self.history.pop(0)
    
    def draw(self):
        """Отрисовка консоли"""
        if not self.visible:
            return
        
        # Полупрозрачный фон
        console_surface = pygame.Surface((self.width, self.height//2))
        console_surface.set_alpha(180)
        console_surface.fill((0, 0, 0))
        self.screen.blit(console_surface, (0, 0))
        
        # История команд
        y = 10
        for line in self.history[-15:]:  # показываем последние 15 строк
            text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (10, y))
            y += 25
        
        # Текущий ввод
        input_display = f"> {self.input_text}"
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 else " "
        input_surface = self.font.render(input_display + cursor, True, self.text_color)
        self.screen.blit(input_surface, (10, y + 10))