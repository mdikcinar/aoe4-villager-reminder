import requests
import psutil
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from typing import Optional
from ..utils.constants import (
    AOE4_API_URL,
    API_CHECK_INTERVAL,
    AOE4_EXECUTABLE,
    PROCESS_CHECK_INTERVAL,
    DETECTION_MODE_API,
    DETECTION_MODE_MANUAL,
)
from ..utils.localization import tr


class GameDetector(QObject):
    """Detects if Age of Empires 4 match is ongoing via API or manual mode."""
    
    # Signals
    game_started = pyqtSignal()
    game_ended = pyqtSignal()
    status_changed = pyqtSignal(str)  # Status message for UI
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mode = DETECTION_MODE_API
        self._profile_id: Optional[str] = None
        self._is_game_running = False
        self._is_game_exe_running = False
        self._is_detecting = False
        
        # Timer for process detection (checks if game exe is running)
        self._process_timer = QTimer(self)
        self._process_timer.timeout.connect(self._check_game_process)
        
        # Timer for API detection
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
    def is_game_exe_running(self) -> bool:
        return self._is_game_exe_running
    
    @property
    def is_detecting(self) -> bool:
        return self._is_detecting
    
    def start_detection(self):
        """Start game detection based on current mode."""
        if self._is_detecting:
            return
        
        self._is_detecting = True
        
        if self._mode == DETECTION_MODE_API:
            if not self._profile_id:
                self.status_changed.emit(tr("detection_error_profile_required"))
                self._is_detecting = False
                return
            # Start process detection first - API will start when game exe is running
            self.status_changed.emit(tr("detection_waiting_for_game"))
            self._check_game_process()  # Immediate check
            self._process_timer.start(PROCESS_CHECK_INTERVAL)
            
        elif self._mode == DETECTION_MODE_MANUAL:
            self.status_changed.emit(tr("detection_manual_mode"))
    
    def stop_detection(self):
        """Stop detection timer."""
        self._is_detecting = False
        self._process_timer.stop()
        self._api_timer.stop()
        self._is_game_exe_running = False
        self.status_changed.emit(tr("detection_stopped"))
    
    def manual_start(self):
        """Manually signal game start (for manual mode)."""
        if self._mode == DETECTION_MODE_MANUAL:
            self._set_game_running(True)
    
    def manual_stop(self):
        """Manually signal game end (for manual mode)."""
        if self._mode == DETECTION_MODE_MANUAL:
            self._set_game_running(False)
    
    def _check_game_process(self):
        """Check if the AoE4 game executable is running."""
        is_running = False
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == AOE4_EXECUTABLE.lower():
                    is_running = True
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        
        if is_running != self._is_game_exe_running:
            self._is_game_exe_running = is_running
            
            if is_running:
                # Game exe started - start API checks
                self.status_changed.emit(tr("detection_game_exe_detected"))
                check_interval_sec = API_CHECK_INTERVAL // 1000
                self.status_changed.emit(tr("detection_api_active").format(interval=check_interval_sec))
                self._check_api()  # Immediate check
                self._api_timer.start(API_CHECK_INTERVAL)
            else:
                # Game exe closed - stop API checks
                self._api_timer.stop()
                if self._is_game_running:
                    self._set_game_running(False)
                self.status_changed.emit(tr("detection_game_exe_closed"))
    
    def _check_api(self):
        """Check if there's an ongoing game via AoE4World API."""
        if not self._profile_id:
            return
        
        # Don't check API if game exe is not running
        if not self._is_game_exe_running:
            return
        
        # Inform user that API check is starting
        self.status_changed.emit(tr("detection_checking_api"))
        
        try:
            url = AOE4_API_URL.format(profile_id=self._profile_id)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                is_ongoing = data.get('ongoing', False)
                
                if is_ongoing:
                    # Game is ongoing - will be handled by _set_game_running
                    pass
                else:
                    # No ongoing game
                    self.status_changed.emit(tr("detection_api_check_complete"))
                
                self._set_game_running(is_ongoing)
            elif response.status_code == 404:
                self.status_changed.emit(tr("detection_profile_not_found"))
            else:
                self.status_changed.emit(tr("detection_api_error").format(code=response.status_code))
                
        except requests.Timeout:
            self.status_changed.emit(tr("detection_api_timeout"))
        except requests.ConnectionError:
            self.status_changed.emit(tr("detection_connection_error"))
        except requests.RequestException as e:
            error_msg = str(e)[:30]
            self.status_changed.emit(tr("detection_api_connection_error").format(error=error_msg))
        except Exception as e:
            error_msg = str(e)[:30]
            self.status_changed.emit(tr("detection_api_check_error").format(error=error_msg))
    
    def _set_game_running(self, is_running: bool):
        """Update game running state and emit signals."""
        if is_running != self._is_game_running:
            self._is_game_running = is_running
            
            if is_running:
                self.status_changed.emit(tr("detection_match_started"))
                self.game_started.emit()
            else:
                self.status_changed.emit(tr("detection_match_ended"))
                self.game_ended.emit()


