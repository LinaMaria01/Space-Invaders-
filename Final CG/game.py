"""
game.py - Lógica principal del juego Space Invaders (reescritura total)

"""
import pygame
import random
import sys
import traceback
from config import *

# Importar módulos del proyecto (algunos pueden no existir; se controlan con try/except)
try:
    from player import Player
except Exception:
    Player = None

try:
    from enemy import EnemyGroup
except Exception:
    EnemyGroup = None

try:
    from bullet import Bullet
except Exception:
    Bullet = None

try:
    from powerup import PowerUpManager
except Exception:
    PowerUpManager = None

try:
    from hand_detector import HandDetector
except Exception:
    HandDetector = None

try:
    from sound_generator import SoundGenerator
except Exception:
    SoundGenerator = None


class Game:
    LEVEL_TRANSITION_MS = 1800  # Duración de la transición entre niveles

    def __init__(self):
        pygame.init()
        # Mixer puede fallar en algunos entornos; envolver en try
        try:
            pygame.mixer.init()
        except Exception:
            print("Advertencia: pygame.mixer no pudo inicializarse (audio deshabilitado).")

        # Ventana y reloj
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders - Control por Visión")
        self.clock = pygame.time.Clock()

        # Estados del juego
        self.state = STATE_SPLASH
        self.running = True
        self.paused = False
        self.audio_enabled = AUDIO_ENABLED

        # Fuentes
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.hud_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)

        # Detector de manos (opcional)
        if HandDetector:
            try:
                self.hand_detector = HandDetector()
            except Exception:
                print("hand_detector.py cargado pero produjo error al inicializar. Usando control por teclado.")
                self.hand_detector = None
        else:
            self.hand_detector = None
            print("hand_detector.py no encontrado: control por teclado habilitado.")

        # Sonidos (opcional)
        if SoundGenerator:
            try:
                self.sound_generator = SoundGenerator()
            except Exception:
                print("sound_generator.py presente pero error al inicializar; sonidos deshabilitados.")
                self.sound_generator = None
        else:
            self.sound_generator = None

        # Inicializar sonidos (pueden ser None)
        self._create_sounds()

        # Manager de power-ups
        self.powerup_manager = PowerUpManager() if PowerUpManager else None
        if not self.powerup_manager:
            print("powerup.py no encontrado: power-ups deshabilitados.")

        # Variables del juego (se inicializan con init_game)
        self.player = None
        self.enemies = None
        self.player_bullets = []
        self.enemy_bullets = []
        self.score = 0
        self.current_level = 1
        self.level_transition_start = None
        self.game_over_timer = None
        self.last_shot_time = 0
        self.last_enemy_shot_time = 0
        self.prev_hand_closed = False

        # Música de fondo (puede ser None)
        self.background_music = None
        self.music_playing = False

        # Start music if possible
        self.start_background_music()

    # -----------------------
    # Sonidos / audio
    # -----------------------
    def _create_sounds(self):
        """Crea o carga sonidos usando SoundGenerator si está disponible."""
        self.shoot_sound = None
        self.explosion_sound = None
        self.hit_sound = None
        self.victory_sound = None
        self.game_over_sound = None
        self.background_music = None

        if not self.sound_generator:
            return

        try:
            self.shoot_sound = self.sound_generator.generate_shoot_sound()
            self.explosion_sound = self.sound_generator.generate_explosion_sound()
            self.hit_sound = self.sound_generator.generate_hit_sound()
            self.victory_sound = self.sound_generator.generate_victory_sound()
            self.game_over_sound = self.sound_generator.generate_game_over_sound()
            self.background_music = self.sound_generator.generate_background_music()
            if self.background_music:
                try:
                    self.background_music.set_volume(0.25)
                except Exception:
                    pass
        except Exception as e:
            print("Error al crear sonidos:", e)
            traceback.print_exc()

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        if not self.audio_enabled:
            try:
                pygame.mixer.stop()
            except Exception:
                pass
            self.music_playing = False
        else:
            self.start_background_music()

    def start_background_music(self):
        if self.audio_enabled and self.background_music and not self.music_playing:
            try:
                self.background_music.play(loops=-1)
                self.music_playing = True
            except Exception:
                pass

    def play_sound(self, sound):
        if self.audio_enabled and sound:
            try:
                sound.play()
            except Exception:
                pass

    # -----------------------
    # Inicialización y niveles
    # -----------------------
    def init_game(self, level=1, reset_score=False):
        """Inicia o reinicia la partida en el nivel indicado."""
        # Mantener score si no se quiere reiniciar
        if reset_score:
            self.score = 0

        # Crear jugador
        if Player:
            self.player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2,
                                 SCREEN_HEIGHT - 80)
            # atributo runtime para doble disparo (se puede crear dinámicamente)
            self.player.double_shot_until = 0
        else:
            self.player = None
            print("player.py no disponible: el juego no funcionará correctamente.")

        # Crear enemigos con configuración del nivel
        if EnemyGroup:
            # EnemyGroup acepta parámetro level en su constructor en tu enemy.py
            try:
                self.enemies = EnemyGroup(level=level)
            except TypeError:
                # si el constructor tenia otra firma, intentar sin argumentos
                self.enemies = EnemyGroup()
        else:
            self.enemies = None
            print("enemy.py no encontrado: no habrá enemigos.")

        # Reset balas y power-ups
        self.player_bullets = []
        self.enemy_bullets = []
        if self.powerup_manager:
            try:
                self.powerup_manager.clear()
            except Exception:
                pass

        self.current_level = level
        self.level_transition_start = None
        self.game_over_timer = None
        self.last_shot_time = 0
        self.last_enemy_shot_time = 0
        self.prev_hand_closed = False

    # -----------------------
    # Eventos
    # -----------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Navegar entre estados
            if self.state == STATE_SPLASH:
                if event.type == pygame.KEYDOWN:
                    self.state = STATE_MENU
                    self.start_background_music()

            elif self.state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_menu_click(event.pos)

            elif self.state == STATE_INSTRUCTIONS:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = STATE_MENU

            elif self.state == STATE_PLAYING:
                # Pausa
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_SPACE:
                        # disparo por teclado
                        self._player_shoot_by_input()
                    elif event.key == pygame.K_m:
                        self.toggle_audio()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # permitir click para disparar si se desea
                    if event.button == 1:  # botón izquierdo
                        self._player_shoot_by_input()

    def handle_menu_click(self, pos):
        x, y = pos
        # Jugar
        if 250 <= x <= 550 and 200 <= y <= 260:
            # iniciar nivel 1
            self.init_game(level=1, reset_score=True)
            # pasar a transición para que el jugador vea mensaje
            self.state = STATE_LEVEL_TRANSITION
            self.level_transition_start = pygame.time.get_ticks()
        # Instrucciones
        elif 250 <= x <= 550 and 290 <= y <= 350:
            self.state = STATE_INSTRUCTIONS
        # Salir
        elif 250 <= x <= 550 and 380 <= y <= 440:
            self.running = False
        # Mute/Unmute
        elif SCREEN_WIDTH - 120 <= x <= SCREEN_WIDTH - 20 and 20 <= y <= 70:
            self.toggle_audio()

    # -----------------------
    # Lógica principal por estado
    # -----------------------
    def update_splash(self):
        self.splash_timer = getattr(self, "splash_timer", 0) + 1
        if self.splash_timer > FPS * 3:  # 3 segundos
            self.state = STATE_MENU
            self.start_background_music()

    def update_level_transition(self):
        """Gestiona la pantalla de transición entre niveles."""
        if not self.level_transition_start:
            self.level_transition_start = pygame.time.get_ticks()
        now = pygame.time.get_ticks()
        if now - self.level_transition_start > self.LEVEL_TRANSITION_MS:
            # Iniciar el nivel (current_level ya fue incrementado por update_playing cuando terminó anterior)
            # Si se empieza desde menú, current_level debería estar en 1
            self.init_game(level=self.current_level, reset_score=False)
            self.state = STATE_PLAYING

    def update_playing(self):
        """Lógica principal del juego cuando se está jugando."""
        if self.paused:
            return  # no actualizar nada si está en pausa

        now = pygame.time.get_ticks()

        # Asegurar música
        self.start_background_music()

        # Actualizar estado del jugador (timers internos si aplica)
        if self.player:
            try:
                self.player.update(now)
            except Exception:
                # player.update puede no existir; ignorar si falla
                pass

        # Detección de manos (si existe)
        hand_x = 0.5
        hand_closed = False
        if self.hand_detector:
            try:
                frame = self.hand_detector.update()
                hand_x = self.hand_detector.get_position()
                hand_closed = self.hand_detector.is_hand_closed()
            except Exception:
                hand_x = 0.5
                hand_closed = False

        # Control del jugador
        if self.player:
            if CONTROL_MODE == "vision" and self.hand_detector:
                try:
                    self.player.set_position_normalized(hand_x)
                except Exception:
                    pass
            else:
                # control por teclado
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.move_left()
                if keys[pygame.K_RIGHT]:
                    self.player.move_right()

        # Disparo por gesto (mano cerrada) - gestionar debounce
        if hand_closed and not self.prev_hand_closed:
            if now - self.last_shot_time > 300:
                self._player_shoot_by_input()
                self.last_shot_time = now
        self.prev_hand_closed = hand_closed

        # Actualizar enemigos
        if self.enemies:
            try:
                self.enemies.update()
            except Exception:
                pass

        # Enemigos disparan según configuración de nivel
        lvl_cfg = LEVEL_CONFIG.get(self.current_level, LEVEL_CONFIG[1])
        enemy_shoot_interval = lvl_cfg.get("enemy_shoot_interval", 1200)
        enemy_shoot_chance = lvl_cfg.get("enemy_shoot_chance", 0.2)
        if now - self.last_enemy_shot_time > enemy_shoot_interval:
            self.last_enemy_shot_time = now
            if self.enemies:
                try:
                    shooter = self.enemies.get_random_shooter()
                except Exception:
                    shooter = None
                if shooter and random.random() < enemy_shoot_chance:
                    # Shooter puede ser Boss o Enemy
                    sx = shooter.x + getattr(shooter, "width", BULLET_WIDTH) // 2
                    sy = shooter.y + getattr(shooter, "height", BULLET_HEIGHT)
                    # Crear bala enemiga (direccion -1 hacia abajo en tu Bullet)
                    if Bullet:
                        try:
                            b = Bullet(sx, sy, -1)
                            self.enemy_bullets.append(b)
                        except Exception:
                            # fallback sencillo
                            pass

        # Actualizar balas del jugador
        for bullet in self.player_bullets[:]:
            try:
                bullet.update()
            except Exception:
                # fallback: mover hacia arriba
                bullet.y -= BULLET_SPEED
                bullet.rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)

            if bullet.is_off_screen():
                if bullet in self.player_bullets:
                    self.player_bullets.remove(bullet)
                continue

            # Colisión con enemigos o jefe
            if self.enemies:
                # Si hay un boss
                if getattr(self.enemies, "boss", None):
                    boss = self.enemies.boss
                    if bullet.rect.colliderect(boss.rect):
                        # daño al boss
                        try:
                            defeated, pts = self.enemies.damage_boss()
                        except Exception:
                            defeated, pts = (boss.take_damage(), getattr(boss, "points", POINTS_BOSS))
                            if defeated:
                                # eliminar boss
                                try:
                                    self.enemies.boss = None
                                except Exception:
                                    pass
                        # sumar puntos si se devolvieron
                        try:
                            self.score += pts
                        except Exception:
                            self.score += POINTS_BOSS
                        if bullet in self.player_bullets:
                            self.player_bullets.remove(bullet)
                        self.play_sound(self.explosion_sound)
                        # posible drop
                        if self.powerup_manager and random.random() < POWERUP_DROP_CHANCE:
                            try:
                                self.powerup_manager.spawn_powerup(bullet.x, bullet.y)
                            except Exception:
                                pass
                        # si boss derrotado, desencadenar transición/fin
                        if defeated:
                            # si quedan más niveles
                            if self.current_level < max(LEVEL_CONFIG.keys()):
                                self.current_level += 1
                                self.state = STATE_LEVEL_TRANSITION
                                self.level_transition_start = pygame.time.get_ticks()
                            else:
                                self.state = STATE_GAME_OVER
                                self.game_over_timer = pygame.time.get_ticks()
                                self.play_sound(self.victory_sound)
                        continue  # seguir con siguientes balas

                # Colisión con enemigos normales
                for enemy in list(getattr(self.enemies, "enemies", [])):
                    try:
                        if bullet.rect.colliderect(enemy.rect):
                            # Remover bala y enemigo, sumar puntos según enemy.remove_enemy
                            if bullet in self.player_bullets:
                                self.player_bullets.remove(bullet)
                            try:
                                pts = self.enemies.remove_enemy(enemy)
                                # enemy.remove_enemy en tu enemy.py devuelve puntos (enemy.points)
                                self.score += pts if pts else 0
                            except Exception:
                                # fallback: quitar de la lista directamente
                                try:
                                    self.enemies.enemies.remove(enemy)
                                except Exception:
                                    pass
                                # añadir puntos según tipo
                                etype = getattr(enemy, "type", "common")
                                if etype == "advanced":
                                    self.score += POINTS_ADVANCED_ENEMY
                                else:
                                    self.score += POINTS_COMMON_ENEMY
                            self.play_sound(self.explosion_sound)
                            # spawn powerup
                            if self.powerup_manager and random.random() < POWERUP_DROP_CHANCE:
                                try:
                                    self.powerup_manager.spawn_powerup(enemy.x, enemy.y)
                                except Exception:
                                    pass
                            break
                    except Exception:
                        continue

        # Actualizar balas enemigas
        for bullet in self.enemy_bullets[:]:
            try:
                bullet.update()
            except Exception:
                bullet.y += ENEMY_BULLET_SPEED
                bullet.rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)

            if bullet.is_off_screen():
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                continue

            # Colisión con el jugador
            if self.player and bullet.rect.colliderect(self.player.rect):
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                died = self.player.hit()
                self.play_sound(self.hit_sound)
                if died:
                    self.state = STATE_GAME_OVER
                    self.game_over_timer = pygame.time.get_ticks()
                    self.play_sound(self.game_over_sound)

        # Actualizar power-ups: caída y colisiones
        if self.powerup_manager:
            try:
                self.powerup_manager.update(now)
                powerup_type, collected = self.powerup_manager.check_collision(self.player.rect if self.player else pygame.Rect(0,0,0,0), now)
                if powerup_type:
                    # aplicar efecto
                    if powerup_type == POWERUP_EXTRA_LIFE:
                        if self.player:
                            self.player.add_life()
                    elif powerup_type == POWERUP_SHIELD:
                        if self.player:
                            self.player.activate_shield()
                    elif powerup_type == POWERUP_DOUBLE_SHOT:
                        if self.player:
                            self.player.double_shot_until = now + POWERUP_DURATION
                    # reproducir sonido de recogida
                    self.play_sound(self.explosion_sound)
            except Exception:
                pass

        # Verificar condiciones de fin de nivel o derrota
        if self.enemies:
            try:
                if self.enemies.reached_bottom():
                    # derrota inmediata
                    self.state = STATE_GAME_OVER
                    self.game_over_timer = pygame.time.get_ticks()
                    self.play_sound(self.game_over_sound)
                elif self.enemies.is_empty():
                    # nivel completado
                    if self.current_level < max(LEVEL_CONFIG.keys()):
                        self.current_level += 1
                        self.state = STATE_LEVEL_TRANSITION
                        self.level_transition_start = pygame.time.get_ticks()
                        self.play_sound(self.victory_sound)
                    else:
                        # completó todos los niveles
                        self.state = STATE_GAME_OVER
                        self.game_over_timer = pygame.time.get_ticks()
                        self.play_sound(self.victory_sound)
            except Exception:
                pass

    # -----------------------
    # Disparo del jugador (gestionando doble disparo)
    # -----------------------
    def _player_shoot_by_input(self):
        """Crea balas según estado (doble disparo si está activo)"""
        if not self.player or not Bullet:
            return

        now = pygame.time.get_ticks()
        # cooldown simple
        if now - self.last_shot_time < 150:
            return
        self.last_shot_time = now

        double_active = getattr(self.player, "double_shot_until", 0) > now
        if double_active:
            # dos balas con ligero offset
            left_x = self.player.x + 8
            right_x = self.player.x + self.player.width - 8
            try:
                b1 = Bullet(left_x, self.player.y, 1)
                b2 = Bullet(right_x, self.player.y, 1)
                self.player_bullets.append(b1)
                self.player_bullets.append(b2)
            except Exception:
                # fallback: un único disparo
                b = Bullet(self.player.x + self.player.width // 2, self.player.y, 1)
                self.player_bullets.append(b)
        else:
            b = Bullet(self.player.x + self.player.width // 2, self.player.y, 1)
            self.player_bullets.append(b)

        self.play_sound(self.shoot_sound)

    # -----------------------
    # Dibujado por estado
    # -----------------------
    def draw_audio_button(self):
        button_rect = pygame.Rect(SCREEN_WIDTH - 120, 20, 100, 50)
        if self.audio_enabled:
            color = NEON_GREEN
            text = "🔊 ON"
        else:
            color = RED
            text = "🔇 OFF"
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 3)
        else:
            pygame.draw.rect(self.screen, color, button_rect, 2)
        text_surface = self.small_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_splash(self):
        self.screen.fill(DARK_BLUE)
        self.splash_timer = getattr(self, "splash_timer", 0)
        # simple starfield
        for i in range(40):
            x = (i * 137) % SCREEN_WIDTH
            y = (i * 219 + (self.splash_timer * 3)) % SCREEN_HEIGHT
            pygame.draw.circle(self.screen, WHITE, (x, y), (i % 3) + 1)
        title = self.title_font.render("SPACE INVADERS", True, NEON_GREEN)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 160)))
        sub = self.menu_font.render("Control por Visión", True, YELLOW)
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 240)))
        if (self.splash_timer // 30) % 2 == 0:
            press = self.small_font.render("Presiona cualquier tecla", True, WHITE)
            self.screen.blit(press, press.get_rect(center=(SCREEN_WIDTH // 2, 420)))
        self.splash_timer += 1

    def draw_menu(self):
        self.screen.fill(DARK_BLUE)
        title_surface = self.title_font.render("SPACE INVADERS", True, NEON_GREEN)
        self.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100)))
        # botones
        mouse_pos = pygame.mouse.get_pos()
        buttons = [("JUGAR", 230), ("INSTRUCCIONES", 320), ("SALIR", 410)]
        for text, y in buttons:
            rect = pygame.Rect(250, y, 300, 60)
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, NEON_PINK, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 3)
            else:
                pygame.draw.rect(self.screen, BLUE, rect)
                pygame.draw.rect(self.screen, CYAN, rect, 2)
            surf = self.menu_font.render(text, True, WHITE)
            self.screen.blit(surf, surf.get_rect(center=rect.center))
        # audio button and hint
        self.draw_audio_button()
        hint = self.small_font.render("Presiona M o clic arriba para silenciar", True, GRAY)
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 560)))

    def draw_instructions(self):
        self.screen.fill(DARK_BLUE)
        title = self.menu_font.render("INSTRUCCIONES", True, NEON_GREEN)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))
        lines = [
            "OBJETIVO:",
            "Destruye todos los invasores antes de que lleguen al fondo",
            "",
            "CONTROLES:",
            "- Mueve tu mano para mover la nave (modo visión)",
            "- Cierra el puño para disparar",
            "- También puedes usar las FLECHAS y ESPACIO",
            "- Presiona P para pausar",
            "- Presiona M para silenciar",
            "",
            "PUNTUACIÓN:",
            f"- Enemigo común: {POINTS_COMMON_ENEMY} pts",
            f"- Enemigo avanzado: {POINTS_ADVANCED_ENEMY} pts",
            f"- Jefe: {POINTS_BOSS} pts",
            f"- Vidas iniciales: {PLAYER_LIVES}"
        ]
        y = 120
        for line in lines:
            color = WHITE
            if line.endswith(":"):
                color = YELLOW
            surf = self.small_font.render(line, True, color)
            self.screen.blit(surf, (50, y))
            y += 28
        self.draw_audio_button()

    def draw_playing(self):
        # fondo y estrellas
        self.screen.fill(DARK_BLUE)
        frame = pygame.time.get_ticks() // 50
        for i in range(80):
            x = (i * 137) % SCREEN_WIDTH
            y = ((i * 219) + frame) % SCREEN_HEIGHT
            pygame.draw.circle(self.screen, WHITE, (x, y), (i % 3) + 1)

        # dibujar player
        if self.player:
            self.player.draw(self.screen)

        # dibujar enemigos
        if self.enemies:
            self.enemies.draw(self.screen)

        # dibujar balas
        for b in self.player_bullets:
            try:
                b.draw(self.screen)
            except Exception:
                pass
        for b in self.enemy_bullets:
            try:
                b.draw(self.screen)
            except Exception:
                pass

        # dibujar power-ups (caídos)
        if self.powerup_manager:
            try:
                self.powerup_manager.draw(self.screen)
            except Exception:
                pass

        # HUD: score y vidas
        score_surface = self.hud_font.render(f"PUNTOS: {self.score}", True, YELLOW)
        self.screen.blit(score_surface, (10, 10))
        lives = self.player.lives if self.player else 0
        lives_surface = self.hud_font.render(f"VIDAS: {lives}", True, RED)
        self.screen.blit(lives_surface, (10, 45))

        # power-ups activos en HUD
        if self.powerup_manager:
            x = 10
            now = pygame.time.get_ticks()
            for ptype in list(self.powerup_manager.active_powerups.keys()):
                remaining = self.powerup_manager.get_remaining_time(ptype, now)
                text = f"{ptype}: {remaining}s"
                surf = self.small_font.render(text, True, CYAN)
                self.screen.blit(surf, (x, SCREEN_HEIGHT - 30))
                x += 180

        # hand detector indicator
        hand_status = "MANO DETECTADA" if self.hand_detector and getattr(self.hand_detector, "hand_x", 0.5) != 0.5 else "SIN MANO"
        hand_color = NEON_GREEN if self.hand_detector and getattr(self.hand_detector, "hand_x", 0.5) != 0.5 else RED
        hand_surface = self.small_font.render(hand_status, True, hand_color)
        self.screen.blit(hand_surface, (SCREEN_WIDTH - 240, 10))

        # audio indicator
        audio_surface = self.small_font.render("🔊" if self.audio_enabled else "🔇", True, WHITE)
        self.screen.blit(audio_surface, (SCREEN_WIDTH - 240, 40))

        # pausa overlay
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            paused_surf = self.title_font.render("PAUSA", True, NEON_PINK)
            self.screen.blit(paused_surf, paused_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    def draw_level_transition(self):
        self.screen.fill(DARK_BLUE)
        text = f"Nivel {self.current_level} - {LEVEL_CONFIG.get(self.current_level, {}).get('name', '')}"
        surf = self.menu_font.render(text, True, CYAN)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        instr = self.small_font.render("Preparando la siguiente oleada...", True, WHITE)
        self.screen.blit(instr, instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))

    def draw_game_over(self):
        self.screen.fill(DARK_BLUE)
        # mensaje de victoria o derrota
        won = False
        try:
            if self.enemies and self.enemies.is_empty():
                won = True
        except Exception:
            won = False
        if won:
            msg = "¡VICTORIA!"
            color = NEON_GREEN
        else:
            msg = "GAME OVER"
            color = RED
        title = self.title_font.render(msg, True, color)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 160)))
        score_s = self.menu_font.render(f"Puntuación: {self.score}", True, YELLOW)
        self.screen.blit(score_s, score_s.get_rect(center=(SCREEN_WIDTH // 2, 260)))
        sub = self.small_font.render("Volviendo al menú principal...", True, WHITE)
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 340)))

    # -----------------------
    # Loop principal
    # -----------------------
    def run(self):
        # Inicializar timers
        self.splash_timer = 0

        while self.running:
            self.handle_events()

            # Actualizar según estado
            if self.state == STATE_SPLASH:
                self.update_splash()
            elif self.state == STATE_MENU:
                # asegurar música
                self.start_background_music()
            elif self.state == STATE_LEVEL_TRANSITION:
                self.update_level_transition()
            elif self.state == STATE_PLAYING:
                self.update_playing()
            elif self.state == STATE_GAME_OVER:
                # Después de mostrar game over por N segundos, volver al menú
                if not self.game_over_timer:
                    self.game_over_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.game_over_timer > 3000:
                    self.state = STATE_MENU

            # Dibujar según estado
            if self.state == STATE_SPLASH:
                self.draw_splash()
            elif self.state == STATE_MENU:
                self.draw_menu()
            elif self.state == STATE_INSTRUCTIONS:
                self.draw_instructions()
            elif self.state == STATE_LEVEL_TRANSITION:
                self.draw_level_transition()
            elif self.state == STATE_PLAYING:
                self.draw_playing()
            elif self.state == STATE_GAME_OVER:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

        # Salida limpia
        if self.hand_detector:
            try:
                self.hand_detector.release()
            except Exception:
                pass
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    g = Game()
    g.run()
