import pygame
import settings_RK as S
from entities_RK import TowerRK
from waves_RK import WaveManagerRK
from ui_RK import UIButtonRK, UIOverlayRK
from utils_RK import dist_RK

def snap_to_grid_RK(pos):
    x, y = pos
    gx = (x // S.GRID_SIZE) * S.GRID_SIZE + S.GRID_SIZE // 2
    gy = (y // S.GRID_SIZE) * S.GRID_SIZE + S.GRID_SIZE // 2
    return (gx, gy)

def is_on_path_RK(pos, path_points, threshold=25):
    for p in path_points:
        if dist_RK(pos, p) < threshold:
            return True
    return False

def main_RK():
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()

    ui = UIOverlayRK()

    enemies = []
    towers = []
    projectiles = []

    gold = S.START_GOLD
    lives = S.START_LIVES

    wave_mgr = WaveManagerRK(S.PATH_POINTS)

    def start_wave_RK():
        if not wave_mgr.wave_in_progress:
            wave_mgr.start_next_wave_RK()

    start_button = UIButtonRK((S.WIDTH - 180, 6, 170, 28), "Start Next Wave (N)", start_wave_RK)

    running = True
    game_over = False
    win = False

    while running:
        dt = clock.tick(S.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            start_button.handle_event_RK(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    start_wave_RK()
                if event.key == pygame.K_r and (game_over or win):
                    return main_RK()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not (game_over or win):
                mx, my = event.pos
                if my <= 40:
                    continue

                place_pos = snap_to_grid_RK(event.pos)

                if gold >= S.TOWER_COST and not is_on_path_RK(place_pos, S.PATH_POINTS):
                    towers.append(TowerRK(place_pos))
                    gold -= S.TOWER_COST

        if game_over or win:
            screen.fill(S.BLACK)
            msg = "GAME OVER (R to restart)" if game_over else "YOU WIN! (R to restart)"
            ui.draw_message_center_RK(screen, msg)
            pygame.display.flip()
            continue

        wave_mgr.update_RK(dt, enemies)

        for e in enemies:
            e.update_RK(dt)

        for e in enemies:
            if e.reached_end and e.alive:
                e.alive = False
                lives -= 1
                if lives <= 0:
                    game_over = True

        for t in towers:
            t.update_RK(dt, enemies, projectiles)

        for p in projectiles:
            p.update_RK(dt)

        projectiles = [p for p in projectiles if p.alive]

        for e in enemies:
            if not e.alive and not getattr(e, "_rewarded", False) and not e.reached_end:
                gold += e.reward
                e._rewarded = True

        if wave_mgr.finished and all((not e.alive) or e.reached_end for e in enemies):
            win = True

        screen.fill(S.GRAY)

        for x in range(0, S.WIDTH, S.GRID_SIZE):
            pygame.draw.line(screen, (100, 100, 100), (x, 40), (x, S.HEIGHT))
        for y in range(40, S.HEIGHT, S.GRID_SIZE):
            pygame.draw.line(screen, (100, 100, 100), (0, y), (S.WIDTH, y))

        pygame.draw.lines(screen, S.DARK, False, S.PATH_POINTS, 8)
        for pnt in S.PATH_POINTS:
            pygame.draw.circle(screen, S.BLACK, pnt, 8)

        for t in towers:
            t.draw_RK(screen)
        for e in enemies:
            if e.alive:
                e.draw_RK(screen)
        for p in projectiles:
            p.draw_RK(screen)

        ui.draw_hud_RK(screen, gold, lives, wave_mgr.current_wave, wave_mgr.wave_in_progress, wave_mgr.finished)
        start_button.draw_RK(screen, ui.font)
        ui.draw_hint_RK(screen, f"Click to place tower ({S.TOWER_COST} gold). Avoid path.")

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_RK()
