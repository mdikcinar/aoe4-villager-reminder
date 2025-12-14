import os
import sys
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QSystemTrayIcon, QApplication
from typing import Optional

# Initialize pygame mixer for sound
import pygame
pygame.mixer.init()


class NotificationService(QObject):
    """Handles sound and popup notifications."""
    
    notification_sent = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._volume = 70  # 0-100
        self._sound_enabled = True
        self._popup_enabled = True
        self._sound_file: Optional[str] = None
        self._tray_icon: Optional[QSystemTrayIcon] = None
        
        # Load default sound
        self._load_default_sound()
    
    def _load_default_sound(self):
        """Load the default alert sound."""
        # Try to find the sound file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'sounds', 'villager.wav'),
            os.path.join(getattr(sys, '_MEIPASS', ''), 'assets', 'sounds', 'villager.wav'),
            'assets/sounds/villager.wav',
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self._sound_file = os.path.abspath(path)
                break
    
    @property
    def volume(self) -> int:
        return self._volume
    
    @volume.setter
    def volume(self, value: int):
        self._volume = max(0, min(100, value))
    
    @property
    def sound_enabled(self) -> bool:
        return self._sound_enabled
    
    @sound_enabled.setter
    def sound_enabled(self, value: bool):
        self._sound_enabled = value
    
    @property
    def popup_enabled(self) -> bool:
        return self._popup_enabled
    
    @popup_enabled.setter
    def popup_enabled(self, value: bool):
        self._popup_enabled = value
    
    def set_tray_icon(self, tray_icon: QSystemTrayIcon):
        """Set the system tray icon for popup notifications."""
        self._tray_icon = tray_icon
    
    def set_sound_file(self, path: str):
        """Set a custom sound file."""
        if os.path.exists(path):
            self._sound_file = path
    
    def notify(self, title: str = "Villager Üret!", message: str = "Köylü üretme zamanı!"):
        """Send notification (sound and/or popup)."""
        if self._sound_enabled:
            self._play_sound()
        
        if self._popup_enabled:
            self._show_popup(title, message)
        
        self.notification_sent.emit()
    
    def _play_sound(self):
        """Play the alert sound."""
        try:
            if self._sound_file and os.path.exists(self._sound_file):
                pygame.mixer.music.load(self._sound_file)
                pygame.mixer.music.set_volume(self._volume / 100.0)
                pygame.mixer.music.play()
            else:
                # Fallback: system beep
                QApplication.beep()
        except Exception as e:
            print(f"Sound error: {e}")
            QApplication.beep()
    
    def _show_popup(self, title: str, message: str):
        """Show a popup notification."""
        if self._tray_icon and self._tray_icon.isVisible():
            self._tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                2000  # Duration in ms
            )
    
    def test_sound(self):
        """Play a test sound."""
        self._play_sound()
    
    def test_popup(self):
        """Show a test popup."""
        self._show_popup("Test", "Bu bir test bildirimidir!")


