#!/usr/bin/env python3
"""
Golden tests for UI panels.
Captures screenshots of Timer, Settings, and Statistics panels for documentation.

Usage:
    pytest tests/test_golden.py -v
    
Or run directly to generate images:
    python tests/test_golden.py
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

from src.ui.timer_panel import TimerPanel
from src.ui.settings_panel import SettingsPanel
from src.ui.statistics_panel import StatisticsPanel
from src.ui.overlay_widget import OverlayWidget
from src.ui.styles import DARK_THEME
from src.services.stats_tracker import StatsTracker
from src.utils.localization import tr


def get_golden_dir():
    """Get the golden images directory path."""
    golden_dir = os.path.join(os.path.dirname(__file__), 'golden')
    os.makedirs(golden_dir, exist_ok=True)
    return golden_dir


def create_styled_container(widget: QWidget, width: int = 380, height: int = 500) -> QWidget:
    """Wrap a widget in a styled container with dark theme."""
    container = QWidget()
    container.setStyleSheet(DARK_THEME + """
        QWidget {
            background-color: #1a1a2e;
        }
    """)
    container.setFixedSize(width, height)
    
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    
    return container


def capture_widget(widget: QWidget, filename: str):
    """Capture a widget to an image file."""
    widget.show()
    widget.repaint()
    
    # Process events to ensure widget is fully rendered
    QApplication.processEvents()
    
    # Capture the widget
    pixmap = widget.grab()
    
    # Save to file
    golden_dir = get_golden_dir()
    filepath = os.path.join(golden_dir, filename)
    pixmap.save(filepath, 'PNG')
    
    print(f"Saved: {filepath}")
    return filepath


def generate_timer_panel_image():
    """Generate timer panel screenshot."""
    panel = TimerPanel()
    panel.update_timer(25, 25)  # Set initial state
    panel.set_status(tr("timer_ready"))
    
    container = create_styled_container(panel, 380, 420)
    return capture_widget(container, 'timer_panel.png')


def generate_settings_panel_image():
    """Generate settings panel screenshot."""
    panel = SettingsPanel()
    
    # Increase height to fit all components properly
    container = create_styled_container(panel, 380, 540)
    return capture_widget(container, 'settings_panel.png')


def generate_statistics_panel_image():
    """Generate statistics panel screenshot."""
    # Create a mock stats tracker
    stats_tracker = StatsTracker()
    
    panel = StatisticsPanel(stats_tracker)
    
    container = create_styled_container(panel, 380, 420)
    return capture_widget(container, 'statistics_panel.png')


def generate_overlay_image():
    """Generate in-game overlay screenshot."""
    overlay = OverlayWidget()
    overlay.update_timer(25)
    overlay.set_running(True)
    overlay.set_status(tr("timer_running"))
    
    # Overlay doesn't need a container, it's already styled
    return capture_widget(overlay, 'in_game_overlay.png')


def generate_all_images():
    """Generate all golden images."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    print("=" * 50)
    print("Generating Golden Images")
    print("=" * 50)
    
    images = []
    
    # Timer Panel
    print("\n[1/4] Timer Panel...")
    images.append(generate_timer_panel_image())
    
    # Settings Panel
    print("\n[2/4] Settings Panel...")
    images.append(generate_settings_panel_image())
    
    # Statistics Panel
    print("\n[3/4] Statistics Panel...")
    images.append(generate_statistics_panel_image())
    
    # In-Game Overlay
    print("\n[4/4] In-Game Overlay...")
    images.append(generate_overlay_image())
    
    print("\n" + "=" * 50)
    print("All images generated successfully!")
    print("=" * 50)
    
    return images


# Pytest tests
class TestGoldenImages:
    """Test class for generating golden images."""
    
    def test_timer_panel_screenshot(self, qapp, golden_dir):
        """Generate timer panel screenshot."""
        panel = TimerPanel()
        panel.update_timer(25, 25)
        panel.set_status(tr("timer_ready"))
        
        container = create_styled_container(panel, 380, 420)
        filepath = capture_widget(container, 'timer_panel.png')
        
        assert os.path.exists(filepath)
        assert os.path.getsize(filepath) > 0
    
    def test_settings_panel_screenshot(self, qapp, golden_dir):
        """Generate settings panel screenshot."""
        panel = SettingsPanel()
        
        # Increase height to fit all components properly
        container = create_styled_container(panel, 380, 540)
        filepath = capture_widget(container, 'settings_panel.png')
        
        assert os.path.exists(filepath)
        assert os.path.getsize(filepath) > 0
    
    def test_statistics_panel_screenshot(self, qapp, golden_dir):
        """Generate statistics panel screenshot."""
        stats_tracker = StatsTracker()
        panel = StatisticsPanel(stats_tracker)
        
        container = create_styled_container(panel, 380, 420)
        filepath = capture_widget(container, 'statistics_panel.png')
        
        assert os.path.exists(filepath)
        assert os.path.getsize(filepath) > 0
    
    def test_overlay_screenshot(self, qapp, golden_dir):
        """Generate in-game overlay screenshot."""
        overlay = OverlayWidget()
        overlay.update_timer(25)
        overlay.set_running(True)
        overlay.set_status(tr("timer_running"))
        
        filepath = capture_widget(overlay, 'in_game_overlay.png')
        
        assert os.path.exists(filepath)
        assert os.path.getsize(filepath) > 0


if __name__ == "__main__":
    generate_all_images()

