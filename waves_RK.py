import settings_RK as S
from entities_RK import EnemyRK

class WaveManagerRK:
    def __init__(self, path_points):
        self.path = path_points

        self.waves = [
            (6, 0.9, 1.0, 1.0),
            (10, 0.7, 1.2, 1.05),
            (14, 0.6, 1.5, 1.10),
        ]

        self.current_wave = -1
        self.to_spawn = 0
        self.spawn_interval = 1.0
        self.spawn_timer = 0.0
        self.hp_mult = 1.0
        self.speed_mult = 1.0
        self.wave_in_progress = False
        self.finished = False

    def start_next_wave_RK(self):
        if self.finished:
            return
        self.current_wave += 1
        if self.current_wave >= len(self.waves):
            self.finished = True
            self.wave_in_progress = False
            return

        count, interval, hp_m, sp_m = self.waves[self.current_wave]
        self.to_spawn = count
        self.spawn_interval = interval
        self.spawn_timer = 0.0
        self.hp_mult = hp_m
        self.speed_mult = sp_m
        self.wave_in_progress = True

    def update_RK(self, dt, enemies):
        if not self.wave_in_progress:
            return

        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and self.to_spawn > 0:
            hp = int(S.ENEMY_BASE_HP * self.hp_mult)
            speed = S.ENEMY_BASE_SPEED * self.speed_mult
            reward = S.KILL_REWARD
            enemies.append(EnemyRK(self.path, hp, speed, reward))

            self.to_spawn -= 1
            self.spawn_timer = self.spawn_interval

        if self.to_spawn <= 0:
            if all((not e.alive) or e.reached_end for e in enemies):
                self.wave_in_progress = False
