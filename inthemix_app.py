#!/usr/bin/env python3
"""
InTheMix - MP3 Remix & Mashup App
=================================
Uno strumento potente per creare DIVERTIMENTO!

Caratteristiche:
- Remix Techno/House automatici
- Mashup di due brani con 4 modalità diverse
- Sincronizzazione BPM automatica
- Separazione vocali/strumentali
- Effetti audio professionali

Dipendenze:
pip install librosa soundfile numpy scipy pydub scikit-learn

Autore: GitHub @umbertomaravigna61-debug
"""

import librosa
import librosa.effects
import soundfile as sf
import numpy as np
from scipy import signal
from pydub import AudioSegment
import os
import sys

class InTheMixApp:
    def __init__(self):
        self.sample_rate = 44100
        print("🎵 InTheMix - Benvenuto nel mondo del remix! 🎵")
        print("=" * 60)
    
    def load_audio(self, file_path):
        """Carica file audio e lo converte nel formato richiesto"""
        try:
            print(f"📂 Caricamento: {os.path.basename(file_path)}")
            y, sr = librosa.load(file_path, sr=self.sample_rate)
            print(f"✅ Caricato: {len(y)/self.sample_rate:.2f}s")
            return y, sr
        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            return None, None

    # =================== REMIX ENGINE ===================
    
    def create_techno_remix(self, audio, sr):
        """Trasforma l'audio in stile Techno (130 BPM)"""
        print("🔥 Creando remix Techno...")
        
        # Analizza tempo originale
        tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
        print(f"   Tempo originale: {tempo:.1f} BPM")
        
        # Sincronizza a 130 BPM (tipico Techno)
        target_tempo = 130
        tempo_ratio = target_tempo / tempo
        audio_stretched = librosa.effects.time_stretch(audio, rate=1/tempo_ratio)
        print(f"   Nuovo tempo: {target_tempo} BPM")
        
        # Effetti Techno
        audio_compressed = self._apply_compression(audio_stretched, ratio=8)
        audio_reverb = self._add_reverb(audio_compressed, sr, room_size=0.3)
        audio_eq = self._techno_eq(audio_reverb, sr)
        audio_gated = self._add_gate_effect(audio_eq, sr, gate_freq=8)
        
        print("   ✅ Remix Techno completato!")
        return audio_gated
    
    def create_house_remix(self, audio, sr):
        """Trasforma l'audio in stile House (125 BPM)"""
        print("🕺 Creando remix House...")
        
        tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
        print(f"   Tempo originale: {tempo:.1f} BPM")
        
        # Sincronizza a 125 BPM (tipico House)
        target_tempo = 125
        tempo_ratio = target_tempo / tempo
        audio_stretched = librosa.effects.time_stretch(audio, rate=1/tempo_ratio)
        print(f"   Nuovo tempo: {target_tempo} BPM")
        
        # Effetti House
        audio_compressed = self._apply_compression(audio_stretched, ratio=4)
        audio_bass_boosted = self._house_bass_boost(audio_compressed, sr)
        audio_swing = self._add_swing(audio_bass_boosted, sr)
        audio_reverb = self._add_reverb(audio_swing, sr, room_size=0.7)
        
        print("   ✅ Remix House completato!")
        return audio_reverb

    # =================== MASHUP ENGINE ===================
    
    def load_and_sync_audio_pair(self, file1, file2):
        """Carica due file audio e analizza i loro tempi"""
        print("🎭 Caricamento coppia per mashup...")
        
        audio1, sr1 = self.load_audio(file1)
        audio2, sr2 = self.load_audio(file2)
        
        if audio1 is None or audio2 is None:
            return None, None, None
            
        # Analizza i tempi
        tempo1, beats1 = librosa.beat.beat_track(y=audio1, sr=self.sample_rate)
        tempo2, beats2 = librosa.beat.beat_track(y=audio2, sr=self.sample_rate)
        
        print(f"   Track 1: {tempo1:.1f} BPM")
        print(f"   Track 2: {tempo2:.1f} BPM")
        
        return audio1, audio2, (tempo1, tempo2, beats1, beats2)
    
    def create_mashup(self, audio1, audio2, tempo_info, mashup_type="classic"):
        """Crea diversi tipi di mashup"""
        tempo1, tempo2, beats1, beats2 = tempo_info
        
        mashup_methods = {
            "classic": self._classic_mashup,
            "vocal_instrumental": self._vocal_instrumental_mashup,
            "harmonic_percussive": self._harmonic_percussive_mashup,
            "frequency_split": self._frequency_split_mashup
        }
        
        method = mashup_methods.get(mashup_type, self._classic_mashup)
        return method(audio1, audio2, tempo1, tempo2)
    
    def _classic_mashup(self, audio1, audio2, tempo1, tempo2):
        """Mashup classico: mix bilanciato con sincronizzazione"""
        print("🎼 Mashup classico in corso...")
        
        # Sincronizza al tempo medio
        target_tempo = (tempo1 + tempo2) / 2
        print(f"   Tempo target: {target_tempo:.1f} BPM")
        
        ratio1 = target_tempo / tempo1
        ratio2 = target_tempo / tempo2
        
        sync_audio1 = librosa.effects.time_stretch(audio1, rate=1/ratio1)
        sync_audio2 = librosa.effects.time_stretch(audio2, rate=1/ratio2)
        
        # Equalizza lunghezze
        min_length = min(len(sync_audio1), len(sync_audio2))
        sync_audio1 = sync_audio1[:min_length]
        sync_audio2 = sync_audio2[:min_length]
        
        # Mix dinamico
        mashup = self._dynamic_mix(sync_audio1, sync_audio2)
        return mashup
    
    def _vocal_instrumental_mashup(self, audio1, audio2, tempo1, tempo2):
        """Combina vocal di una traccia con instrumental dell'altra"""
        print("🎤 Mashup vocal/instrumental in corso...")
        
        # Sincronizza
        target_tempo = (tempo1 + tempo2) / 2
        ratio1 = target_tempo / tempo1
        ratio2 = target_tempo / tempo2
        
        sync_audio1 = librosa.effects.time_stretch(audio1, rate=1/ratio1)
        sync_audio2 = librosa.effects.time_stretch(audio2, rate=1/ratio2)
        
        min_length = min(len(sync_audio1), len(sync_audio2))
        sync_audio1 = sync_audio1[:min_length]
        sync_audio2 = sync_audio2[:min_length]
        
        # Separa vocal e instrumental
        vocals1, instrumental1 = self._separate_vocals(sync_audio1)
        vocals2, instrumental2 = self._separate_vocals(sync_audio2)
        
        # Scegli la migliore combinazione
        vocal_energy1 = np.mean(vocals1**2)
        vocal_energy2 = np.mean(vocals2**2)
        
        if vocal_energy1 > vocal_energy2:
            mashup = vocals1 * 0.7 + instrumental2 * 0.8
            print("   Vocal da traccia 1 + instrumental da traccia 2")
        else:
            mashup = vocals2 * 0.7 + instrumental1 * 0.8
            print("   Vocal da traccia 2 + instrumental da traccia 1")
            
        return self._normalize_audio(mashup)
    
    def _harmonic_percussive_mashup(self, audio1, audio2, tempo1, tempo2):
        """Combina elementi armonici e percussivi"""
        print("🥁 Mashup armonico/percussivo in corso...")
        
        # Sincronizza
        target_tempo = (tempo1 + tempo2) / 2
        ratio1 = target_tempo / tempo1
        ratio2 = target_tempo / tempo2
        
        sync_audio1 = librosa.effects.time_stretch(audio1, rate=1/ratio1)
        sync_audio2 = librosa.effects.time_stretch(audio2, rate=1/ratio2)
        
        min_length = min(len(sync_audio1), len(sync_audio2))
        sync_audio1 = sync_audio1[:min_length]
        sync_audio2 = sync_audio2[:min_length]
        
        # Separa componenti
        harmonic1, percussive1 = librosa.effects.hpss(sync_audio1)
        harmonic2, percussive2 = librosa.effects.hpss(sync_audio2)
        
        # Combina intelligentemente
        percussive_energy1 = np.mean(percussive1**2)
        percussive_energy2 = np.mean(percussive2**2)
        
        if percussive_energy1 > percussive_energy2:
            mashup = harmonic2 * 0.6 + percussive1 * 0.8
            print("   Armonie da traccia 2 + percussioni da traccia 1")
        else:
            mashup = harmonic1 * 0.6 + percussive2 * 0.8
            print("   Armonie da traccia 1 + percussioni da traccia 2")
            
        return self._normalize_audio(mashup)
    
    def _frequency_split_mashup(self, audio1, audio2, tempo1, tempo2):
        """Combina bassi da una traccia e acuti dall'altra"""
        print("🎛️ Mashup divisione frequenze in corso...")
        
        # Sincronizza
        target_tempo = (tempo1 + tempo2) / 2
        ratio1 = target_tempo / tempo1
        ratio2 = target_tempo / tempo2
        
        sync_audio1 = librosa.effects.time_stretch(audio1, rate=1/ratio1)
        sync_audio2 = librosa.effects.time_stretch(audio2, rate=1/ratio2)
        
        min_length = min(len(sync_audio1), len(sync_audio2))
        sync_audio1 = sync_audio1[:min_length]
        sync_audio2 = sync_audio2[:min_length]
        
        # Filtri per dividere a 800Hz
        nyquist = self.sample_rate // 2
        crossover_freq = 800
        crossover_normalized = crossover_freq / nyquist
        
        b_low, a_low = signal.butter(4, crossover_normalized, btype='low')
        b_high, a_high = signal.butter(4, crossover_normalized, btype='high')
        
        # Separa frequenze
        bass1 = signal.filtfilt(b_low, a_low, sync_audio1)
        bass2 = signal.filtfilt(b_low, a_low, sync_audio2)
        treble1 = signal.filtfilt(b_high, a_high, sync_audio1)
        treble2 = signal.filtfilt(b_high, a_high, sync_audio2)
        
        # Combina intelligentemente
        bass_energy1 = np.mean(bass1**2)
        bass_energy2 = np.mean(bass2**2)
        
        if bass_energy1 > bass_energy2:
            mashup = bass1 + treble2
            print("   Bassi da traccia 1 + acuti da traccia 2")
        else:
            mashup = bass2 + treble1
            print("   Bassi da traccia 2 + acuti da traccia 1")
            
        return self._normalize_audio(mashup)

    # =================== EFFETTI AUDIO ===================
    
    def _apply_compression(self, audio, ratio=8, threshold=0.1):
        """Applica compressione dinamica"""
        compressed = np.copy(audio)
        over_threshold = np.abs(compressed) > threshold
        compressed[over_threshold] = (
            np.sign(compressed[over_threshold]) * 
            (threshold + (np.abs(compressed[over_threshold]) - threshold) / ratio)
        )
        return compressed
    
    def _add_reverb(self, audio, sr, room_size=0.5):
        """Aggiunge riverbero"""
        reverb_length = int(sr * 0.5)
        reverb_impulse = np.random.normal(0, 0.1, reverb_length) * np.exp(-np.linspace(0, 5, reverb_length))
        audio_reverb = signal.convolve(audio, reverb_impulse * room_size, mode='same')
        return audio * 0.7 + audio_reverb * 0.3
    
    def _techno_eq(self, audio, sr):
        """EQ per Techno: boost medi-acuti"""
        return librosa.effects.preemphasis(audio, coef=0.1) * 1.2
    
    def _house_bass_boost(self, audio, sr):
        """Boost bassi per House"""
        nyquist = sr // 2
        low_cutoff = 200 / nyquist
        b, a = signal.butter(4, low_cutoff, btype='low')
        bass = signal.filtfilt(b, a, audio)
        return audio + bass * 0.5
    
    def _add_gate_effect(self, audio, sr, gate_freq=8):
        """Gate ritmico per Techno"""
        gate_samples = sr // gate_freq
        gate_pattern = np.tile([1, 1, 0.3, 1, 0.7, 1, 0.3, 0.8], 
                              len(audio) // (gate_samples * 8) + 1)
        gate_pattern = gate_pattern[:len(audio)]
        return audio * gate_pattern
    
    def _add_swing(self, audio, sr):
        """Swing groove per House"""
        swing_amount = 0.02
        swing_samples = int(sr * swing_amount)
        swung_audio = np.zeros_like(audio)
        beat_length = sr // 4
        
        for i in range(0, len(audio) - swing_samples, beat_length):
            if (i // beat_length) % 2 == 1:
                end_idx = min(i + beat_length, len(audio) - swing_samples)
                swung_audio[i + swing_samples:end_idx + swing_samples] = audio[i:end_idx]
            else:
                end_idx = min(i + beat_length, len(audio))
                swung_audio[i:end_idx] = audio[i:end_idx]
        
        return swung_audio
    
    def _separate_vocals(self, audio):
        """Separazione vocal/instrumental semplificata"""
        # Filtro per vocal (300-3400 Hz)
        nyquist = self.sample_rate // 2
        vocal_low = 300 / nyquist
        vocal_high = 3400 / nyquist
        
        b_vocal, a_vocal = signal.butter(4, [vocal_low, vocal_high], btype='band')
        vocals = signal.filtfilt(b_vocal, a_vocal, audio)
        instrumental = audio - vocals * 0.6
        
        return vocals, instrumental
    
    def _dynamic_mix(self, audio1, audio2, segments=8):
        """Mix dinamico con crossfading"""
        segment_length = len(audio1) // segments
        mashup = np.zeros_like(audio1)
        
        for i in range(segments):
            start = i * segment_length
            end = start + segment_length if i < segments-1 else len(audio1)
            
            # Alterna pesi
            if i % 2 == 0:
                weight1, weight2 = 0.7, 0.5
            else:
                weight1, weight2 = 0.5, 0.7
            
            mashup[start:end] = audio1[start:end] * weight1 + audio2[start:end] * weight2
            
        return mashup
    
    def _normalize_audio(self, audio):
        """Normalizza per prevenire clipping"""
        max_val = np.max(np.abs(audio))
        return audio / max_val * 0.95 if max_val > 0 else audio

    # =================== I/O AUDIO ===================
    
    def save_audio(self, audio, output_path):
        """Salva audio come MP3"""
        audio_normalized = self._normalize_audio(audio)
        
        # Salva temporaneamente come WAV
        temp_wav = output_path.replace('.mp3', '_temp.wav')
        sf.write(temp_wav, audio_normalized, self.sample_rate)
        
        # Converti in MP3
        try:
            audio_segment = AudioSegment.from_wav(temp_wav)
            audio_segment.export(output_path, format="mp3", bitrate="320k")
            os.remove(temp_wav)
            print(f"✅ Salvato: {output_path}")
        except Exception as e:
            print(f"❌ Errore nel salvataggio: {e}")

def main():
    """Interfaccia utente principale"""
    app = InTheMixApp()
    
    while True:
        print("\n🎛️ Cosa vuoi fare?")
        print("1. 🔥 Remix Techno")
        print("2. 🕺 Remix House") 
        print("3. 🎭 Mashup di due brani")
        print("4. ❌ Esci")
        
        choice = input("\nScelta (1-4): ").strip()
        
        if choice == "1" or choice == "2":
            # REMIX MODE
            input_file = input("📂 File MP3 da remixare: ").strip()
            
            if not os.path.exists(input_file):
                print("❌ File non trovato!")
                continue
            
            audio, sr = app.load_audio(input_file)
            if audio is None:
                continue
            
            base_name = os.path.splitext(input_file)[0]
            
            if choice == "1":
                remixed_audio = app.create_techno_remix(audio, sr)
                output_file = f"{base_name}_TECHNO_remix.mp3"
            else:
                remixed_audio = app.create_house_remix(audio, sr)
                output_file = f"{base_name}_HOUSE_remix.mp3"
            
            app.save_audio(remixed_audio, output_file)
            print(f"🎉 Remix completato!")
        
        elif choice == "3":
            # MASHUP MODE
            file1 = input("📂 Primo file MP3: ").strip()
            file2 = input("📂 Secondo file MP3: ").strip()
            
            if not os.path.exists(file1) or not os.path.exists(file2):
                print("❌ Uno o entrambi i file non esistono!")
                continue
            
            audio1, audio2, tempo_info = app.load_and_sync_audio_pair(file1, file2)
            if audio1 is None:
                continue
            
            print("\n🎭 Tipi di mashup:")
            print("1. Classico - Mix bilanciato")
            print("2. Vocal/Instrumental - Combina vocal e strumentali")
            print("3. Armonico/Percussivo - Combina armonie e ritmi")
            print("4. Divisione frequenze - Bassi + acuti")
            
            mashup_choice = input("Tipo di mashup (1-4): ").strip()
            
            mashup_types = {
                "1": "classic",
                "2": "vocal_instrumental",
                "3": "harmonic_percussive", 
                "4": "frequency_split"
            }
            
            if mashup_choice not in mashup_types:
                print("❌ Scelta non valida!")
                continue
            
            mashup_type = mashup_types[mashup_choice]
            mashup_audio = app.create_mashup(audio1, audio2, tempo_info, mashup_type)
            
            # Nome output
            name1 = os.path.splitext(os.path.basename(file1))[0]
            name2 = os.path.splitext(os.path.basename(file2))[0]
            output_file = f"{name1}_X_{name2}_MASHUP_{mashup_type}.mp3"
            
            app.save_audio(mashup_audio, output_file)
            print(f"🎉 Mashup completato!")
            print(f"Duration: {len(mashup_audio)/app.sample_rate:.2f} secondi")
        
        elif choice == "4":
            print("👋 Grazie per aver usato InTheMix!")
            break
        
        else:
            print("❌ Scelta non valida!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Uscita forzata. Ciao!")
    except Exception as e:
        print(f"\n❌ Errore imprevisto: {e}")
        print("Assicurati di aver installato tutte le dipendenze:")
        print("pip install librosa soundfile numpy scipy pydub scikit-learn")
