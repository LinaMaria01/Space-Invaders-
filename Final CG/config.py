"""
Configuración y constantes del juego Space Invaders
"""

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (200, 0, 255)
DARK_BLUE = (10, 10, 50)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 16, 240)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Estados del juego
STATE_SPLASH = "splash"
STATE_MENU = "menu"
STATE_OPTIONS = "options"
STATE_INSTRUCTIONS = "instructions"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_LEVEL_TRANSITION = "level_transition"
STATE_GAME_OVER = "game_over"

# Configuración del jugador
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40
PLAYER_SPEED = 8
PLAYER_LIVES = 3

# Configuración de enemigos por nivel
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
ENEMY_ROWS = 4
ENEMY_COLS = 8
ENEMY_DROP_DISTANCE = 30

# Configuración de niveles
LEVEL_CONFIG = {
    1: {
        "name": "Invasión Inicial",
        "difficulty": "Fácil",
        "enemy_speed": 1,
        "enemy_shoot_chance": 0.1,
        "enemy_shoot_interval": 1500,
        "rows": 3,
        "cols": 6,
        "advanced_enemy_chance": 0.0
    },
    2: {
        "name": "Oleada Alienígena",
        "difficulty": "Media",
        "enemy_speed": 1.5,
        "enemy_shoot_chance": 0.2,
        "enemy_shoot_interval": 1200,
        "rows": 4,
        "cols": 7,
        "advanced_enemy_chance": 0.2
    },
    3: {
        "name": "Amenaza Avanzada",
        "difficulty": "Difícil",
        "enemy_speed": 2,
        "enemy_shoot_chance": 0.3,
        "enemy_shoot_interval": 1000,
        "rows": 4,
        "cols": 8,
        "advanced_enemy_chance": 0.3
    },
    4: {
        "name": "Jefe Final",
        "difficulty": "Muy Difícil",
        "enemy_speed": 2.5,
        "enemy_shoot_chance": 0.4,
        "enemy_shoot_interval": 800,
        "rows": 0,
        "cols": 0,
        "advanced_enemy_chance": 0.0,
        "boss_fight": True
    }
}

# Configuración de balas
BULLET_WIDTH = 4
BULLET_HEIGHT = 15
BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5

# Configuración de visión por computadora
HAND_DETECTION_CONFIDENCE = 0.7
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Puntuación
POINTS_COMMON_ENEMY = 10
POINTS_ADVANCED_ENEMY = 20
POINTS_BOSS = 100

# Power-ups
POWERUP_DROP_CHANCE = 0.15  # 15% de probabilidad
POWERUP_FALL_SPEED = 3
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30
POWERUP_DURATION = 10000  # 10 segundos en milisegundos

# Tipos de power-ups
POWERUP_DOUBLE_SHOT = "double_shot"
POWERUP_SHIELD = "shield"
POWERUP_EXTRA_LIFE = "extra_life"

# Jefe final
BOSS_WIDTH = 150
BOSS_HEIGHT = 100
BOSS_HEALTH = 20
BOSS_SPEED = 2

# Audio
AUDIO_ENABLED = True  # Estado inicial del audio

# Configuración de opciones (valores por defecto)
CONTROL_MODE = "vision"  # "vision" o "keyboard"
DIFFICULTY_MULTIPLIER = 1.0  # 0.5 (fácil), 1.0 (normal), 1.5 (difícil)
HAND_SENSITIVITY = 1.0  # 0.5 a 2.0