"""
Clase de enemigos (invasores espaciales)
"""
import pygame
import random
from config import *

class Enemy:
    def __init__(self, x, y, enemy_type="common"):
        """Inicializa un enemigo
        
        Args:
            x: posición x
            y: posición y
            enemy_type: "common" o "advanced"
        """
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.type = enemy_type
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.animation_frame = 0
        
        # Propiedades según tipo
        if enemy_type == "advanced":
            self.points = POINTS_ADVANCED_ENEMY
            self.color = PURPLE
            self.can_shoot = True
        else:
            self.points = POINTS_COMMON_ENEMY
            self.color = RED
            self.can_shoot = False
        
    def update_rect(self):
        """Actualiza el rectángulo de colisión"""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Dibuja el enemigo con diseño alienígena"""
        # Color según tipo
        color = self.color
        
        # Cuerpo principal
        pygame.draw.rect(screen, color, 
                        (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
        
        # Ojos
        eye_offset = 2 if self.animation_frame % 20 < 10 else 0
        pygame.draw.circle(screen, WHITE, 
                         (self.x + 12, self.y + 12 + eye_offset), 4)
        pygame.draw.circle(screen, WHITE, 
                         (self.x + self.width - 12, self.y + 12 + eye_offset), 4)
        pygame.draw.circle(screen, BLACK, 
                         (self.x + 12, self.y + 12 + eye_offset), 2)
        pygame.draw.circle(screen, BLACK, 
                         (self.x + self.width - 12, self.y + 12 + eye_offset), 2)
        
        # Antenas
        pygame.draw.line(screen, color, 
                        (self.x + 8, self.y + 5), 
                        (self.x + 8, self.y), 2)
        pygame.draw.line(screen, color, 
                        (self.x + self.width - 8, self.y + 5), 
                        (self.x + self.width - 8, self.y), 2)
        pygame.draw.circle(screen, NEON_PINK, (self.x + 8, self.y), 3)
        pygame.draw.circle(screen, NEON_PINK, (self.x + self.width - 8, self.y), 3)
        
        # Indicador de enemigo avanzado
        if self.type == "advanced":
            pygame.draw.rect(screen, YELLOW, 
                           (self.x + self.width // 2 - 3, self.y + self.height - 8, 6, 4))
        
        self.animation_frame += 1


class Boss:
    def __init__(self, x, y):
        """Inicializa el jefe final"""
        self.x = x
        self.y = y
        self.width = BOSS_WIDTH
        self.height = BOSS_HEIGHT
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.speed = BOSS_SPEED
        self.direction = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.animation_frame = 0
        self.shoot_timer = 0
        self.points = POINTS_BOSS
        
    def update(self):
        """Actualiza la posición del jefe"""
        self.x += self.speed * self.direction
        
        # Cambiar dirección en los bordes
        if self.x <= 50 or self.x >= SCREEN_WIDTH - self.width - 50:
            self.direction *= -1
        
        self.update_rect()
        self.animation_frame += 1
    
    def update_rect(self):
        """Actualiza el rectángulo de colisión"""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def take_damage(self):
        """El jefe recibe daño"""
        self.health -= 1
        return self.health <= 0
    
    def draw(self, screen):
        """Dibuja el jefe final"""
        # Cuerpo principal grande
        pygame.draw.rect(screen, NEON_PINK, 
                        (self.x + 10, self.y + 10, self.width - 20, self.height - 20))
        pygame.draw.rect(screen, PURPLE, 
                        (self.x + 10, self.y + 10, self.width - 20, self.height - 20), 3)
        
        # Ojos grandes
        eye_size = 12
        eye_offset = 3 if self.animation_frame % 30 < 15 else 0
        pygame.draw.circle(screen, WHITE, 
                         (self.x + 40, self.y + 35 + eye_offset), eye_size)
        pygame.draw.circle(screen, WHITE, 
                         (self.x + self.width - 40, self.y + 35 + eye_offset), eye_size)
        pygame.draw.circle(screen, RED, 
                         (self.x + 40, self.y + 35 + eye_offset), eye_size // 2)
        pygame.draw.circle(screen, RED, 
                         (self.x + self.width - 40, self.y + 35 + eye_offset), eye_size // 2)
        
        # Antenas múltiples
        for i in range(3):
            x_pos = self.x + 30 + i * 45
            pygame.draw.line(screen, NEON_GREEN, 
                           (x_pos, self.y + 10), 
                           (x_pos, self.y - 10), 3)
            pygame.draw.circle(screen, YELLOW, (x_pos, self.y - 10), 5)
        
        # Barra de vida
        health_bar_width = self.width - 40
        health_bar_height = 8
        health_bar_x = self.x + 20
        health_bar_y = self.y - 20
        
        # Fondo de la barra
        pygame.draw.rect(screen, GRAY, 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        # Barra de vida actual
        current_health_width = int((self.health / self.max_health) * health_bar_width)
        health_color = GREEN if self.health > self.max_health * 0.5 else (YELLOW if self.health > self.max_health * 0.25 else RED)
        pygame.draw.rect(screen, health_color, 
                        (health_bar_x, health_bar_y, current_health_width, health_bar_height))
        
        # Borde de la barra
        pygame.draw.rect(screen, WHITE, 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 1)


class EnemyGroup:
    def __init__(self, level=1):
        """Inicializa un grupo de enemigos
        
        Args:
            level: nivel actual del juego (1-4)
        """
        self.enemies = []
        self.boss = None
        self.direction = 1  # 1 = derecha, -1 = izquierda
        self.level = level
        self.level_config = LEVEL_CONFIG.get(level, LEVEL_CONFIG[1])
        self.speed = self.level_config["enemy_speed"]
        
        # Crear formación o jefe según el nivel
        if self.level_config.get("boss_fight", False):
            self.create_boss()
        else:
            self.create_formation()
        
    def create_formation(self):
        """Crea la formación de enemigos según el nivel"""
        self.enemies = []
        rows = self.level_config["rows"]
        cols = self.level_config["cols"]
        advanced_chance = self.level_config["advanced_enemy_chance"]
        
        start_x = 100
        start_y = 80
        spacing_x = 60
        spacing_y = 50
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y
                
                # Determinar tipo de enemigo
                enemy_type = "advanced" if random.random() < advanced_chance else "common"
                
                enemy = Enemy(x, y, enemy_type)
                self.enemies.append(enemy)
    
    def create_boss(self):
        """Crea el jefe final"""
        boss_x = SCREEN_WIDTH // 2 - BOSS_WIDTH // 2
        boss_y = 100
        self.boss = Boss(boss_x, boss_y)
    
    def update(self):
        """Actualiza la posición de todos los enemigos o del jefe"""
        if self.boss:
            self.boss.update()
            return
        
        # Verificar si algún enemigo toca el borde
        should_drop = False
        for enemy in self.enemies:
            if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy.width:
                should_drop = True
                break
        
        if should_drop:
            self.direction *= -1
            for enemy in self.enemies:
                enemy.y += ENEMY_DROP_DISTANCE
        
        # Mover todos los enemigos
        for enemy in self.enemies:
            enemy.x += self.speed * self.direction
            enemy.update_rect()
    
    def draw(self, screen):
        """Dibuja todos los enemigos o el jefe"""
        if self.boss:
            self.boss.draw(screen)
        else:
            for enemy in self.enemies:
                enemy.draw(screen)
    
    def get_random_shooter(self):
        """Retorna un enemigo aleatorio para disparar"""
        if self.boss:
            return self.boss
        
        # Filtrar enemigos que pueden disparar
        shooters = [e for e in self.enemies if e.type == "advanced" or random.random() < 0.3]
        if shooters:
            return random.choice(shooters)
        return None
    
    def remove_enemy(self, enemy):
        """Elimina un enemigo"""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            return enemy.points
        return 0
    
    def damage_boss(self):
        """Daña al jefe y retorna True si fue derrotado"""
        if self.boss:
            is_defeated = self.boss.take_damage()
            if is_defeated:
                points = self.boss.points
                self.boss = None
                return True, points
            return False, 0
        return False, 0
    
    def is_empty(self):
        """Verifica si no quedan enemigos"""
        if self.boss:
            return False
        return len(self.enemies) == 0
    
    def reached_bottom(self):
        """Verifica si algún enemigo llegó al fondo"""
        if self.boss:
            return False
        
        for enemy in self.enemies:
            if enemy.y + enemy.height >= SCREEN_HEIGHT - 100:
                return True
        return False