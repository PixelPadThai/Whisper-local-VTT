import time
import numpy as np
import sounddevice as sd
import webrtcvad
from PyQt5.QtCore import QThread, QMutex, pyqtSignal
from collections import deque
from threading import Event

from utils import ConfigManager


class VoiceListenerThread(QThread):
    """
    A thread class that continuously listens for voice activity in the background.
    When voice is detected, it emits a signal to start recording.
    
    This is used for the 'auto_voice_activation' recording mode.
    """

    voiceDetectedSignal = pyqtSignal()

    def __init__(self):
        """
        Initialize the VoiceListenerThread.
        """
        super().__init__()
        self.is_running = True
        self.sample_rate = None
        self.mutex = QMutex()

    def stop(self):
        """Stop the voice listener thread."""
        self.mutex.lock()
        self.is_running = False
        self.mutex.unlock()
        self.wait()

    def run(self):
        """Main execution method for the voice listener thread."""
        try:
            ConfigManager.console_print('Voice listener started - waiting for speech...')
            
            recording_options = ConfigManager.get_config_section('recording_options')
            self.sample_rate = recording_options.get('sample_rate') or 16000
            frame_duration_ms = 30  # 30ms frame duration for WebRTC VAD
            frame_size = int(self.sample_rate * (frame_duration_ms / 1000.0))

            # Create VAD for voice detection
            vad = webrtcvad.Vad(2)  # VAD aggressiveness: 0 to 3, 3 being the most aggressive
            
            # Need consecutive voice frames to avoid false positives
            consecutive_voice_frames_needed = 3
            consecutive_voice_count = 0

            audio_buffer = deque(maxlen=frame_size)
            data_ready = Event()

            def audio_callback(indata, frames, time, status):
                if status:
                    ConfigManager.console_print(f"Voice listener audio callback status: {status}")
                audio_buffer.extend(indata[:, 0])
                data_ready.set()

            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16',
                                blocksize=frame_size, device=recording_options.get('sound_device'),
                                callback=audio_callback):
                while self.is_running:
                    data_ready.wait(timeout=0.1)  # Add timeout to check is_running regularly
                    if not self.is_running:
                        break
                        
                    data_ready.clear()

                    if len(audio_buffer) < frame_size:
                        continue

                    # Process frame for voice detection
                    frame = np.array(list(audio_buffer), dtype=np.int16)
                    audio_buffer.clear()

                    # Check if frame contains speech
                    if vad.is_speech(frame.tobytes(), self.sample_rate):
                        consecutive_voice_count += 1
                        if consecutive_voice_count >= consecutive_voice_frames_needed:
                            ConfigManager.console_print('Voice detected! Starting recording...')
                            self.voiceDetectedSignal.emit()
                            break
                    else:
                        consecutive_voice_count = 0

        except Exception as e:
            ConfigManager.console_print(f'Voice listener error: {e}')
        finally:
            ConfigManager.console_print('Voice listener stopped.') 