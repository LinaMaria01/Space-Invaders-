"""
Generador de efectos de sonido para el juego
"""
import numpy as np
import pygame
from scipy import signal

class SoundGenerator:
    def __init__(self, sample_rate=22050):
        """Inicializa el generador de sonidos"""
        self.sample_rate = sample_rate
        
    def generate_shoot_sound(self):
        """Genera sonido de disparo láser"""
        duration = 0.15
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Frecuencia descendente para efecto láser
        freq_start = 800
        freq_end = 200
        frequency = np.linspace(freq_start, freq_end, len(t))
        
        # Generar onda
        phase = np.cumsum(2 * np.pi * frequency / self.sample_rate)
        wave = np.sin(phase)
        
        # Envelope de ataque y decay rápido
        envelope = np.exp(-t * 15)
        wave = wave * envelope
        
        # Normalizar y convertir a 16-bit
        wave = np.int16(wave * 32767 * 0.3)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_explosion_sound(self):
        """Genera sonido de explosión"""
        duration = 0.3
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Ruido blanco para explosión
        noise = np.random.uniform(-1, 1, len(t))
        
        # Filtro paso bajo para hacer el sonido más grave
        b, a = signal.butter(4, 0.1)
        filtered_noise = signal.filtfilt(b, a, noise)
        
        # Envelope exponencial
        envelope = np.exp(-t * 8)
        wave = filtered_noise * envelope
        
        # Agregar componente de baja frecuencia
        low_freq = np.sin(2 * np.pi * 60 * t) * envelope
        wave = wave * 0.7 + low_freq * 0.3
        
        # Normalizar
        wave = np.int16(wave * 32767 * 0.5)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_hit_sound(self):
        """Genera sonido de impacto al jugador"""
        duration = 0.25
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Onda cuadrada para sonido más duro
        freq = 150
        square_wave = signal.square(2 * np.pi * freq * t)
        
        # Envelope
        envelope = np.exp(-t * 10)
        wave = square_wave * envelope
        
        # Agregar ruido
        noise = np.random.uniform(-0.2, 0.2, len(t))
        wave = wave * 0.8 + noise * 0.2
        
        # Normalizar
        wave = np.int16(wave * 32767 * 0.6)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_background_music(self):
        """Genera música de fondo constante y envolvente"""
        duration = 16.0  # 16 segundos para mayor variedad antes de repetir
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Bajo rítmico constante (patrón de 4/4)
        bass_freq = 110  # A2
        bass = np.sin(2 * np.pi * bass_freq * t)
        
        # Patrón rítmico del bajo
        bass_rhythm = np.zeros(len(t))
        beat_duration = 0.5  # Cada beat dura 0.5 segundos
        for i in range(int(duration / beat_duration)):
            start_idx = int(i * beat_duration * self.sample_rate)
            end_idx = int((i * beat_duration + 0.3) * self.sample_rate)
            if end_idx < len(bass_rhythm):
                bass_rhythm[start_idx:end_idx] = 1
        
        bass = bass * bass_rhythm * 0.25
        
        # Melodía espacial con arpegios
        melody_notes = [
            # Primer patrón (4 segundos)
            (440, 0, 0.5), (494, 0.5, 1.0), (523, 1.0, 1.5), (587, 1.5, 2.0),
            (523, 2.0, 2.5), (494, 2.5, 3.0), (440, 3.0, 3.5), (392, 3.5, 4.0),
            # Segundo patrón (4 segundos)
            (523, 4.0, 4.5), (587, 4.5, 5.0), (659, 5.0, 5.5), (698, 5.5, 6.0),
            (659, 6.0, 6.5), (587, 6.5, 7.0), (523, 7.0, 7.5), (494, 7.5, 8.0),
            # Tercer patrón (4 segundos)
            (392, 8.0, 8.5), (440, 8.5, 9.0), (494, 9.0, 9.5), (523, 9.5, 10.0),
            (494, 10.0, 10.5), (440, 10.5, 11.0), (392, 11.0, 11.5), (349, 11.5, 12.0),
            # Cuarto patrón (4 segundos)
            (440, 12.0, 12.5), (523, 12.5, 13.0), (587, 13.0, 13.5), (659, 13.5, 14.0),
            (587, 14.0, 14.5), (523, 14.5, 15.0), (440, 15.0, 15.5), (392, 15.5, 16.0),
        ]
        
        melody = np.zeros(len(t))
        
        for freq, start, end in melody_notes:
            start_idx = int(start * self.sample_rate)
            end_idx = int(end * self.sample_rate)
            if end_idx < len(melody):
                note_t = t[start_idx:end_idx] - start
                note = np.sin(2 * np.pi * freq * note_t)
                
                # Envelope suave
                note_duration = end - start
                attack_samples = int(0.05 * self.sample_rate)
                release_samples = int(0.1 * self.sample_rate)
                
                envelope = np.ones(len(note_t))
                if len(note_t) > attack_samples:
                    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                if len(note_t) > release_samples:
                    envelope[-release_samples:] = np.linspace(1, 0, release_samples)
                
                melody[start_idx:end_idx] = note * envelope * 0.15
        
        # Pad atmosférico (acordes sostenidos)
        pad = np.zeros(len(t))
        chord_changes = [
            # Acordes que cambian cada 4 segundos
            ([220, 277, 330], 0, 4),    # Am
            ([262, 330, 392], 4, 8),    # C
            ([349, 440, 523], 8, 12),   # F
            ([392, 494, 587], 12, 16),  # G
        ]
        
        for freqs, start, end in chord_changes:
            start_idx = int(start * self.sample_rate)
            end_idx = int(end * self.sample_rate)
            if end_idx < len(pad):
                chord_t = t[start_idx:end_idx] - start
                chord_wave = np.zeros(len(chord_t))
                
                for freq in freqs:
                    chord_wave += np.sin(2 * np.pi * freq * chord_t) / len(freqs)
                
                # Envelope muy suave para el pad
                envelope = np.ones(len(chord_t))
                fade_samples = int(0.5 * self.sample_rate)
                if len(chord_t) > fade_samples:
                    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
                    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
                
                pad[start_idx:end_idx] = chord_wave * envelope * 0.1
        
        # Combinar todas las capas
        wave = bass + melody + pad
        
        # Normalizar
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        
        wave = np.int16(wave * 32767 * 0.6)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_victory_sound(self):
        """Genera sonido de victoria"""
        duration = 1.0
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Arpeggio ascendente
        notes = [523, 659, 784, 1047]  # C - E - G - C (octava alta)
        wave = np.zeros(len(t))
        
        note_duration = duration / len(notes)
        for i, freq in enumerate(notes):
            start_idx = int(i * note_duration * self.sample_rate)
            end_idx = int((i + 1) * note_duration * self.sample_rate)
            if end_idx < len(wave):
                note_t = t[start_idx:end_idx] - t[start_idx]
                note = np.sin(2 * np.pi * freq * note_t)
                envelope = np.exp(-note_t * 2)
                wave[start_idx:end_idx] = note * envelope
        
        # Normalizar
        wave = np.int16(wave * 32767 * 0.5)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def generate_game_over_sound(self):
        """Genera sonido de game over"""
        duration = 1.0
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Arpeggio descendente
        notes = [523, 392, 330, 262]  # C - G - E - C (descendente)
        wave = np.zeros(len(t))
        
        note_duration = duration / len(notes)
        for i, freq in enumerate(notes):
            start_idx = int(i * note_duration * self.sample_rate)
            end_idx = int((i + 1) * note_duration * self.sample_rate)
            if end_idx < len(wave):
                note_t = t[start_idx:end_idx] - t[start_idx]
                note = np.sin(2 * np.pi * freq * note_t)
                envelope = np.exp(-note_t * 1.5)
                wave[start_idx:end_idx] = note * envelope
        
        # Normalizar
        wave = np.int16(wave * 32767 * 0.5)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)