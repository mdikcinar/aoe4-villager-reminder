# Modern Dark Theme for AoE4 Villager Reminder
# Inspired by Age of Empires 4 UI

DARK_THEME = """
/* Main Application */
QMainWindow, QWidget {
    background-color: #1a1a2e;
    color: #eaeaea;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #3d3d5c;
    background-color: #1a1a2e;
    border-radius: 8px;
}

QTabBar::tab {
    background-color: #252542;
    color: #b0b0b0;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #3d3d5c;
    color: #ffd700;
}

QTabBar::tab:hover:!selected {
    background-color: #2d2d4a;
}

/* Buttons */
QPushButton {
    background-color: #3d3d5c;
    color: #eaeaea;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #4d4d6c;
}

QPushButton:pressed {
    background-color: #2d2d4a;
}

QPushButton:disabled {
    background-color: #252542;
    color: #666;
}

/* Primary Button (Start) */
QPushButton#startButton {
    background-color: #2d6a4f;
    color: #ffffff;
    font-size: 16px;
    padding: 15px 40px;
}

QPushButton#startButton:hover {
    background-color: #40916c;
}

QPushButton#startButton:pressed {
    background-color: #1b4332;
}

/* Stop Button */
QPushButton#stopButton {
    background-color: #9d0208;
    color: #ffffff;
    font-size: 16px;
    padding: 15px 40px;
}

QPushButton#stopButton:hover {
    background-color: #d00000;
}

QPushButton#stopButton:pressed {
    background-color: #6a040f;
}

/* Labels */
QLabel {
    color: #eaeaea;
}

QLabel#timerLabel {
    font-size: 72px;
    font-weight: bold;
    color: #ffd700;
}

QLabel#statusLabel {
    font-size: 14px;
    color: #b0b0b0;
}

QLabel#titleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #ffd700;
}

/* Sliders */
QSlider::groove:horizontal {
    border: 1px solid #3d3d5c;
    height: 8px;
    background: #252542;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #ffd700;
    border: none;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #ffed4a;
}

QSlider::sub-page:horizontal {
    background: #3d3d5c;
    border-radius: 4px;
}

/* Checkboxes */
QCheckBox {
    spacing: 8px;
    color: #eaeaea;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid #3d3d5c;
    background-color: #252542;
}

QCheckBox::indicator:checked {
    background-color: #ffd700;
    border-color: #ffd700;
}

QCheckBox::indicator:hover {
    border-color: #ffd700;
}

/* Combo Box */
QComboBox {
    background-color: #252542;
    border: 1px solid #3d3d5c;
    border-radius: 6px;
    padding: 8px 12px;
    color: #eaeaea;
    min-width: 150px;
}

QComboBox:hover {
    border-color: #ffd700;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #ffd700;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #252542;
    border: 1px solid #3d3d5c;
    selection-background-color: #3d3d5c;
    color: #eaeaea;
}

/* Line Edit */
QLineEdit {
    background-color: #252542;
    border: 1px solid #3d3d5c;
    border-radius: 6px;
    padding: 8px 12px;
    color: #eaeaea;
}

QLineEdit:focus {
    border-color: #ffd700;
}

/* Spin Box */
QSpinBox {
    background-color: #252542;
    border: 1px solid #3d3d5c;
    border-radius: 6px;
    padding: 8px 12px;
    color: #eaeaea;
}

QSpinBox:focus {
    border-color: #ffd700;
}

QSpinBox::up-button, QSpinBox::down-button {
    background-color: #3d3d5c;
    border: none;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #4d4d6c;
}

/* Group Box */
QGroupBox {
    border: 1px solid #3d3d5c;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: #ffd700;
}

/* Progress Bar (for timer) */
QProgressBar {
    border: none;
    border-radius: 10px;
    background-color: #252542;
    height: 20px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #ffd700;
    border-radius: 10px;
}

/* Scroll Area */
QScrollArea {
    border: none;
    background-color: transparent;
}

/* Tool Tip */
QToolTip {
    background-color: #252542;
    color: #eaeaea;
    border: 1px solid #ffd700;
    padding: 5px;
    border-radius: 4px;
}

/* System Tray Menu */
QMenu {
    background-color: #1a1a2e;
    border: 1px solid #3d3d5c;
    border-radius: 6px;
    padding: 5px;
}

QMenu::item {
    padding: 8px 25px;
    color: #eaeaea;
}

QMenu::item:selected {
    background-color: #3d3d5c;
}

QMenu::separator {
    height: 1px;
    background-color: #3d3d5c;
    margin: 5px 10px;
}
"""

# Colors for programmatic use
COLORS = {
    "background": "#1a1a2e",
    "surface": "#252542",
    "primary": "#ffd700",
    "secondary": "#3d3d5c",
    "success": "#2d6a4f",
    "danger": "#9d0208",
    "text": "#eaeaea",
    "text_secondary": "#b0b0b0",
}


