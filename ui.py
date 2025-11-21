import pygame
import settings as S

class UIButton:
    def __init__(self, rect, text, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, screen, font):
        color = (70, 70, 70) if self.hover else (50, 50, 50)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, S.WHITE, self.rect, 2, border_radius=8)

        surf = font.render(self.text, True, S.WHITE)
        screen.blit(surf, surf.get_rect(center=self.rect.center))


class UIOverlay:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 18)
        self.big = pygame.font.SysFont("consolas", 36)

    def draw_hud(self, screen, gold, lives, wave_idx, wave_active, finished):
        pygame.draw.rect(screen, (0,0,0), (0,0,S.WIDTH,40))
        txt = f"Gold: {gold}   Lives: {lives}   Wave: {wave_idx+1}   Active: {wave_active}"

        if finished:
            txt += "   (ALL WAVES CLEARED)"

        surf = self.font.render(txt, True, S.WHITE)
        screen.blit(surf, (10, 10))

    def draw_message_center(self, screen, msg):
        surf = self.big.render(msg, True, S.WHITE)
        r = surf.get_rect(center=(S.WIDTH//2, S.HEIGHT//2))
        screen.blit(surf, r)

    def draw_hint(self, screen, msg):
        surf = self.font.render(msg, True, S.WHITE)
        screen.blit(surf, (10, S.HEIGHT - 28))
