"""
Clase del jugador (nave espacial)
"""
import pygame
from config import *

class Player:
    def __init__(self, x, y):
        """Inicializa el jugador"""
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.has_shield = False
        self.invulnerable_timer = 0
        
    def move_left(self):
        """Mueve el jugador a la izquierda"""
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
        self.update_rect()
        
    def move_right(self):
        """Mueve el jugador a la derecha"""
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        self.update_rect()
    
    def set_position_normalized(self, normalized_x):
        """Establece la posición basada en un valor normalizado (0-1)"""
        self.x = int(normalized_x * (SCREEN_WIDTH - self.width))
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        self.update_rect()
    
    def update_rect(self):
        """Actualiza el rectángulo de colisión"""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, current_time):
        """Actualiza el estado del jugador"""
        # Actualizar invulnerabilidad temporal
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
    
    def draw(self, screen):
        """Dibuja el jugador con un diseño moderno"""
        # Cuerpo principal (triángulo)
        points = [
            (self.x + self.width // 2, self.y),  # Punta
            (self.x, self.y + self.height),  # Izquierda
            (self.x + self.width, self.y + self.height)  # Derecha
        ]
        pygame.draw.polygon(screen, CYAN, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
        
        # Cabina (círculo brillante)
        pygame.draw.circle(screen, NEON_GREEN, 
                         (self.x + self.width // 2, self.y + self.height // 2), 8)
        
        # Alas laterales
        pygame.draw.rect(screen, BLUE, 
                        (self.x - 5, self.y + self.height - 10, 10, 10))
        pygame.draw.rect(screen, BLUE, 
                        (self.x + self.width - 5, self.y + self.height - 10, 10, 10))
        
        # Dibujar escudo si está activo
        if self.has_shield:
            shield_radius = max(self.width, self.height) // 2 + 10
            pygame.draw.circle(screen, BLUE, 
                             (self.x + self.width // 2, self.y + self.height // 2), 
                             shield_radius, 3)
            pygame.draw.circle(screen, CYAN, 
                             (self.x + self.width // 2, self.y + self.height // 2), 
                             shield_radius + 2, 1)
    
    def hit(self):
        """El jugador recibe un impacto
        
        Returns:
            bool: True si el jugador murió, False si sobrevivió
        """
        # Si tiene escudo, el escudo absorbe el impacto
        if self.has_shield:
            self.has_shield = False
            self.invulnerable_timer = 60  # 1 segundo de invulnerabilidad
            return False
        
        # Si está en periodo de invulnerabilidad, no recibe daño
        if self.invulnerable_timer > 0:
            return False
        
        self.lives -= 1
        self.invulnerable_timer = 120  # 2 segundos de invulnerabilidad
        return self.lives <= 0
    
    def add_life(self):
        """Agrega una vida extra"""
        self.lives += 1
    
    def activate_shield(self):
        """Activa el escudo"""
        self.has_shield = True
    
    def deactivate_shield(self):
        """Desactiva el escudo"""
        self.has_shield = False