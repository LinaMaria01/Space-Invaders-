"""
Space Invaders con Control por Visión
Proyecto Final - Computación Gráfica 2025-2

Autores: Lina María Calvo Castro - Juan Manuel Diaz Torres
Tecnología: Python + Pygame + MediaPipe + OpenCV
"""

from game import Game

def main():
    """Función principal"""
    print("=" * 50)
    print("SPACE INVADERS - CONTROL POR VISIÓN")
    print("=" * 50)
    print("\nIniciando juego...")
    print("Asegúrate de tener una cámara conectada.")
    print("\nControles:")
    print("- Mueve tu mano para controlar la nave")
    print("- Cierra el puño para disparar")
    print("- También puedes usar flechas y ESPACIO\n")
    
    game = Game()
    game.run()

if __name__ == "__main__":

    main()
