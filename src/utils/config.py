import json
import os
from typing import Any, Optional
from .constants import (
    CONFIG_FILE, 
    DEFAULT_INTERVAL, 
    DEFAULT_VOLUME,
    DETECTION_MODE_API
)


class Config:
    """Manages application configuration with JSON persistence."""
    
    _instance: Optional['Config'] = None
    _defaults = {
        "interval": DEFAULT_INTERVAL,
        "volume": DEFAULT_VOLUME,
        "detection_mode": DETECTION_MODE_API,
        "profile_id": None,
        "sound_enabled": True,
        "popup_enabled": True,
        "always_on_top": False,
        "start_minimized": False,
        "auto_start_detection": True,
        "auto_show_overlay": True,
        "language": None,  # None means auto-detect
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
            cls._instance._config_path = cls._get_config_path()
            cls._instance._load()
        return cls._instance
    
    @staticmethod
    def _get_config_path() -> str:
        """Get config file path in user's app data directory."""
        app_data = os.environ.get('APPDATA', os.path.expanduser('~'))
        config_dir = os.path.join(app_data, 'AoE4VillagerReminder')
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, CONFIG_FILE)
    
    def _load(self):
        """Load configuration from file."""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
        except (json.JSONDecodeError, IOError):
            self._config = {}
        
        # Apply defaults for missing keys
        for key, value in self._defaults.items():
            if key not in self._config:
                self._config[key] = value
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default if default is not None else self._defaults.get(key))
    
    def set(self, key: str, value: Any):
        """Set a configuration value and save."""
        self._config[key] = value
        self.save()
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any):
        self.set(key, value)


