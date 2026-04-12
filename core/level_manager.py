
class LM:
    ''' Level Manager - manager for spawn enemy, difficulty level, type enemy, style map
    score = int(wave*1.5 * (1 + difficulty_level * 0.7))
        Args:
            score: int количество очков для спавна врагов
            wave: int номер волны 
            difficulty_level: int уровень сложности, зависит от уровня '''
    level_config: dict = {}     # storing in folder 'level'
    difficulty_level: int = 1
    count_wave: int = 1
    enemy_spawn: dict = {}
    enemy_config: dict = {}
    sum_score_enemy: int = 0

    selected_card: set = set()  # Какие карты выбраны на уровень



    @classmethod
    def init_enemy(cls, config) -> None:
        if config:
            cls.enemy_config = config

    @classmethod
    def new_level(cls, config: dict) -> None:
        cls.enemy_spawn = {}
        if config:
            cls.level_config = config
            cls.difficulty_level = config['difficulty_level']
            cls.count_wave = config['count_wave']
            for y in config['enemy']:
                x = config['enemy'][y]
                if x == 'all':
                    cls.enemy_spawn[y] = (0, cls.count_wave, cls.enemy_config[y]['score'])
                elif x.split('-')[1] == 'end':
                    cls.enemy_spawn[y] = (int(x.split('-')[0]), cls.count_wave, cls.enemy_config[y]['score'])
                else:
                    cls.enemy_spawn[y] = (int(x.split('-')[0]), int(x.split('-')[1]), cls.enemy_config[y]['score'])


    @classmethod
    def new_WAVE(cls, wave: int):
        score = int(wave * (1 + cls.difficulty_level * 0.7))
        from sprites.zombies import ZM
        for y in cls.enemy_spawn:
            if cls.enemy_spawn[y][0] <= wave <= cls.enemy_spawn[y][1]:
                f = score // cls.enemy_spawn[y][2]
                if f > 0:
                    for _ in range(f):
                        ZM.create_zombie(y)