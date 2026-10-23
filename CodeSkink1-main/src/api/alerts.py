"""
LifeLine Navigator — Alerts & Accessibility Engine
Siren detection (audio processing) + vibration/flash patterns for deaf/HoH users.
Manual implementation — showcases signal processing work.
"""
import numpy as np
import time
import threading
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from src.config import VIBRATION_PATTERNS, FLASH_COLORS


class AlertState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    DETECTED = "detected"
    ALERTING = "alerting"
    COOLDOWN = "cooldown"


@dataclass
class AudioFeatures:
    """Extracted audio features for classification."""
    mfcc: np.ndarray           # 13 MFCC coefficients
    spectral_centroid: float
    spectral_rolloff: float
    zero_crossing_rate: float
    rms_energy: float
    dominant_freq: float


class SirenDetector:
    """
    Lightweight siren detector using traditional DSP (no heavy ML).
    Detects characteristic siren patterns: frequency sweep, modulation.
    Manual implementation — not an API wrapper.
    """

    # Siren characteristics (typical Indian emergency sirens)
    SIREN_FREQ_RANGE = (300, 2000)       # Hz
    SIREN_SWEEP_RATE_MIN = 0.5           # Hz/sec (slow sweep)
    SIREN_SWEEP_RATE_MAX = 10.0          # Hz/sec (fast sweep)
    SIREN_MODULATION_FREQ = (1, 5)       # Hz (wail/yelp pattern)
    MIN_DURATION_SEC = 2.0               # Minimum siren duration
    CONFIDENCE_THRESHOLD = 0.6

    def __init__(self, sample_rate: int = 16000, frame_size: int = 1024, hop_size: int = 512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.state = AlertState.IDLE
        self._buffer = np.array([], dtype=np.float32)
        self._feature_history: List[AudioFeatures] = []
        self._last_detection_time = 0
        self._callback = None

    def set_callback(self, callback):
        """Set callback function(alert_type, confidence, features)."""
        self._callback = callback

    def process_audio(self, audio_chunk: np.ndarray) -> Optional[Dict]:
        """
        Process incoming audio chunk.
        Returns detection result dict or None.
        """
        # Append to buffer
        self._buffer = np.concatenate([self._buffer, audio_chunk.astype(np.float32)])

        # Process in frames
        results = []
        while len(self._buffer) >= self.frame_size:
            frame = self._buffer[:self.frame_size]
            self._buffer = self._buffer[self.hop_size:]

            features = self._extract_features(frame)
            self._feature_history.append(features)

            # Keep limited history
            if len(self._feature_history) > 50:
                self._feature_history.pop(0)

            # Classify
            result = self._classify_siren(features)
            if result:
                results.append(result)

        # Return highest confidence detection
        if results:
            best = max(results, key=lambda r: r["confidence"])
            if best["confidence"] >= self.CONFIDENCE_THRESHOLD:
                self._trigger_alert(best)
                return best

        return None

    def _extract_features(self, frame: np.ndarray) -> AudioFeatures:
        """Extract audio features from frame."""
        # Apply window
        windowed = frame * np.hanning(len(frame))

        # FFT
        fft = np.fft.rfft(windowed)
        magnitude = np.abs(fft)
        freqs = np.fft.rfftfreq(len(frame), 1/self.sample_rate)

        # RMS Energy
        rms = np.sqrt(np.mean(frame**2))

        # Zero Crossing Rate
        zcr = np.sum(np.diff(np.signbit(frame))) / len(frame)

        # Spectral Centroid
        if np.sum(magnitude) > 0:
            centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
        else:
            centroid = 0

        # Spectral Rolloff (85%)
        cumsum = np.cumsum(magnitude)
        rolloff_idx = np.where(cumsum >= 0.85 * cumsum[-1])[0]
        rolloff = freqs[rolloff_idx[0]] if len(rolloff_idx) > 0 else 0

        # Dominant Frequency
        dom_idx = np.argmax(magnitude)
        dom_freq = freqs[dom_idx] if dom_idx < len(freqs) else 0

        # Simple MFCC approximation (13 coeffs via DCT of log mel spectrogram)
        # Simplified: use 13 mel filterbank energies
        mel_energies = self._mel_filterbank(magnitude, freqs)
        mfcc = self._dct(mel_energies)[:13] if len(mel_energies) >= 13 else np.zeros(13)

        return AudioFeatures(
            mfcc=mfcc,
            spectral_centroid=centroid,
            spectral_rolloff=rolloff,
            zero_crossing_rate=zcr,
            rms_energy=rms,
            dominant_freq=dom_freq
        )

    def _mel_filterbank(self, magnitude: np.ndarray, freqs: np.ndarray, n_mels: int = 26) -> np.ndarray:
        """Simple mel filterbank."""
        # Mel scale conversion
        def hz_to_mel(hz): return 2595 * np.log10(1 + hz / 700)
        def mel_to_hz(mel): return 700 * (10**(mel / 2595) - 1)

        mel_min, mel_max = hz_to_mel(0), hz_to_mel(self.sample_rate / 2)
        mel_points = np.linspace(mel_min, mel_max, n_mels + 2)
        hz_points = mel_to_hz(mel_points)

        filterbank = np.zeros((n_mels, len(magnitude)))
        for i in range(n_mels):
            f_left, f_center, f_right = hz_points[i], hz_points[i+1], hz_points[i+2]
            left_idx = np.searchsorted(freqs, f_left)
            center_idx = np.searchsorted(freqs, f_center)
            right_idx = np.searchsorted(freqs, f_right)

            if left_idx < center_idx:
                filterbank[i, left_idx:center_idx] = (freqs[left_idx:center_idx] - f_left) / (f_center - f_left)
            if center_idx < right_idx:
                filterbank[i, center_idx:right_idx] = (f_right - freqs[center_idx:right_idx]) / (f_right - f_center)

        return np.dot(filterbank, magnitude)

    def _dct(self, x: np.ndarray) -> np.ndarray:
        """Discrete Cosine Transform Type-II."""
        N = len(x)
        n = np.arange(N)
        k = np.arange(N).reshape(-1, 1)
        dct_matrix = np.cos(np.pi / N * (n + 0.5) * k)
        dct_matrix[0, :] *= 1 / np.sqrt(2)
        return np.dot(dct_matrix, x) * np.sqrt(2 / N)

    def _classify_siren(self, features: AudioFeatures) -> Optional[Dict]:
        """
        Rule-based siren classification.
        Checks for: frequency sweep, modulation, energy pattern.
        """
        # Basic energy gate
        if features.rms_energy < 0.01:
            return None

        # Frequency in siren range?
        freq_ok = self.SIREN_FREQ_RANGE[0] <= features.dominant_freq <= self.SIREN_FREQ_RANGE[1]
        if not freq_ok:
            return None

        # Need history for sweep/modulation detection
        if len(self._feature_history) < 10:
            return None

        # Check for frequency sweep (siren wail)
        recent_freqs = [f.dominant_freq for f in self._feature_history[-20:]]
        freq_changes = np.diff(recent_freqs)
        sweep_rate = np.mean(np.abs(freq_changes)) * (self.sample_rate / self.hop_size)

        sweep_ok = self.SIREN_SWEEP_RATE_MIN <= sweep_rate <= self.SIREN_SWEEP_RATE_MAX

        # Check for modulation (yelp/wail pattern)
        recent_energy = [f.rms_energy for f in self._feature_history[-30:]]
        if len(recent_energy) > 10:
            # Autocorrelation to find modulation frequency
            energy_norm = (recent_energy - np.mean(recent_energy)) / (np.std(recent_energy) + 1e-6)
            autocorr = np.correlate(energy_norm, energy_norm, mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            peaks = np.where((autocorr[1:-1] > autocorr[:-2]) & (autocorr[1:-1] > autocorr[2:]))[0] + 1
            if len(peaks) > 1:
                mod_period = np.mean(np.diff(peaks)) * self.hop_size / self.sample_rate
                mod_freq = 1.0 / mod_period if mod_period > 0 else 0
                mod_ok = self.SIREN_MODULATION_FREQ[0] <= mod_freq <= self.SIREN_MODULATION_FREQ[1]
            else:
                mod_ok = False
        else:
            mod_ok = False

        # Confidence scoring
        confidence = 0.0
        if freq_ok: confidence += 0.3
        if sweep_ok: confidence += 0.4
        if mod_ok: confidence += 0.3

        if confidence >= self.CONFIDENCE_THRESHOLD:
            # Classify siren type based on pattern
            if sweep_rate > 3.0:
                alert_type = "fire"  # Fast sweep = fire/ambulance
            elif mod_ok:
                alert_type = "evacuate"  # Modulated = civil defense
            else:
                alert_type = "siren_generic"

            return {
                "alert_type": alert_type,
                "confidence": min(confidence, 1.0),
                "features": {
                    "dominant_freq": features.dominant_freq,
                    "sweep_rate": sweep_rate,
                    "modulation_freq": mod_freq if 'mod_freq' in locals() else 0,
                    "rms_energy": features.rms_energy
                }
            }

        return None

    def _trigger_alert(self, detection: Dict):
        """Trigger alert callback and haptic/visual feedback."""
        now = time.time()
        if now - self._last_detection_time < 5.0:  # Debounce
            return
        self._last_detection_time = now

        self.state = AlertState.ALERTING
        if self._callback:
            self._callback(detection["alert_type"], detection["confidence"], detection["features"])
        self.state = AlertState.IDLE


class HapticFeedback:
    """
    Vibration pattern generator for mobile devices.
    Uses Web Vibration API via Streamlit JS injection.
    """

    def __init__(self):
        self.patterns = VIBRATION_PATTERNS

    def get_pattern(self, alert_type: str) -> List[int]:
        """Get vibration pattern for alert type (milliseconds)."""
        return self.patterns.get(alert_type, self.patterns["siren_generic"])

    def get_js_code(self, alert_type: str) -> str:
        """Generate JavaScript to trigger vibration on mobile."""
        pattern = self.get_pattern(alert_type)
        # Web Vibration API: navigator.vibrate(pattern)
        return f"""
        <script>
        if (navigator.vibrate) {{
            navigator.vibrate({pattern});
        }}
        </script>
        """

    def get_flash_css(self, alert_type: str) -> str:
        """Generate CSS for visual flash animation."""
        color = FLASH_COLORS.get(alert_type, FLASH_COLORS["siren_generic"])
        return f"""
        <style>
        @keyframes emergency-flash {{
            0%, 100% {{ background-color: transparent; }}
            50% {{ background-color: {color}80; }}
        }}
        .emergency-flash {{
            animation: emergency-flash 0.5s ease-in-out 3;
            pointer-events: none;
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 9999;
        }}
        </style>
        <div class="emergency-flash"></div>
        """


class AlertManager:
    """
    High-level alert coordination: siren detection + haptic + visual + notifications.
    """

    def __init__(self):
        self.detector = SirenDetector()
        self.haptic = HapticFeedback()
        self.active_alerts: List[Dict] = []
        self._setup_detector_callback()

    def _setup_detector_callback(self):
        def on_detect(alert_type, confidence, features):
            alert = {
                "type": alert_type,
                "confidence": confidence,
                "features": features,
                "timestamp": time.time()
            }
            self.active_alerts.append(alert)
            # Trigger haptic + visual
            self.trigger_haptic(alert_type)
            self.trigger_visual(alert_type)
        self.detector.set_callback(on_detect)

    def process_audio(self, audio_chunk: np.ndarray) -> Optional[Dict]:
        """Process audio through detector."""
        return self.detector.process_audio(audio_chunk)

    def trigger_haptic(self, alert_type: str):
        """Trigger vibration pattern."""
        # In Streamlit, this injects JS
        return self.haptic.get_js_code(alert_type)

    def trigger_visual(self, alert_type: str):
        """Trigger visual flash."""
        return self.haptic.get_flash_css(alert_type)

    def trigger_manual_alert(self, alert_type: str, message: str = "") -> Dict:
        """Manually trigger alert (for testing/demo)."""
        alert = {
            "type": alert_type,
            "confidence": 1.0,
            "features": {},
            "timestamp": time.time(),
            "manual": True,
            "message": message
        }
        self.active_alerts.append(alert)
        self.trigger_haptic(alert_type)
        self.trigger_visual(alert_type)
        return alert

    def get_active_alerts(self, max_age_sec: float = 30.0) -> List[Dict]:
        """Get recent alerts."""
        now = time.time()
        return [a for a in self.active_alerts if now - a["timestamp"] < max_age_sec]

    def clear_alerts(self):
        self.active_alerts.clear()


# ──────────────────────────────────────────────
# SINGLETON
# ──────────────────────────────────────────────
_alert_manager = None

def get_alert_manager() -> AlertManager:
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager