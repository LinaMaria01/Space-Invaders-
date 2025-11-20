"""
Clase de proyectiles (balas)
"""
import pygame
from config import *

class Bullet:
    def __init__(self, x, y, direction=1):
        """
        Inicializa una bala
        direction: 1 = arriba (jugador), -1 = abajo (enemigo)
        """
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.direction = direction
        self.speed = BULLET_SPEED if direction == 1 else ENEMY_BULLET_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        """Actualiza la posición de la bala"""
        self.y -= self.speed * self.direction
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        """Verifica si la bala salió de la pantalla"""
        return self.y < 0 or self.y > SCREEN_HEIGHT
    
    def draw(self, screen):
        """Dibuja la bala"""
        if self.direction == 1:
            # Bala del jugador (cyan brillante)
            pygame.draw.rect(screen, CYAN, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 1)
        else:
            # Bala del enemigo (roja)
            pygame.draw.rect(screen, RED, self.rect)
            pygame.draw.rect(screen, YELLOW, self.rect, 1)