import os
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QSystemTrayIcon, QMenu, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QCloseEvent

from .styles import DARK_THEME
from .timer_panel import TimerPanel
from .settings_panel import SettingsPanel
from .statistics_panel import StatisticsPanel
from .overlay_widget import OverlayWidget
from ..services.game_detector import GameDetector
from ..services.timer_service import TimerService
from ..services.notification import NotificationService
from ..services.stats_tracker import StatsTracker
from ..utils.config import Config
from ..utils.constants import APP_NAME, APP_VERSION
from ..utils.localization import tr


class MainWindow(QMainWindow):
    """Main application window - compact and fixed size."""
    
    def __init__(self):
        super().__init__()
        self._config = Config()
        
        # Initialize services
        self._game_detector = GameDetector(self)
        self._timer_service = TimerService(self)
        self._notification_service = NotificationService(self)
        self._stats_tracker = StatsTracker(self)
        
        # Overlay window
        self._overlay = OverlayWidget()
        
        # Setup UI
        self._setup_window()
        self._setup_tray()
        self._setup_ui()
        self._connect_signals()
        self._apply_settings()
        
        # Auto-start detection if enabled
        if self._settings_panel.auto_start_enabled:
            self._game_detector.start_detection()
    
    def _setup_window(self):
        """Configure main window - fixed size, no resize."""
        self.setWindowTitle(f"{APP_NAME}")
        
        # Fixed size - no resizing allowed
        self.setFixedSize(380, 600)
        
        # Apply dark theme
        self.setStyleSheet(DARK_THEME)
        
        # Window icon
        icon_path = self._get_icon_path()
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        
        # Always on top if enabled
        if self._config.get("always_on_top"):
            self.setWindowFlags(
                self.windowFlags() | 
                Qt.WindowType.WindowStaysOnTopHint
            )
    
    def _get_icon_path(self) -> str:
        """Get the application icon path."""
        # Get project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        possible_paths = [
            os.path.join(project_root, 'app_icon.png'),  # Root directory
            os.path.join(project_root, 'assets', 'icons', 'app_icon.png'),  # Assets/icons
            os.path.join(getattr(sys, '_MEIPASS', ''), 'app_icon.png'),  # PyInstaller bundle
            os.path.join(getattr(sys, '_MEIPASS', ''), 'assets', 'icons', 'app_icon.png'),  # PyInstaller bundle assets
        ]
        for path in possible_paths:
            if path and os.path.exists(path):
                return path
        return ""
    
    def _setup_tray(self):
        """Setup system tray icon."""
        self._tray_icon = QSystemTrayIcon(self)
        
        icon_path = self._get_icon_path()
        if icon_path:
            self._tray_icon.setIcon(QIcon(icon_path))
        else:
            self._tray_icon.setIcon(self.style().standardIcon(
                self.style().StandardPixmap.SP_ComputerIcon
            ))
        
        # Tray menu
        self._tray_menu = QMenu()
        
        self._tray_show_action = QAction(tr("tray_show"), self)
        self._tray_show_action.triggered.connect(self.show_normal)
        self._tray_menu.addAction(self._tray_show_action)
        
        self._tray_menu.addSeparator()
        
        self._tray_overlay_action = QAction(tr("tray_overlay_toggle"), self)
        self._tray_overlay_action.triggered.connect(self._toggle_overlay)
        self._tray_menu.addAction(self._tray_overlay_action)
        
        self._tray_menu.addSeparator()
        
        self._tray_start_action = QAction(tr("tray_start"), self)
        self._tray_start_action.triggered.connect(self._on_start_clicked)
        self._tray_menu.addAction(self._tray_start_action)
        
        self._tray_stop_action = QAction(tr("tray_stop"), self)
        self._tray_stop_action.triggered.connect(self._on_stop_clicked)
        self._tray_menu.addAction(self._tray_stop_action)
        
        self._tray_menu.addSeparator()
        
        self._tray_quit_action = QAction(tr("tray_quit"), self)
        self._tray_quit_action.triggered.connect(self._quit_app)
        self._tray_menu.addAction(self._tray_quit_action)
        
        self._tray_icon.setContextMenu(self._tray_menu)
        self._tray_icon.activated.connect(self._on_tray_activated)
        self._tray_icon.show()
        
        self._notification_service.set_tray_icon(self._tray_icon)
    
    def _setup_ui(self):
        """Setup the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel(APP_NAME)
        title.setStyleSheet("color: #ffd700; font-size: 14px; font-weight: bold;")
        header.addWidget(title)
        
        header.addStretch()
        
        version = QLabel(f"v{APP_VERSION}")
        version.setStyleSheet("color: #666; font-size: 10px;")
        header.addWidget(version)
        
        main_layout.addLayout(header)
        
        # Tab widget
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3d3d5c;
                border-radius: 6px;
                background-color: #1a1a2e;
            }
            QTabBar::tab {
                background-color: #252542;
                color: #b0b0b0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 11px;
            }
            QTabBar::tab:selected {
                background-color: #3d3d5c;
                color: #ffd700;
            }
            QTabBar::tab:hover:!selected {
                background-color: #2d2d4a;
            }
        """)
        
        # Timer tab
        self._timer_panel = TimerPanel()
        self._tabs.addTab(self._timer_panel, "⏱ " + tr("tab_timer"))
        
        # Settings tab
        self._settings_panel = SettingsPanel()
        self._tabs.addTab(self._settings_panel, "⚙ " + tr("tab_settings"))
        
        # Statistics tab
        self._stats_panel = StatisticsPanel(self._stats_tracker)
        self._tabs.addTab(self._stats_panel, "📊 " + tr("tab_statistics"))
        
        main_layout.addWidget(self._tabs)
    
    def _connect_signals(self):
        """Connect all signals."""
        # Game detector
        self._game_detector.game_started.connect(self._on_game_started)
        self._game_detector.game_ended.connect(self._on_game_ended)
        self._game_detector.status_changed.connect(self._timer_panel.set_status)
        
        # Timer service
        self._timer_service.tick.connect(self._on_timer_tick)
        self._timer_service.alert.connect(self._on_timer_alert)
        self._timer_service.started.connect(lambda: self._on_timer_state_changed(True))
        self._timer_service.stopped.connect(lambda: self._on_timer_state_changed(False))
        self._timer_service.paused.connect(lambda: self._timer_panel.set_paused(True))
        self._timer_service.resumed.connect(lambda: self._timer_panel.set_paused(False))
        
        # Timer panel buttons
        self._timer_panel.start_btn.clicked.connect(self._on_start_clicked)
        self._timer_panel.pause_btn.clicked.connect(self._on_pause_clicked)
        self._timer_panel.stop_btn.clicked.connect(self._on_stop_clicked)
        self._timer_panel.overlay_btn.clicked.connect(self._toggle_overlay)
        
        # Settings panel
        self._settings_panel.interval_changed.connect(self._on_interval_changed)
        self._settings_panel.volume_changed.connect(self._on_volume_changed)
        self._settings_panel.detection_mode_changed.connect(self._on_detection_mode_changed)
        self._settings_panel.profile_id_changed.connect(self._on_profile_id_changed)
        self._settings_panel.sound_enabled_changed.connect(
            lambda v: setattr(self._notification_service, 'sound_enabled', v)
        )
        self._settings_panel.popup_enabled_changed.connect(
            lambda v: setattr(self._notification_service, 'popup_enabled', v)
        )
        self._settings_panel.always_on_top_changed.connect(self._on_always_on_top_changed)
        self._settings_panel.test_sound_requested.connect(self._notification_service.test_sound)
        self._settings_panel.test_popup_requested.connect(self._notification_service.test_popup)
        self._settings_panel.language_changed.connect(self._on_language_changed)
        
        # Overlay
        self._overlay.closed.connect(self._on_overlay_closed)
        self._overlay.start_clicked.connect(self._on_start_clicked)
        self._overlay.stop_clicked.connect(self._on_stop_clicked)
        
        # Connect pause/resume to overlay as well
        self._timer_service.paused.connect(lambda: self._overlay.set_paused(True))
        self._timer_service.resumed.connect(lambda: self._overlay.set_paused(False))
    
    def _apply_settings(self):
        """Apply settings from config."""
        self._timer_service.interval = self._config.get("interval", 25)
        self._notification_service.volume = self._config.get("volume", 70)
        self._notification_service.sound_enabled = self._config.get("sound_enabled", True)
        self._notification_service.popup_enabled = self._config.get("popup_enabled", False)
        
        self._game_detector.mode = self._config.get("detection_mode", "api")
        profile_id = self._config.get("profile_id")
        if profile_id:
            self._game_detector.profile_id = str(profile_id)
        
        # Update timer display
        self._timer_panel.update_timer(self._timer_service.interval, self._timer_service.interval)
        self._overlay.update_timer(self._timer_service.interval)
    
    def _on_start_clicked(self):
        """Handle start button."""
        if self._game_detector.mode == "manual":
            self._game_detector.manual_start()
        self._timer_service.start()
        self._stats_tracker.start_session()
    
    def _on_pause_clicked(self):
        """Handle pause button."""
        self._timer_service.toggle_pause()
    
    def _on_stop_clicked(self):
        """Handle stop button."""
        if self._game_detector.mode == "manual":
            self._game_detector.manual_stop()
        self._timer_service.stop()
        self._stats_tracker.end_session()
    
    def _on_game_started(self):
        """Handle game start detection."""
        # Auto-open overlay when match starts (if enabled)
        if self._settings_panel.auto_show_overlay_enabled and not self._overlay.isVisible():
            self._overlay.show()
            self._timer_panel.overlay_btn.setText(tr("btn_hide"))
        
        if self._settings_panel.auto_start_enabled:
            self._timer_service.start()
            self._stats_tracker.start_session()
    
    def _on_game_ended(self):
        """Handle game end detection."""
        self._timer_service.stop()
        self._stats_tracker.end_session()
    
    def _on_timer_tick(self, remaining: int):
        """Update displays on timer tick."""
        self._timer_panel.update_timer(remaining, self._timer_service.interval)
        self._overlay.update_timer(remaining)
    
    def _on_timer_alert(self):
        """Handle timer alert."""
        self._notification_service.notify()
        self._stats_tracker.record_alert()
        self._overlay.flash_alert()
    
    def _on_timer_state_changed(self, is_running: bool):
        """Handle timer start/stop."""
        self._timer_panel.update_button_states(is_running)
        self._overlay.set_running(is_running)
        
        if not is_running:
            # Reset display
            self._timer_panel.update_timer(self._timer_service.interval, self._timer_service.interval)
            self._overlay.update_timer(self._timer_service.interval)
    
    def _on_interval_changed(self, value: int):
        """Handle interval change."""
        self._timer_service.interval = value
        if not self._timer_service.is_running:
            self._timer_panel.update_timer(value, value)
            self._overlay.update_timer(value)
    
    def _on_volume_changed(self, value: int):
        """Handle volume change."""
        self._notification_service.volume = value
    
    def _on_detection_mode_changed(self, mode: str):
        """Handle detection mode change."""
        self._game_detector.mode = mode
    
    def _on_profile_id_changed(self, profile_id: str):
        """Handle profile ID change."""
        self._game_detector.profile_id = profile_id if profile_id else None
        # Restart detection if API mode is active
        if self._game_detector.mode == "api" and self._settings_panel.auto_start_enabled:
            if profile_id:
                # Stop current detection and restart with new profile ID
                was_detecting = self._game_detector.is_detecting
                if was_detecting:
                    self._game_detector.stop_detection()
                self._game_detector.start_detection()
    
    def _on_always_on_top_changed(self, enabled: bool):
        """Handle always on top change."""
        self._config.set("always_on_top", enabled)
        if enabled:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()
    
    def _on_language_changed(self, lang_code: str):
        """Handle language change - retranslate all UI."""
        self._retranslate_ui()
        self._timer_panel.retranslate_ui()
        self._settings_panel.retranslate_ui()
        self._stats_panel.retranslate_ui()
        self._overlay.retranslate_ui()
    
    def _retranslate_ui(self):
        """Retranslate main window UI strings."""
        # Update tab titles
        self._tabs.setTabText(0, "⏱ " + tr("tab_timer"))
        self._tabs.setTabText(1, "⚙ " + tr("tab_settings"))
        self._tabs.setTabText(2, "📊 " + tr("tab_statistics"))
        
        # Update tray menu
        self._tray_show_action.setText(tr("tray_show"))
        self._tray_overlay_action.setText(tr("tray_overlay_toggle"))
        self._tray_start_action.setText(tr("tray_start"))
        self._tray_stop_action.setText(tr("tray_stop"))
        self._tray_quit_action.setText(tr("tray_quit"))
    
    def _toggle_overlay(self):
        """Toggle overlay visibility."""
        if self._overlay.isVisible():
            self._overlay.hide()
            self._timer_panel.overlay_btn.setText(tr("btn_show"))
        else:
            self._overlay.show()
            self._timer_panel.overlay_btn.setText(tr("btn_hide"))
    
    def _on_overlay_closed(self):
        """Handle overlay close."""
        self._timer_panel.overlay_btn.setText(tr("btn_show"))
    
    def _on_tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_normal()
    
    def show_normal(self):
        """Show and activate window."""
        self.showNormal()
        self.activateWindow()
        self.raise_()
    
    def closeEvent(self, event: QCloseEvent):
        """Handle close - minimize to tray."""
        if self._tray_icon.isVisible():
            self.hide()
            self._tray_icon.showMessage(
                APP_NAME,
                tr("running_in_background"),
                QSystemTrayIcon.MessageIcon.Information,
                1500
            )
            event.ignore()
        else:
            self._quit_app()
    
    def _quit_app(self):
        """Quit application properly."""
        self._game_detector.stop_detection()
        self._timer_service.stop()
        self._stats_tracker.end_session()
        self._overlay.close()
        self._tray_icon.hide()
        QApplication.quit()
