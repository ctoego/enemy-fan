import pygame

from core.state_game import G
from core.chunk import ChunkManager



class SG:
    ''' SpriteGroup,  storing variables group sprites 
        Отрисовка, управление спрайтами
    '''

    sprite_card: set = set()

    all_sprites_map = pygame.sprite.Group()     # карта
    all_sprites_window = pygame.sprite.Group()  # шипы

    all_sprites_spawn = pygame.sprite.Group()   # один на карту, куда идут враги, а мы защищаем

    all_sprites_zobies = pygame.sprite.Group()  # зомби
    all_sprites_bullet = pygame.sprite.Group()  # снаряды
    all_sprites_turent = pygame.sprite.Group()  # турели 
    all_sprites_matrix = pygame.sprite.Group()  # матрица на главном экране

    # кнопки

    all_sprites_menu_game = pygame.sprite.Group()
    all_sprites_arrow = pygame.sprite.Group()

    _cached_map_surface = None
    _cached_map_size = (0, 0)

    chunk_manager = None  # менеджер чанков

    @classmethod
    def clear_sprites_group(cls):
        # Очищаем группы (удаляем все спрайты)
        cls.all_sprites_map.empty()
        cls.all_sprites_window.empty()
        cls.all_sprites_spawn.empty()
        cls.all_sprites_turent.empty()
        cls.all_sprites_zobies.empty()
        cls.all_sprites_bullet.empty()
        cls._cached_map_surface = None

    @classmethod
    def init_sprite_card(cls, d: set):
        cls.sprite_card = d
    @classmethod
    def init_chunks(cls):
        cls.chunk_manager = ChunkManager(
            G.MAP_COUNT_WIDTH,
            G.MAP_COUNT_HEIGHT,
            G.GRID
        )
    @classmethod
    def rebuild_all_chunks(cls):
        """Перестроить все чанки (при старте игры)"""
        if cls.chunk_manager:
            for chunk in cls.chunk_manager.chunks.values():
                chunk.mark_dirty()
            cls.chunk_manager.rebuild_dirty_chunks(cls.all_sprites_map)
    
    @classmethod
    def mark_cell_dirty(cls, grid_x: int, grid_y: int):
        """Пометить клетку как изменённую"""
        if cls.chunk_manager:
            cls.chunk_manager.mark_cell_dirty(grid_x, grid_y)
    
    @classmethod
    def endless_mode_render(cls, screen):
        camera = G.camera


        if cls.chunk_manager:
            cls.chunk_manager.rebuild_dirty_chunks(cls.all_sprites_map)

        if cls.chunk_manager and camera:
            # Рисуем чанки
            cls.chunk_manager.draw(screen, camera.x, camera.y)
        else:
            # Fallback без чанков
            cls.all_sprites_map.draw(screen)
        
        # Динамические объекты 
        if camera:
            dynamic_groups = [  cls.all_sprites_spawn, cls.all_sprites_window, 
                                cls.all_sprites_turent, cls.all_sprites_zobies, 
                                cls.all_sprites_bullet]
            for group in dynamic_groups:
                old_positions = [(s.rect.x, s.rect.y) for s in group]
                for s in group:
                    s.rect.x -= camera.x
                    s.rect.y -= camera.y
                group.draw(screen)
                for s, (x, y) in zip(group, old_positions):
                    s.rect.x = x
                    s.rect.y = y
        else:
            cls.all_sprites_spawn.draw(screen)
            cls.all_sprites_window.draw(screen)
            cls.all_sprites_turent.draw(screen)
            cls.all_sprites_zobies.draw(screen)
            cls.all_sprites_bullet.draw(screen)