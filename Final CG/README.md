# Space Invaders con Control por Visión

Juego estilo Space Invaders controlado mediante detección de manos usando visión por computadora.

## 📋 Descripción

Este proyecto es un videojuego 2D desarrollado en Python con Pygame que implementa control mediante visión por computadora utilizando MediaPipe y OpenCV. El jugador controla una nave espacial con sus manos detectadas por la cámara web.

## Características

- **Pantalla de inicio** atractiva con animaciones
- **Menú principal** con opciones: Jugar, Instrucciones y Salir
- **Control por visión**: Mueve tu mano para controlar la nave
- **Sistema de puntuación** y vidas
- **Enemigos** en formación tipo Space Invaders
- **Efectos de sonido** realistas para disparos, explosiones e impactos
- **Música de fondo constante** durante todo el juego
- **Opción de silenciar** todo el audio con un clic o tecla M
- **Interfaz moderna** con diseño neón y espacial
- **Retorno automático** al menú después de terminar

## Requisitos

- Python 3.8 o superior
- Cámara web funcional
- Sistema operativo: Windows, macOS o Linux

## Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install pygame opencv-python mediapipe numpy scipy
```

## Ejecución

Para ejecutar el juego, simplemente corre:

```bash
python main.py
```

**Nota**: La primera vez que ejecutes el juego, tomará unos segundos generar los efectos de sonido y música. Verás mensajes en la consola indicando el progreso.

## Controles

### Control por Visión (Principal)
- **Mover nave**: Mueve tu mano izquierda/derecha frente a la cámara
- **Disparar**: Cierra el puño

### Control por Teclado (Alternativo)
- **Flechas ←/→**: Mover nave
- **ESPACIO**: Disparar
- **M**: Silenciar/activar audio
- **Cualquier tecla**: Avanzar desde pantalla de inicio

### Control de Audio
- **Botón en pantalla** (esquina superior derecha): Clic para silenciar/activar
- **Tecla M**: Silenciar/activar audio en cualquier momento

## Reglas del Juego

1. **Objetivo**: Destruye todos los invasores alienígenas antes de que lleguen al fondo
2. **Puntuación**: Cada enemigo destruido otorga 10 puntos
3. **Vidas**: Comienzas con 3 vidas
4. **Fin del juego**: 
   - Pierdes todas tus vidas
   - Los enemigos llegan al fondo
   - Destruyes todos los enemigos (¡Victoria!)

## Sistema de Audio

El juego incluye un sistema completo de audio con:

### Música de Fondo
- **Música constante**: Se reproduce durante todo el juego (menú, instrucciones y jugando)
- **16 segundos de duración** con variaciones melódicas antes de repetirse
- **Múltiples capas**: Bajo rítmico, melodía espacial y pad atmosférico
- **Volumen balanceado**: 25% para no ser intrusiva

### Efectos de Sonido
- **Disparo láser**: Sonido futurista cuando disparas
- **Explosión**: Efecto al destruir enemigos
- **Impacto**: Sonido cuando recibes daño
- **Victoria**: Melodía ascendente al ganar
- **Game Over**: Melodía descendente al perder

### Control de Audio
- **Botón visual**: En la esquina superior derecha muestra 🔊 ON o 🔇 OFF
- **Tecla M**: Alterna entre sonido activado/silenciado
- **Persistente**: El estado del audio se mantiene durante toda la sesión

Todos los sonidos son generados programáticamente usando síntesis de audio, por lo que no se requieren archivos externos.

## Estructura del Proyecto

```
/workspace/
├── main.py              # Archivo principal de ejecución
├── game.py              # Lógica principal del juego
├── config.py            # Configuración y constantes
├── player.py            # Clase del jugador
├── enemy.py             # Clases de enemigos
├── bullet.py            # Clase de proyectiles
├── hand_detector.py     # Detección de manos con MediaPipe
├── sound_generator.py   # Generador de efectos de sonido y música
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## Configuración

Puedes modificar parámetros del juego en `config.py`:
- Resolución de pantalla
- Velocidad del jugador y enemigos
- Número de vidas
- Puntos por enemigo
- Sensibilidad de detección de manos
- Estado inicial del audio (AUDIO_ENABLED)

Para ajustar el volumen de los sonidos, puedes modificar los valores en `game.py` en el método `create_sounds()`:
- Música de fondo: `self.background_music.set_volume(0.25)` (línea ~68)
- Efectos de sonido: Entre 0.4 y 0.6

## Requerimientos Cumplidos

### Funcionales
- RF-01 a RF-16: Todos los requerimientos funcionales implementados

### No Funcionales
- RNF-01: Desarrollado en Python 3.x con Pygame
- RNF-02: Visión implementada con MediaPipe y OpenCV
- RNF-03: Procesamiento de cámara no bloquea el loop principal
- RNF-04: Menú legible y claro
- RNF-05: Instrucciones explican controles
- RNF-06: Código modular y comentado

### De Interfaz
- RI-01 a RI-06: Todos implementados

### De Contenido
- RC-01: Efectos de sonido en acciones (disparo, explosión, impacto)
- RC-02: Sonido para colisiones y eventos
- RC-03: Sprites para jugador, enemigos y fondo
- RC-04: Recursos generados programáticamente (uso libre)

## Solución de Problemas

### La cámara no funciona
- Verifica que tu cámara esté conectada y funcionando
- Asegúrate de que ninguna otra aplicación esté usando la cámara
- En algunos sistemas, puede necesitar permisos de cámara

### El juego va lento
- Cierra otras aplicaciones que usen la cámara
- Reduce la resolución de la cámara en `config.py`
- Verifica que tu sistema cumpla con los requisitos mínimos

### Error de importación de módulos
- Asegúrate de haber instalado todas las dependencias (incluyendo scipy)
- Verifica que estás usando Python 3.8 o superior

### No se escucha el sonido
- Verifica que tu sistema de audio esté funcionando
- Asegúrate de que pygame.mixer esté correctamente inicializado
- Revisa el volumen del sistema y del juego
- Verifica que el botón de audio en el juego esté en ON (🔊)

### La música es muy repetitiva
- La música tiene 16 segundos de duración con 4 patrones diferentes
- Puedes modificar la duración en `sound_generator.py` línea 117
- O puedes silenciar la música con la tecla M y jugar solo con efectos

### La generación de sonidos tarda mucho
- Es normal que la primera vez tarde unos segundos (10-15 segundos)
- Los sonidos se generan una sola vez al inicio del juego
- Si tarda más de 30 segundos, puede haber un problema con scipy

## Desarrollo

Este proyecto fue desarrollado como proyecto final para el curso de Computación Gráfica 2025-2, cumpliendo con todos los requerimientos especificados en el documento de requerimientos.

### Tecnologías Utilizadas
- **Pygame**: Framework de desarrollo de juegos
- **MediaPipe**: Detección de manos en tiempo real
- **OpenCV**: Procesamiento de video
- **NumPy**: Operaciones numéricas
- **SciPy**: Síntesis y procesamiento de audio

## Licencia

Este proyecto es de uso educativo.

## Agradecimientos

- Pygame por el framework de desarrollo de juegos
- MediaPipe por la detección de manos
- OpenCV por el procesamiento de video
- SciPy por las herramientas de procesamiento de señales


