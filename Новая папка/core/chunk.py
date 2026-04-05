import pygame
from core.state_game import G

class Chunk:
    SIZE = 16

    def __init__(self, x: int, y: int, grid_size: int):
        self.chunk_x = x
        self.chunk_y = y
        self.grid_size = grid_size
        self.surface = None
        self.is_dirty = True
        self.world_x = x * grid_size * self.SIZE
        self.world_y = y * grid_size * self.SIZE

    def mark_dirty(self):
        self.is_dirty = True

    def rebuild(self, map_sprites):
        chunk_width_px = self.SIZE * self.grid_size
        self.surface = pygame.Surface((chunk_width_px, chunk_width_px))
        
        # Границы чанка в КЛЕТКАХ
        chunk_start_x = self.chunk_x * self.SIZE
        chunk_start_y = self.chunk_y * self.SIZE
        chunk_end_x = chunk_start_x + self.SIZE
        chunk_end_y = chunk_start_y + self.SIZE
        
        for sprite in map_sprites:
            # Получаем координаты КЛЕТКИ (не пиксели!)
            if hasattr(sprite, 'grid_x'):
                gx, gy = sprite.grid_x, sprite.grid_y
            elif hasattr(sprite, 'number'):
                gx, gy = sprite.number
            else:
                continue
            
            # Сравниваем клетки с клетками
            if (chunk_start_x <= gx < chunk_end_x and
                chunk_start_y <= gy < chunk_end_y):
                
                # Локальные координаты в ПИКСЕЛЯХ
                local_x = (gx - chunk_start_x) * self.grid_size
                local_y = (gy - chunk_start_y) * self.grid_size
                self.surface.blit(sprite.image, (local_x, local_y))
        
        self.is_dirty = False

    def draw(self, screen, camera_x, camera_y):
        if self.surface:
            screen.blit(self.surface, (self.world_x - camera_x, self.world_y - camera_y))


class ChunkManager:
    def __init__(self, map_width_cells: int, map_height_cells: int, grid_size: int):
        self.grid_size = grid_size
        self.chunk_size = Chunk.SIZE
        self.chunks_x = (map_width_cells + self.chunk_size - 1) // self.chunk_size
        self.chunks_y = (map_height_cells + self.chunk_size - 1) // self.chunk_size
        
        self.chunks = {}
        for cx in range(self.chunks_x):
            for cy in range(self.chunks_y):
                self.chunks[(cx, cy)] = Chunk(cx, cy, grid_size)
    
    def mark_cell_dirty(self, grid_x: int, grid_y: int):
        chunk_x = grid_x // Chunk.SIZE
        chunk_y = grid_y // Chunk.SIZE
        chunk = self.chunks.get((chunk_x, chunk_y))
        if chunk:
            chunk.mark_dirty()
    
    def rebuild_dirty_chunks(self, map_sprites):
        for chunk in self.chunks.values():
            if chunk.is_dirty:
                chunk.rebuild(map_sprites)
    
    def draw(self, screen, camera_x: int, camera_y: int):
        start_chunk_x = max(0, camera_x // (Chunk.SIZE * self.grid_size))
        end_chunk_x = min(self.chunks_x, 
                         (camera_x + screen.get_width()) // (Chunk.SIZE * self.grid_size) + 2)
        start_chunk_y = max(0, camera_y // (Chunk.SIZE * self.grid_size))
        end_chunk_y = min(self.chunks_y,
                         (camera_y + screen.get_height()) // (Chunk.SIZE * self.grid_size) + 2)
        
        for cx in range(start_chunk_x, end_chunk_x):
            for cy in range(start_chunk_y, end_chunk_y):
                chunk = self.chunks.get((cx, cy))
                if chunk:
                    chunk.draw(screen, camera_x, camera_y)