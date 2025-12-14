import psutil
import requests
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from typing import Optional
from ..utils.constants import (
    AOE4_PROCESS_NAMES,
    AOE4_API_URL,
    PROCESS_CHECK_INTERVAL,
    API_CHECK_INTERVAL,
    DETECTION_MODE_PROCESS,
    DETECTION_MODE_API,
    DETECTION_MODE_MANUAL,
)


class GameDetector(QObject):
    """Detects if Age of Empires 4 game is running using multiple methods."""
    
    # Signals
    game_started = pyqtSignal()
    game_ended = pyqtSignal()
    status_changed = pyqtSignal(str)  # Status message for UI
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mode = DETECTION_MODE_PROCESS
        self._profile_id: Optional[str] = None
        self._is_game_running = False
        self._is_detecting = False
        
        # Timers for different detection modes
        self._process_timer = QTimer(self)
        self._process_timer.timeout.connect(self._check_process)
        
        self._api_timer = QTimer(self)
        self._api_timer.timeout.connect(self._check_api)
    
    @property
    def mode(self) -> str:
        return self._mode
    
    @mode.setter
    def mode(self, value: str):
        was_detecting = self._is_detecting
        if was_detecting:
            self.stop_detection()
        self._mode = value
        if was_detecting:
            self.start_detection()
    
    @property
    def profile_id(self) -> Optional[str]:
        return self._profile_id
    
    @profile_id.setter
    def profile_id(self, value: Optional[str]):
        self._profile_id = value
    
    @property
    def is_game_running(self) -> bool:
        return self._is_game_running
    
    @property
    def is_detecting(self) -> bool:
        return self._is_detecting
    
    def start_detection(self):
        """Start game detection based on current mode."""
        if self._is_detecting:
            return
        
        self._is_detecting = True
        
        if self._mode == DETECTION_MODE_PROCESS:
            self.status_changed.emit("Process algılama aktif...")
            self._check_process()  # Immediate check
            self._process_timer.start(PROCESS_CHECK_INTERVAL)
            
        elif self._mode == DETECTION_MODE_API:
            if not self._profile_id:
                self.status_changed.emit("Hata: Profile ID gerekli!")
                self._is_detecting = False
                return
            self.status_changed.emit("API algılama aktif...")
            self._check_api()  # Immediate check
            self._api_timer.start(API_CHECK_INTERVAL)
            
        elif self._mode == DETECTION_MODE_MANUAL:
            self.status_changed.emit("Manuel mod - Start'a basın")
    
    def stop_detection(self):
        """Stop all detection timers."""
        self._is_detecting = False
        self._process_timer.stop()
        self._api_timer.stop()
        self.status_changed.emit("Algılama durduruldu")
    
    def manual_start(self):
        """Manually signal game start (for manual mode)."""
        if self._mode == DETECTION_MODE_MANUAL:
            self._set_game_running(True)
    
    def manual_stop(self):
        """Manually signal game end (for manual mode)."""
        if self._mode == DETECTION_MODE_MANUAL:
            self._set_game_running(False)
    
    def _check_process(self):
        """Check if AoE4 process is running."""
        try:
            is_running = False
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] in AOE4_PROCESS_NAMES:
                        is_running = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self._set_game_running(is_running)
            
        except Exception as e:
            self.status_changed.emit(f"Process kontrol hatası: {str(e)}")
    
    def _check_api(self):
        """Check if there's an ongoing game via AoE4World API."""
        if not self._profile_id:
            return
        
        try:
            url = AOE4_API_URL.format(profile_id=self._profile_id)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                is_ongoing = data.get('ongoing', False)
                self._set_game_running(is_ongoing)
            else:
                self.status_changed.emit(f"API hatası: {response.status_code}")
                
        except requests.RequestException as e:
            self.status_changed.emit(f"API bağlantı hatası: {str(e)}")
        except Exception as e:
            self.status_changed.emit(f"API kontrol hatası: {str(e)}")
    
    def _set_game_running(self, is_running: bool):
        """Update game running state and emit signals."""
        if is_running != self._is_game_running:
            self._is_game_running = is_running
            
            if is_running:
                self.status_changed.emit("Oyun algılandı!")
                self.game_started.emit()
            else:
                self.status_changed.emit("Oyun bitti")
                self.game_ended.emit()


