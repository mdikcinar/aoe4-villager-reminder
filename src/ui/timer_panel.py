from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt

from ..utils.localization import tr


class TimerPanel(QWidget):
    """Timer display panel for the main window."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Timer display container
        timer_container = QFrame()
        timer_container.setStyleSheet("""
            QFrame {
                background-color: #252542;
                border-radius: 12px;
            }
        """)
        
        timer_layout = QVBoxLayout(timer_container)
        timer_layout.setContentsMargins(20, 25, 20, 25)
        timer_layout.setSpacing(10)
        timer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Timer label
        self.timer_label = QLabel("25")
        self.timer_label.setStyleSheet("""
            QLabel {
                color: #ffd700;
                font-size: 72px;
                font-weight: bold;
            }
        """)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #1a1a2e;
            }
            QProgressBar::chunk {
                background-color: #ffd700;
                border-radius: 4px;
            }
        """)
        timer_layout.addWidget(self.progress_bar)
        
        # Subtitle
        self._subtitle = QLabel(tr("timer_seconds"))
        self._subtitle.setStyleSheet("color: #b0b0b0; font-size: 13px;")
        self._subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self._subtitle)
        
        layout.addWidget(timer_container)
        
        # Control buttons
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)
        
        self.start_btn = QPushButton(tr("btn_start"))
        self.start_btn.setObjectName("startButton")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d6a4f;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #40916c;
            }
            QPushButton:disabled {
                background-color: #1b4332;
                color: #666;
            }
        """)
        controls_layout.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton(tr("btn_pause"))
        self.pause_btn.setEnabled(False)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d5c;
                color: #eaeaea;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4d4d6c;
            }
            QPushButton:disabled {
                background-color: #252542;
                color: #666;
            }
        """)
        controls_layout.addWidget(self.pause_btn)
        
        self.stop_btn = QPushButton(tr("btn_stop"))
        self.stop_btn.setObjectName("stopButton")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #9d0208;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #d00000;
            }
            QPushButton:disabled {
                background-color: #4a0104;
                color: #666;
            }
        """)
        controls_layout.addWidget(self.stop_btn)
        
        layout.addWidget(controls)
        
        # Status label
        self.status_label = QLabel(tr("timer_ready"))
        self.status_label.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Spacer
        layout.addStretch()
        
        # Overlay toggle
        overlay_container = QFrame()
        overlay_container.setStyleSheet("""
            QFrame {
                background-color: #252542;
                border-radius: 8px;
            }
        """)
        overlay_layout = QHBoxLayout(overlay_container)
        overlay_layout.setContentsMargins(15, 12, 15, 12)
        
        self._overlay_label = QLabel(tr("overlay_ingame"))
        self._overlay_label.setStyleSheet("color: #eaeaea; font-size: 12px;")
        overlay_layout.addWidget(self._overlay_label)
        
        overlay_layout.addStretch()
        
        self.overlay_btn = QPushButton(tr("btn_show"))
        self.overlay_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d5c;
                color: #ffd700;
                border: none;
                padding: 6px 16px;
                border-radius: 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #4d4d6c;
            }
        """)
        overlay_layout.addWidget(self.overlay_btn)
        
        layout.addWidget(overlay_container)
    
    def update_timer(self, seconds: int, interval: int):
        """Update timer display."""
        self.timer_label.setText(str(seconds))
        progress = (seconds / interval) * 100 if interval > 0 else 100
        self.progress_bar.setValue(int(progress))
        
        # Color change when low
        if seconds <= 3:
            self.timer_label.setStyleSheet("""
                QLabel {
                    color: #ff6b6b;
                    font-size: 72px;
                    font-weight: bold;
                }
            """)
        else:
            self.timer_label.setStyleSheet("""
                QLabel {
                    color: #ffd700;
                    font-size: 72px;
                    font-weight: bold;
                }
            """)
    
    def set_status(self, message: str):
        """Update status message."""
        self.status_label.setText(message)
    
    def update_button_states(self, is_running: bool):
        """Update button enabled states."""
        self.start_btn.setEnabled(not is_running)
        self.pause_btn.setEnabled(is_running)
        self.stop_btn.setEnabled(is_running)
        self.pause_btn.setText(tr("btn_pause"))
    
    def set_paused(self, is_paused: bool):
        """Update pause button text."""
        self.pause_btn.setText(tr("btn_resume") if is_paused else tr("btn_pause"))
    
    def retranslate_ui(self):
        """Retranslate all UI strings (called when language changes)."""
        self._subtitle.setText(tr("timer_seconds"))
        self.start_btn.setText(tr("btn_start"))
        self.pause_btn.setText(tr("btn_pause"))
        self.stop_btn.setText(tr("btn_stop"))
        self.status_label.setText(tr("timer_ready"))
        self._overlay_label.setText(tr("overlay_ingame"))
        self.overlay_btn.setText(tr("btn_show"))
