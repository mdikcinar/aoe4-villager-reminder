from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from ..utils.constants import DEFAULT_INTERVAL


class TimerService(QObject):
    """Manages the villager production timer."""
    
    # Signals
    tick = pyqtSignal(int)  # Remaining seconds
    alert = pyqtSignal()  # Time to produce villager
    started = pyqtSignal()
    stopped = pyqtSignal()
    paused = pyqtSignal()
    resumed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._interval = DEFAULT_INTERVAL
        self._remaining = self._interval
        self._is_running = False
        self._is_paused = False
        self._alert_count = 0
        
        self._timer = QTimer(self)
        self._timer.setInterval(1000)  # 1 second
        self._timer.timeout.connect(self._on_tick)
    
    @property
    def interval(self) -> int:
        """Get timer interval in seconds."""
        return self._interval
    
    @interval.setter
    def interval(self, value: int):
        """Set timer interval in seconds."""
        self._interval = value
        if not self._is_running:
            self._remaining = value
    
    @property
    def remaining(self) -> int:
        """Get remaining seconds."""
        return self._remaining
    
    @property
    def is_running(self) -> bool:
        """Check if timer is running."""
        return self._is_running
    
    @property
    def is_paused(self) -> bool:
        """Check if timer is paused."""
        return self._is_paused
    
    @property
    def alert_count(self) -> int:
        """Get total alert count for current session."""
        return self._alert_count
    
    def start(self):
        """Start the timer."""
        if self._is_running and not self._is_paused:
            return
        
        if self._is_paused:
            # Resume from pause
            self._is_paused = False
            self._timer.start()
            self.resumed.emit()
        else:
            # Fresh start
            self._remaining = self._interval
            self._is_running = True
            self._is_paused = False
            self._alert_count = 0
            self._timer.start()
            self.started.emit()
        
        self.tick.emit(self._remaining)
    
    def stop(self):
        """Stop the timer completely."""
        self._timer.stop()
        self._is_running = False
        self._is_paused = False
        self._remaining = self._interval
        self.stopped.emit()
        self.tick.emit(self._remaining)
    
    def pause(self):
        """Pause the timer."""
        if self._is_running and not self._is_paused:
            self._timer.stop()
            self._is_paused = True
            self.paused.emit()
    
    def resume(self):
        """Resume from pause."""
        if self._is_paused:
            self._is_paused = False
            self._timer.start()
            self.resumed.emit()
    
    def toggle_pause(self):
        """Toggle between paused and running."""
        if self._is_paused:
            self.resume()
        elif self._is_running:
            self.pause()
    
    def reset(self):
        """Reset timer to initial interval without stopping."""
        self._remaining = self._interval
        self.tick.emit(self._remaining)
    
    def _on_tick(self):
        """Handle each second tick."""
        self._remaining -= 1
        self.tick.emit(self._remaining)
        
        if self._remaining <= 0:
            # Time's up - alert and reset
            self._alert_count += 1
            self.alert.emit()
            self._remaining = self._interval
            self.tick.emit(self._remaining)


