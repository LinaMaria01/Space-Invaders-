"""
Sistema de power-ups
"""
import pygame
import random
from config import *

class PowerUp:
    def __init__(self, x, y, powerup_type):
        """Inicializa un power-up
        
        Args:
            x: posición x
            y: posición y
            powerup_type: tipo de power-up (POWERUP_DOUBLE_SHOT, POWERUP_SHIELD, POWERUP_EXTRA_LIFE)
        """
        self.x = x
        self.y = y
        self.width = POWERUP_WIDTH
        self.height = POWERUP_HEIGHT
        self.type = powerup_type
        self.speed = POWERUP_FALL_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.animation_frame = 0
        
        # Configuración según tipo
        if powerup_type == POWERUP_DOUBLE_SHOT:
            self.color = CYAN
            self.symbol = "2X"
        elif powerup_type == POWERUP_SHIELD:
            self.color = BLUE
            self.symbol = "⚡"
        elif powerup_type == POWERUP_EXTRA_LIFE:
            self.color = GREEN
            self.symbol = "♥"
    
    def update(self):
        """Actualiza la posición del power-up"""
        self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        """Verifica si el power-up salió de la pantalla"""
        return self.y > SCREEN_HEIGHT
    
    def draw(self, screen):
        """Dibuja el power-up"""
        # Efecto de rotación
        rotation_offset = (self.animation_frame % 60) / 60.0 * 360
        
        # Fondo con efecto de brillo
        glow_size = 2 + int(abs(pygame.math.Vector2(0, 0).distance_to(
            pygame.math.Vector2(self.animation_frame % 10, 0))))
        
        # Dibujar círculo de brillo
        for i in range(3):
            alpha_color = (*self.color, 100 - i * 30)
            glow_radius = self.width // 2 + glow_size + i * 3
            pygame.draw.circle(screen, self.color, 
                             (int(self.x + self.width // 2), 
                              int(self.y + self.height // 2)), 
                             glow_radius, 2)
        
        # Cuerpo principal
        pygame.draw.rect(screen, self.color, 
                        (self.x + 3, self.y + 3, self.width - 6, self.height - 6))
        pygame.draw.rect(screen, WHITE, 
                        (self.x + 3, self.y + 3, self.width - 6, self.height - 6), 2)
        
        # Símbolo
        font = pygame.font.Font(None, 24)
        text = font.render(self.symbol, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width // 2, 
                                          self.y + self.height // 2))
        screen.blit(text, text_rect)
        
        self.animation_frame += 1


class PowerUpManager:
    def __init__(self):
        """Inicializa el gestor de power-ups"""
        self.powerups = []
        self.active_powerups = {}  # {tipo: tiempo_fin}
    
    def spawn_powerup(self, x, y):
        """Genera un power-up aleatorio en la posición dada"""
        if random.random() < POWERUP_DROP_CHANCE:
            powerup_types = [POWERUP_DOUBLE_SHOT, POWERUP_SHIELD, POWERUP_EXTRA_LIFE]
            powerup_type = random.choice(powerup_types)
            powerup = PowerUp(x, y, powerup_type)
            self.powerups.append(powerup)
    
    def update(self, current_time):
        """Actualiza todos los power-ups"""
        # Actualizar posiciones
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.is_off_screen():
                self.powerups.remove(powerup)
        
        # Actualizar power-ups activos (eliminar los expirados)
        for powerup_type in list(self.active_powerups.keys()):
            if current_time >= self.active_powerups[powerup_type]:
                del self.active_powerups[powerup_type]
    
    def draw(self, screen):
        """Dibuja todos los power-ups"""
        for powerup in self.powerups:
            powerup.draw(screen)
    
    def check_collision(self, player_rect, current_time):
        """Verifica colisiones con el jugador y activa power-ups
        
        Returns:
            tuple: (powerup_type or None, collected_powerup)
        """
        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(player_rect):
                self.powerups.remove(powerup)
                
                # Activar power-up
                if powerup.type == POWERUP_EXTRA_LIFE:
                    # Vida extra no tiene duración, se aplica inmediatamente
                    return powerup.type, powerup
                else:
                    # Power-ups temporales
                    self.active_powerups[powerup.type] = current_time + POWERUP_DURATION
                    return powerup.type, powerup
        
        return None, None
    
    def is_active(self, powerup_type):
        """Verifica si un power-up está activo"""
        return powerup_type in self.active_powerups
    
    def get_remaining_time(self, powerup_type, current_time):
        """Obtiene el tiempo restante de un power-up activo"""
        if powerup_type in self.active_powerups:
            remaining = self.active_powerups[powerup_type] - current_time
            return max(0, remaining // 1000)  # Convertir a segundos
        return 0
    
    def clear(self):
        """Limpia todos los power-ups"""
        self.powerups.clear()
        self.active_powerups.clear()