from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QGridLayout, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from ..services.stats_tracker import StatsTracker
from ..utils.localization import tr


class StatCard(QFrame):
    """Compact stat card."""
    
    def __init__(self, title: str, value: str = "0", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            StatCard {
                background-color: #252542;
                border-radius: 6px;
            }
        """)
        self.setFixedHeight(60)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffd700;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 10px; color: #b0b0b0;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
    
    def set_value(self, value: str):
        self.value_label.setText(value)


class StatisticsPanel(QWidget):
    """Compact statistics panel."""
    
    def __init__(self, stats_tracker: StatsTracker, parent=None):
        super().__init__(parent)
        self._stats = stats_tracker
        self._setup_ui()
        self._connect_signals()
        self._update_stats()
        
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._update_session_stats)
        self._refresh_timer.start(1000)
    
    def retranslate_ui(self):
        """Retranslate all UI strings (called when language changes)."""
        # Update group titles
        self.session_group.setTitle(tr("stats_current_session"))
        self.today_group.setTitle(tr("stats_today"))
        self.alltime_group.setTitle(tr("stats_all_time"))
        
        # Update stat card titles
        self.session_alerts_card.title_label.setText(tr("stats_alert"))
        self.session_duration_card.title_label.setText(tr("stats_duration"))
        self.today_alerts_card.title_label.setText(tr("stats_alert"))
        self.today_time_card.title_label.setText(tr("stats_duration"))
        self.today_sessions_card.title_label.setText(tr("stats_session_count"))
        self.total_alerts_card.title_label.setText(tr("stats_alert"))
        self.total_time_card.title_label.setText(tr("stats_duration"))
        self.avg_alerts_card.title_label.setText(tr("stats_avg_per_session"))
        
        # Update button
        self.reset_btn.setText(tr("btn_reset"))
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        
        # Current Session
        self.session_group = QGroupBox(tr("stats_current_session"))
        self.session_group.setStyleSheet("QGroupBox { font-size: 11px; }")
        session_layout = QHBoxLayout(self.session_group)
        session_layout.setSpacing(8)
        
        self.session_alerts_card = StatCard(tr("stats_alert"))
        session_layout.addWidget(self.session_alerts_card)
        
        self.session_duration_card = StatCard(tr("stats_duration"))
        session_layout.addWidget(self.session_duration_card)
        
        layout.addWidget(self.session_group)
        
        # Today
        self.today_group = QGroupBox(tr("stats_today"))
        self.today_group.setStyleSheet("QGroupBox { font-size: 11px; }")
        today_layout = QHBoxLayout(self.today_group)
        today_layout.setSpacing(8)
        
        self.today_alerts_card = StatCard(tr("stats_alert"))
        today_layout.addWidget(self.today_alerts_card)
        
        self.today_time_card = StatCard(tr("stats_duration"))
        today_layout.addWidget(self.today_time_card)
        
        self.today_sessions_card = StatCard(tr("stats_session_count"))
        today_layout.addWidget(self.today_sessions_card)
        
        layout.addWidget(self.today_group)
        
        # All Time
        self.alltime_group = QGroupBox(tr("stats_all_time"))
        self.alltime_group.setStyleSheet("QGroupBox { font-size: 11px; }")
        alltime_layout = QHBoxLayout(self.alltime_group)
        alltime_layout.setSpacing(8)
        
        self.total_alerts_card = StatCard(tr("stats_alert"))
        alltime_layout.addWidget(self.total_alerts_card)
        
        self.total_time_card = StatCard(tr("stats_duration"))
        alltime_layout.addWidget(self.total_time_card)
        
        self.avg_alerts_card = StatCard(tr("stats_avg_per_session"))
        alltime_layout.addWidget(self.avg_alerts_card)
        
        layout.addWidget(self.alltime_group)
        
        layout.addStretch()
        
        # Reset button
        reset_layout = QHBoxLayout()
        reset_layout.addStretch()
        
        self.reset_btn = QPushButton(tr("btn_reset"))
        self.reset_btn.setFixedSize(90, 28)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6a040f;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #9d0208;
            }
        """)
        reset_layout.addWidget(self.reset_btn)
        
        layout.addLayout(reset_layout)
    
    def _connect_signals(self):
        self._stats.stats_updated.connect(self._update_stats)
        self.reset_btn.clicked.connect(self._on_reset_clicked)
    
    def _update_stats(self):
        # Today
        today = self._stats.get_today_stats()
        self.today_alerts_card.set_value(str(today.get("alerts", 0)))
        self.today_time_card.set_value(self._format_short(today.get("time_seconds", 0)))
        self.today_sessions_card.set_value(str(today.get("sessions", 0)))
        
        # All time
        self.total_alerts_card.set_value(str(self._stats.total_alerts))
        self.total_time_card.set_value(self._format_short(self._stats.total_game_time))
        self.avg_alerts_card.set_value(f"{self._stats.get_average_alerts_per_session():.1f}")
    
    def _update_session_stats(self):
        self.session_alerts_card.set_value(str(self._stats.session_alerts))
        
        duration = self._stats.current_session_duration
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        self.session_duration_card.set_value(f"{minutes}:{seconds:02d}")
    
    def _format_short(self, seconds: float) -> str:
        """Short time format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if hours > 0:
            return f"{hours}{tr('time_format_short_hours')}{minutes}{tr('time_format_short_minutes')}"
        else:
            return f"{minutes}{tr('time_format_short_minutes')}"
    
    def _on_reset_clicked(self):
        reply = QMessageBox.question(
            self,
            tr("stats_reset_title"),
            tr("stats_reset_message"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self._stats.reset_all_stats()
