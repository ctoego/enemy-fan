

class Camera:
    '''камера для передвижения по карте'''

    def __init__(self, map_width: int, map_height: int, screen_width: int, screen_height: int ):
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.x: int = map_width //4      # Смещение камеры
        self.y: int = map_height //4

        self.max_x: int = max(0, self.map_width - self.screen_width)
        self.max_y: int = max(0, self.map_height - self.screen_height)

        self.mode = 'manual'

    def set_mode(self, mode: str):
        self.mode = mode
    
    def toggle_mode(self, s: bool):
        self.mode = "follow" if s else "manual"
    
    def update(self, target_x=None, target_y=None):
        if self.mode == "follow" and target_x is not None  and target_y is not None:
            desired_x = target_x - self.screen_width // 2
            desired_y = target_y - self.screen_height // 2
            self.x = max(0, min(int(desired_x//1.3), self.max_x))
            self.y = max(0, min(int(desired_y//1.3), self.max_y))
    
    def move(self, dx, dy):
        if self.mode == "manual":
            self.x += dx
            self.y += dy
            self.x = max(0, min(self.x, self.max_x))
            self.y = max(0, min(self.y, self.max_y))

    def apply(self, rect):
        """Преобразует мировой rect в экранный (с учётом камеры)"""
        return rect.move(-self.x, -self.y)
    
    def apply_xy(self, x, y):
        """Преобразует мировые координаты в экранные"""
        return x - self.x, y - self.y