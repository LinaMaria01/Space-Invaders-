# Space Invaders con Visión por Computadora - TODO

## Archivos a crear:

1. **main.py** - Archivo principal que inicia el juego
2. **game.py** - Lógica principal del juego y estados
3. **player.py** - Clase del jugador (nave)
4. **enemy.py** - Clase de enemigos
5. **bullet.py** - Clase de proyectiles
6. **hand_detector.py** - Detección de manos con MediaPipe
7. **config.py** - Configuración y constantes del juego
8. **requirements.txt** - Dependencias del proyecto
9. **README.md** - Guía de instalación y ejecución

## Estructura del juego:

### Estados:
- SPLASH: Pantalla de inicio
- MENU: Menú principal
- INSTRUCTIONS: Pantalla de instrucciones
- PLAYING: Jugando
- GAME_OVER: Fin del juego

### Características principales:
- Control con manos (MediaPipe + OpenCV)
- Enemigos en formación tipo Space Invaders
- Sistema de puntuación y vidas
- Efectos de sonido
- HUD con información
- Diseño moderno y atractivo

## Implementación:
- Resolución: 800x600 píxeles
- FPS: 60
- Control: Movimiento horizontal con posición de la mano
- Disparo: Gesto de mano cerrada o tecla ESPACIO