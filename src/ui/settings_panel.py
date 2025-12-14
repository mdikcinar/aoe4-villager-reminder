from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSlider, QCheckBox, QComboBox, QLineEdit,
    QGroupBox, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from ..utils.constants import (
    MIN_INTERVAL, MAX_INTERVAL, DEFAULT_INTERVAL,
    DETECTION_MODE_PROCESS, DETECTION_MODE_API, DETECTION_MODE_MANUAL
)
from ..utils.config import Config


class SettingsPanel(QWidget):
    """Compact settings panel."""
    
    # Signals
    interval_changed = pyqtSignal(int)
    volume_changed = pyqtSignal(int)
    detection_mode_changed = pyqtSignal(str)
    profile_id_changed = pyqtSignal(str)
    sound_enabled_changed = pyqtSignal(bool)
    popup_enabled_changed = pyqtSignal(bool)
    always_on_top_changed = pyqtSignal(bool)
    test_sound_requested = pyqtSignal()
    test_popup_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._config = Config()
        self._setup_ui()
        self._load_settings()
        self._connect_signals()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        
        # Timer Settings
        timer_group = QGroupBox("Zamanlayıcı")
        timer_group.setStyleSheet("QGroupBox { font-size: 11px; }")
        timer_layout = QVBoxLayout(timer_group)
        timer_layout.setSpacing(8)
        
        # Interval
        interval_row = QHBoxLayout()
        interval_row.addWidget(QLabel("Aralık:"))
        
        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setRange(MIN_INTERVAL, MAX_INTERVAL)
        self.interval_slider.setValue(DEFAULT_INTERVAL)
        interval_row.addWidget(self.interval_slider)
        
        self.interval_label = QLabel(f"{DEFAULT_INTERVAL}s")
        self.interval_label.setMinimumWidth(35)
        self.interval_label.setStyleSheet("color: #ffd700;")
        interval_row.addWidget(self.interval_label)
        
        timer_layout.addLayout(interval_row)
        
        # Quick presets
        preset_row = QHBoxLayout()
        for seconds in [20, 25, 30, 35]:
            btn = QPushButton(f"{seconds}")
            btn.setFixedSize(40, 24)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3d3d5c;
                    border: none;
                    border-radius: 4px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #4d4d6c;
                }
            """)
            btn.clicked.connect(lambda checked, s=seconds: self._set_interval(s))
            preset_row.addWidget(btn)
        preset_row.addStretch()
        timer_layout.addLayout(preset_row)
        
        layout.addWidget(timer_group)
        
        # Detection Settings
        detection_group = QGroupBox("Oyun Algılama")
        detection_group.setStyleSheet("QGroupBox { font-size: 11px; }")
        detection_layout = QVBoxLayout(detection_group)
        detection_layout.setSpacing(8)
        
        # Mode combo
        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Yöntem:"))
        
        self.detection_combo = QComboBox()
        self.detection_combo.setFixedHeight(28)
        self.detection_combo.addItem("Process", DETECTION_MODE_PROCESS)
        self.detection_combo.addItem("API", DETECTION_MODE_API)
        self.detection_combo.addItem("Manuel", DETECTION_MODE_MANUAL)
        mode_row.addWidget(self.detection_combo)
        mode_row.addStretch()
        
        detection_layout.addLayout(mode_row)
        
        # Profile ID (for API mode)
        self.profile_row = QWidget()
        profile_layout = QHBoxLayout(self.profile_row)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.addWidget(QLabel("Profile ID:"))
        
        self.profile_input = QLineEdit()
        self.profile_input.setPlaceholderText("aoe4world.com ID")
        self.profile_input.setFixedHeight(26)
        self.profile_input.setMaximumWidth(120)
        profile_layout.addWidget(self.profile_input)
        profile_layout.addStretch()
        
        detection_layout.addWidget(self.profile_row)
        self.profile_row.setVisible(False)
        
        layout.addWidget(detection_group)
        
        # Notification Settings
        notif_group = QGroupBox("Bildirimler")
        notif_group.setStyleSheet("QGroupBox { font-size: 11px; }")
        notif_layout = QVBoxLayout(notif_group)
        notif_layout.setSpacing(8)
        
        # Sound row
        sound_row = QHBoxLayout()
        
        self.sound_checkbox = QCheckBox("Ses")
        self.sound_checkbox.setChecked(True)
        sound_row.addWidget(self.sound_checkbox)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(80)
        sound_row.addWidget(self.volume_slider)
        
        self.volume_label = QLabel("70%")
        self.volume_label.setMinimumWidth(35)
        sound_row.addWidget(self.volume_label)
        
        self.test_sound_btn = QPushButton("Test")
        self.test_sound_btn.setFixedSize(45, 24)
        self.test_sound_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d5c;
                border: none;
                border-radius: 4px;
                font-size: 10px;
            }
            QPushButton:hover { background-color: #4d4d6c; }
        """)
        sound_row.addWidget(self.test_sound_btn)
        sound_row.addStretch()
        
        notif_layout.addLayout(sound_row)
        
        # Popup row
        popup_row = QHBoxLayout()
        
        self.popup_checkbox = QCheckBox("Popup bildirimi")
        self.popup_checkbox.setChecked(True)
        popup_row.addWidget(self.popup_checkbox)
        
        self.test_popup_btn = QPushButton("Test")
        self.test_popup_btn.setFixedSize(45, 24)
        self.test_popup_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d5c;
                border: none;
                border-radius: 4px;
                font-size: 10px;
            }
            QPushButton:hover { background-color: #4d4d6c; }
        """)
        popup_row.addWidget(self.test_popup_btn)
        popup_row.addStretch()
        
        notif_layout.addLayout(popup_row)
        
        layout.addWidget(notif_group)
        
        # UI Settings
        ui_group = QGroupBox("Arayüz")
        ui_group.setStyleSheet("QGroupBox { font-size: 11px; }")
        ui_layout = QVBoxLayout(ui_group)
        ui_layout.setSpacing(6)
        
        self.always_on_top_checkbox = QCheckBox("Her zaman üstte")
        ui_layout.addWidget(self.always_on_top_checkbox)
        
        self.auto_start_checkbox = QCheckBox("Otomatik başla")
        self.auto_start_checkbox.setChecked(True)
        self.auto_start_checkbox.setToolTip("Oyun algılandığında timer otomatik başlasın")
        ui_layout.addWidget(self.auto_start_checkbox)
        
        layout.addWidget(ui_group)
        
        layout.addStretch()
    
    def _connect_signals(self):
        self.interval_slider.valueChanged.connect(self._on_interval_changed)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        self.detection_combo.currentIndexChanged.connect(self._on_detection_mode_changed)
        self.profile_input.textChanged.connect(self._on_profile_id_changed)
        
        self.sound_checkbox.stateChanged.connect(
            lambda state: self.sound_enabled_changed.emit(state == Qt.CheckState.Checked.value)
        )
        self.popup_checkbox.stateChanged.connect(
            lambda state: self.popup_enabled_changed.emit(state == Qt.CheckState.Checked.value)
        )
        self.always_on_top_checkbox.stateChanged.connect(
            lambda state: self.always_on_top_changed.emit(state == Qt.CheckState.Checked.value)
        )
        
        self.test_sound_btn.clicked.connect(self.test_sound_requested.emit)
        self.test_popup_btn.clicked.connect(self.test_popup_requested.emit)
    
    def _load_settings(self):
        self.interval_slider.setValue(self._config.get("interval", DEFAULT_INTERVAL))
        self.volume_slider.setValue(self._config.get("volume", 70))
        
        mode = self._config.get("detection_mode", DETECTION_MODE_PROCESS)
        index = self.detection_combo.findData(mode)
        if index >= 0:
            self.detection_combo.setCurrentIndex(index)
        
        profile_id = self._config.get("profile_id")
        if profile_id:
            self.profile_input.setText(str(profile_id))
        
        self.sound_checkbox.setChecked(self._config.get("sound_enabled", True))
        self.popup_checkbox.setChecked(self._config.get("popup_enabled", True))
        self.always_on_top_checkbox.setChecked(self._config.get("always_on_top", False))
        self.auto_start_checkbox.setChecked(self._config.get("auto_start_detection", True))
        
        self._update_profile_visibility()
    
    def _set_interval(self, seconds: int):
        self.interval_slider.setValue(seconds)
    
    def _on_interval_changed(self, value: int):
        self.interval_label.setText(f"{value}s")
        self._config.set("interval", value)
        self.interval_changed.emit(value)
    
    def _on_volume_changed(self, value: int):
        self.volume_label.setText(f"{value}%")
        self._config.set("volume", value)
        self.volume_changed.emit(value)
    
    def _on_detection_mode_changed(self, index: int):
        mode = self.detection_combo.currentData()
        self._config.set("detection_mode", mode)
        self.detection_mode_changed.emit(mode)
        self._update_profile_visibility()
    
    def _on_profile_id_changed(self, text: str):
        self._config.set("profile_id", text if text else None)
        self.profile_id_changed.emit(text)
    
    def _update_profile_visibility(self):
        mode = self.detection_combo.currentData()
        self.profile_row.setVisible(mode == DETECTION_MODE_API)
    
    @property
    def auto_start_enabled(self) -> bool:
        return self.auto_start_checkbox.isChecked()
