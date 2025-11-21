import pygame
from utils import dist
import settings as S

vec = pygame.math.Vector2

class Enemy:
    def __init__(self, path_points, hp, speed, reward):
        self.path = [vec(p) for p in path_points]
        self.pos = self.path[0].copy()
        self.target_index = 1

        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.reward = reward

        self.radius = S.ENEMY_RADIUS
        self.alive = True
        self.reached_end = False

    def update(self, dt):
        if not self.alive or self.reached_end:
            return

        if self.target_index >= len(self.path):
            self.reached_end = True
            return

        target = self.path[self.target_index]
        direction = target - self.pos
        d = direction.length()

        if d < 1e-6:
            self.target_index += 1
            return

        direction.normalize_ip()
        step = self.speed * dt

        if step >= d:
            self.pos = target
            self.target_index += 1
        else:
            self.pos += direction * step

    def take_damage(self, dmg):
        if not self.alive:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, S.RED, self.pos, self.radius)

        bar_w = 28
        bar_h = 5
        x = self.pos.x - bar_w / 2
        y = self.pos.y - self.radius - 10
        ratio = max(0, self.hp / self.max_hp)

        pygame.draw.rect(screen, S.DARK, (x, y, bar_w, bar_h))
        pygame.draw.rect(screen, S.GREEN, (x, y, bar_w * ratio, bar_h))


class Projectile:
    def __init__(self, pos, target, damage):
        self.pos = vec(pos)
        self.target = target
        self.damage = damage
        self.speed = S.PROJECTILE_SPEED
        self.radius = S.PROJECTILE_RADIUS
        self.alive = True

    def update(self, dt):
        if not self.alive or not self.target.alive:
            self.alive = False
            return

        direction = self.target.pos - self.pos
        d = direction.length()

        if d < 2.0:
            self.target.take_damage(self.damage)
            self.alive = False
            return

        direction.normalize_ip()
        self.pos += direction * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, S.YELLOW, self.pos, self.radius)


class Tower:
    def __init__(self, pos):
        self.pos = vec(pos)
        self.range = S.TOWER_RANGE
        self.damage = S.TOWER_DAMAGE
        self.fire_rate = S.TOWER_FIRE_RATE
        self.cooldown = 0.0
        self.radius = S.TOWER_RADIUS
        self.selected = False

    def update(self, dt, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= dt

        target = None
        best_d = 1e9
        for e in enemies:
            if not e.alive or e.reached_end:
                continue
            d = dist(self.pos, e.pos)
            if d <= self.range and d < best_d:
                best_d = d
                target = e

        if target and self.cooldown <= 0:
            projectiles.append(Projectile(self.pos, target, self.damage))
            self.cooldown = 1.0 / self.fire_rate

    def draw(self, screen):
        pygame.draw.circle(screen, S.BLUE, self.pos, self.radius)
        pygame.draw.circle(screen, S.CYAN, self.pos, self.range, 1)

        if self.selected:
            pygame.draw.circle(screen, S.WHITE, self.pos, self.radius + 3, 2)
