from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QMouseEvent

from ..utils.localization import tr
from ..utils.config import Config


class OverlayWidget(QWidget):
    """
    Transparent in-game overlay widget.
    Shows timer in a minimal, always-on-top transparent window.
    Similar to Discord's overlay.
    """
    
    closed = pyqtSignal()
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_position = QPoint()
        self._is_locked = False
        self._config = Config()
        self._setup_window()
        self._setup_ui()
        self._restore_position()
    
    def _setup_window(self):
        """Configure window for overlay behavior."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool  # Don't show in taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(150, 95)
    
    def _restore_position(self):
        """Restore saved position or use default."""
        screen = self.screen().availableGeometry()
        default_x = screen.width() - 180
        default_y = 50
        
        x = self._config.get("overlay_x", default_x)
        y = self._config.get("overlay_y", default_y)
        
        # Ensure position is within screen bounds
        x = max(0, min(x, screen.width() - self.width()))
        y = max(0, min(y, screen.height() - self.height()))
        
        self.move(x, y)
    
    def _save_position(self):
        """Save current position to config."""
        pos = self.pos()
        self._config.set("overlay_x", pos.x())
        self._config.set("overlay_y", pos.y())
    
    def _setup_ui(self):
        """Setup the overlay UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main container with semi-transparent background
        self._container = QWidget()
        self._container.setStyleSheet("""
            QWidget {
                background-color: rgba(26, 26, 46, 0.85);
                border-radius: 10px;
                border: 1px solid rgba(255, 215, 0, 0.3);
            }
        """)
        
        container_layout = QVBoxLayout(self._container)
        container_layout.setContentsMargins(10, 8, 10, 8)
        container_layout.setSpacing(4)
        
        # Header with close button
        header = QHBoxLayout()
        
        self._title = QLabel(tr("overlay_title"))
        self._title.setStyleSheet("color: rgba(255, 215, 0, 0.8); font-size: 11px; font-weight: bold; border: none; background: transparent;")
        header.addWidget(self._title)
        
        header.addStretch()
        
        # Lock button
        self._lock_btn = QPushButton("🔓")
        self._lock_btn.setFixedSize(20, 20)
        self._lock_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 12px;
                color: #b0b0b0;
            }
            QPushButton:hover {
                color: #ffd700;
            }
        """)
        self._lock_btn.clicked.connect(self._toggle_lock)
        self._lock_btn.setToolTip(tr("overlay_lock_tooltip"))
        header.addWidget(self._lock_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 14px;
                color: #b0b0b0;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        close_btn.clicked.connect(self._on_close)
        header.addWidget(close_btn)
        
        container_layout.addLayout(header)
        
        # Main content: Timer on left, buttons on right
        content = QHBoxLayout()
        content.setSpacing(6)
        
        # Left side: Timer and status
        timer_section = QVBoxLayout()
        timer_section.setSpacing(2)
        
        self._timer_label = QLabel("25")
        self._timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._timer_label.setStyleSheet("""
            QLabel {
                color: #ffd700;
                font-size: 32px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
        """)
        timer_section.addWidget(self._timer_label)
        
        self._status_label = QLabel(tr("timer_ready"))
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("""
            QLabel {
                color: rgba(176, 176, 176, 0.8);
                font-size: 10px;
                border: none;
                background: transparent;
            }
        """)
        timer_section.addWidget(self._status_label)
        
        content.addLayout(timer_section)
        
        # Right side: Control buttons (vertical)
        controls = QVBoxLayout()
        controls.setSpacing(3)
        
        self._start_btn = QPushButton("▶")
        self._start_btn.setFixedSize(24, 20)
        self._start_btn.setFlat(True)
        self._start_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: rgba(220, 220, 220, 0.9);
                font-size: 12px;
            }
            QPushButton:hover {
                color: rgba(255, 255, 255, 1.0);
                background: transparent;
            }
            QPushButton:disabled {
                color: rgba(100, 100, 100, 0.5);
                background: transparent;
            }
            QPushButton:pressed {
                background: transparent;
            }
        """)
        self._start_btn.setToolTip(tr("btn_start"))
        self._start_btn.clicked.connect(self.start_clicked.emit)
        controls.addWidget(self._start_btn)
        
        self._stop_btn = QPushButton("⏹")
        self._stop_btn.setFixedSize(24, 20)
        self._stop_btn.setFlat(True)
        self._stop_btn.setEnabled(False)
        self._stop_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: rgba(220, 220, 220, 0.9);
                font-size: 12px;
            }
            QPushButton:hover {
                color: rgba(255, 255, 255, 1.0);
                background: transparent;
            }
            QPushButton:disabled {
                color: rgba(100, 100, 100, 0.5);
                background: transparent;
            }
            QPushButton:pressed {
                background: transparent;
            }
        """)
        self._stop_btn.setToolTip(tr("btn_stop"))
        self._stop_btn.clicked.connect(self.stop_clicked.emit)
        controls.addWidget(self._stop_btn)
        
        content.addLayout(controls)
        
        container_layout.addLayout(content)
        
        layout.addWidget(self._container)
    
    def update_timer(self, seconds: int):
        """Update the timer display."""
        self._timer_label.setText(str(seconds))
        
        # Flash effect when low
        if seconds <= 3:
            self._timer_label.setStyleSheet("""
                QLabel {
                    color: #ff6b6b;
                    font-size: 32px;
                    font-weight: bold;
                    border: none;
                    background: transparent;
                }
            """)
        else:
            self._timer_label.setStyleSheet("""
                QLabel {
                    color: #ffd700;
                    font-size: 32px;
                    font-weight: bold;
                    border: none;
                    background: transparent;
                }
            """)
    
    def set_status(self, status: str):
        """Update status text."""
        self._status_label.setText(status)
    
    def set_running(self, is_running: bool):
        """Update visual state based on timer running."""
        # Play button: enabled when not running (to start or resume)
        # Stop button: enabled when running (to stop)
        self._start_btn.setEnabled(not is_running)
        self._stop_btn.setEnabled(is_running)
        
        if is_running:
            self._status_label.setText(tr("timer_running"))
            self._container.setStyleSheet("""
                QWidget {
                    background-color: rgba(26, 26, 46, 0.9);
                    border-radius: 10px;
                    border: 1px solid rgba(45, 106, 79, 0.8);
                }
            """)
        else:
            self._status_label.setText(tr("timer_stopped"))
            self._container.setStyleSheet("""
                QWidget {
                    background-color: rgba(26, 26, 46, 0.85);
                    border-radius: 10px;
                    border: 1px solid rgba(255, 215, 0, 0.3);
                }
            """)
    
    def set_paused(self, is_paused: bool):
        """Update visual state when paused."""
        if is_paused:
            # When paused: play button enabled (to resume), stop button enabled (to stop)
            self._start_btn.setEnabled(True)
            self._stop_btn.setEnabled(True)
            self._status_label.setText(tr("timer_paused"))
        else:
            # When running: play button disabled, stop button enabled
            self._start_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)
            self._status_label.setText(tr("timer_running"))
    
    def _toggle_lock(self):
        """Toggle position lock."""
        self._is_locked = not self._is_locked
        self._lock_btn.setText("🔒" if self._is_locked else "🔓")
    
    def _on_close(self):
        """Handle close button."""
        self._save_position()
        self.hide()
        self.closed.emit()
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for dragging."""
        if event.button() == Qt.MouseButton.LeftButton and not self._is_locked:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for dragging."""
        if event.buttons() == Qt.MouseButton.LeftButton and not self._is_locked:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release - save position after dragging."""
        if event.button() == Qt.MouseButton.LeftButton and not self._is_locked:
            self._save_position()
            event.accept()
    
    def flash_alert(self):
        """Flash the overlay when alert triggers."""
        original_style = self._container.styleSheet()
        self._container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 107, 107, 0.9);
                border-radius: 10px;
                border: 2px solid #ff6b6b;
            }
        """)
        
        # Reset after delay
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(200, lambda: self._container.setStyleSheet(original_style))
    
    def retranslate_ui(self):
        """Retranslate all UI strings (called when language changes)."""
        self._title.setText(tr("overlay_title"))
        self._lock_btn.setToolTip(tr("overlay_lock_tooltip"))
        self._status_label.setText(tr("timer_ready"))
        self._start_btn.setToolTip(tr("btn_start"))
        self._stop_btn.setToolTip(tr("btn_stop"))
