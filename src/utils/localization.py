"""Localization support for AoE4 Villager Reminder."""
import json
import locale
import os
from typing import Dict, Optional

from .config import Config


# Supported languages with their display names
SUPPORTED_LANGUAGES = {
    "en": "English",
    "tr": "Türkçe",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
}


class Localization:
    """Manages application localization/internationalization."""
    
    _instance: Optional['Localization'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._strings: Dict[str, str] = {}
            cls._instance._current_lang = "en"
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        """Initialize localization."""
        config = Config()
        saved_lang = config.get("language")
        
        if saved_lang and saved_lang in SUPPORTED_LANGUAGES:
            self._current_lang = saved_lang
        else:
            self._current_lang = self._detect_language()
            config.set("language", self._current_lang)
        
        self._load_strings()
    
    def _detect_language(self) -> str:
        """Detect system language and return supported language code."""
        try:
            # Get system locale
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                # Extract language code (e.g., 'en_US' -> 'en')
                lang_code = system_locale.split('_')[0].lower()
                if lang_code in SUPPORTED_LANGUAGES:
                    return lang_code
        except Exception:
            pass
        
        # Default to English
        return "en"
    
    def _get_locales_path(self) -> str:
        """Get the path to locales directory."""
        # Check multiple possible locations
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'locales'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'locales'),
        ]
        
        # For PyInstaller bundled app
        import sys
        if hasattr(sys, '_MEIPASS'):
            possible_paths.insert(0, os.path.join(sys._MEIPASS, 'src', 'locales'))
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return possible_paths[0]
    
    def _load_strings(self):
        """Load language strings from JSON file."""
        locales_path = self._get_locales_path()
        lang_file = os.path.join(locales_path, f"{self._current_lang}.json")
        
        # Fallback to English if language file doesn't exist
        if not os.path.exists(lang_file):
            lang_file = os.path.join(locales_path, "en.json")
            self._current_lang = "en"
        
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                self._strings = json.load(f)
        except (json.JSONDecodeError, IOError, FileNotFoundError):
            self._strings = {}
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get a localized string by key."""
        return self._strings.get(key, default if default is not None else key)
    
    def set_language(self, lang_code: str) -> bool:
        """Set the current language and reload strings."""
        if lang_code not in SUPPORTED_LANGUAGES:
            return False
        
        self._current_lang = lang_code
        config = Config()
        config.set("language", lang_code)
        self._load_strings()
        return True
    
    @property
    def current_language(self) -> str:
        """Get current language code."""
        return self._current_lang
    
    @property
    def current_language_name(self) -> str:
        """Get current language display name."""
        return SUPPORTED_LANGUAGES.get(self._current_lang, "English")
    
    def __call__(self, key: str, default: Optional[str] = None) -> str:
        """Shorthand for get()."""
        return self.get(key, default)


# Global instance for easy access
_loc = None

def get_localization() -> Localization:
    """Get the global Localization instance."""
    global _loc
    if _loc is None:
        _loc = Localization()
    return _loc

def tr(key: str, default: Optional[str] = None) -> str:
    """Translate a key. Shorthand function."""
    return get_localization().get(key, default)

