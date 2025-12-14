from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QMouseEvent


class OverlayWidget(QWidget):
    """
    Transparent in-game overlay widget.
    Shows timer in a minimal, always-on-top transparent window.
    Similar to Discord's overlay.
    """
    
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_position = QPoint()
        self._is_locked = False
        self._setup_window()
        self._setup_ui()
    
    def _setup_window(self):
        """Configure window for overlay behavior."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool  # Don't show in taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(180, 100)
        
        # Start position (top-right corner)
        screen = self.screen().availableGeometry()
        self.move(screen.width() - 200, 50)
    
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
        container_layout.setContentsMargins(15, 10, 15, 10)
        container_layout.setSpacing(5)
        
        # Header with close button
        header = QHBoxLayout()
        
        title = QLabel("Villager")
        title.setStyleSheet("color: rgba(255, 215, 0, 0.8); font-size: 11px; font-weight: bold; border: none; background: transparent;")
        header.addWidget(title)
        
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
        self._lock_btn.setToolTip("Konumu kilitle/aç")
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
        
        # Timer display
        self._timer_label = QLabel("25")
        self._timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._timer_label.setStyleSheet("""
            QLabel {
                color: #ffd700;
                font-size: 36px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
        """)
        container_layout.addWidget(self._timer_label)
        
        # Status
        self._status_label = QLabel("Hazır")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("""
            QLabel {
                color: rgba(176, 176, 176, 0.8);
                font-size: 10px;
                border: none;
                background: transparent;
            }
        """)
        container_layout.addWidget(self._status_label)
        
        layout.addWidget(self._container)
    
    def update_timer(self, seconds: int):
        """Update the timer display."""
        self._timer_label.setText(str(seconds))
        
        # Flash effect when low
        if seconds <= 3:
            self._timer_label.setStyleSheet("""
                QLabel {
                    color: #ff6b6b;
                    font-size: 36px;
                    font-weight: bold;
                    border: none;
                    background: transparent;
                }
            """)
        else:
            self._timer_label.setStyleSheet("""
                QLabel {
                    color: #ffd700;
                    font-size: 36px;
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
        if is_running:
            self._status_label.setText("Çalışıyor")
            self._container.setStyleSheet("""
                QWidget {
                    background-color: rgba(26, 26, 46, 0.9);
                    border-radius: 10px;
                    border: 1px solid rgba(45, 106, 79, 0.8);
                }
            """)
        else:
            self._status_label.setText("Durduruldu")
            self._container.setStyleSheet("""
                QWidget {
                    background-color: rgba(26, 26, 46, 0.85);
                    border-radius: 10px;
                    border: 1px solid rgba(255, 215, 0, 0.3);
                }
            """)
    
    def _toggle_lock(self):
        """Toggle position lock."""
        self._is_locked = not self._is_locked
        self._lock_btn.setText("🔒" if self._is_locked else "🔓")
    
    def _on_close(self):
        """Handle close button."""
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


