"""
Pytest configuration and fixtures for PyQt6 testing.
"""

import sys
import os
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from PyQt6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def golden_dir():
    """Return the path to the golden images directory."""
    path = os.path.join(os.path.dirname(__file__), 'golden')
    os.makedirs(path, exist_ok=True)
    return path

