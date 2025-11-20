"""
Detector de manos usando MediaPipe y OpenCV
"""
import cv2
import mediapipe as mp
from config import HAND_DETECTION_CONFIDENCE, CAMERA_WIDTH, CAMERA_HEIGHT

class HandDetector:
    def __init__(self):
        """Inicializa el detector de manos"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Inicializar cámara
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        
        self.hand_x = 0.5  # Posición normalizada (0-1)
        self.is_closed = False  # Mano cerrada para disparar
        
    def update(self):
        """Actualiza la detección de manos"""
        success, frame = self.cap.read()
        if not success:
            return None
            
        # Voltear horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Convertir a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar frame
        results = self.hands.process(rgb_frame)
        
        # Dibujar landmarks si se detecta mano
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Obtener posición de la muñeca (landmark 0)
                wrist = hand_landmarks.landmark[0]
                self.hand_x = wrist.x
                
                # Detectar si la mano está cerrada (puño)
                # Comparar distancia entre punta del dedo índice y palma
                index_tip = hand_landmarks.landmark[8]
                palm = hand_landmarks.landmark[0]
                
                distance = ((index_tip.x - palm.x)**2 + (index_tip.y - palm.y)**2)**0.5
                self.is_closed = distance < 0.15
        
        return frame
    
    def get_position(self):
        """Retorna la posición normalizada de la mano (0-1)"""
        return self.hand_x
    
    def is_hand_closed(self):
        """Retorna True si la mano está cerrada (para disparar)"""
        return self.is_closed
    
    def release(self):
        """Libera recursos de la cámara"""
        self.cap.release()
        cv2.destroyAllWindows()