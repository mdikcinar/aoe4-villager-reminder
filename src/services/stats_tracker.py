import json
import os
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal
from ..utils.constants import STATS_FILE
from ..utils.localization import tr


class StatsTracker(QObject):
    """Tracks and persists usage statistics."""
    
    stats_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._stats_path = self._get_stats_path()
        self._stats: Dict[str, Any] = {}
        self._session_start: Optional[datetime] = None
        self._session_alerts = 0
        self._load()
    
    @staticmethod
    def _get_stats_path() -> str:
        """Get stats file path in user's app data directory."""
        app_data = os.environ.get('APPDATA', os.path.expanduser('~'))
        config_dir = os.path.join(app_data, 'AoE4VillagerReminder')
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, STATS_FILE)
    
    def _load(self):
        """Load statistics from file."""
        try:
            if os.path.exists(self._stats_path):
                with open(self._stats_path, 'r', encoding='utf-8') as f:
                    self._stats = json.load(f)
        except (json.JSONDecodeError, IOError):
            self._stats = {}
        
        # Ensure required keys exist
        defaults = {
            "total_alerts": 0,
            "total_sessions": 0,
            "total_game_time_seconds": 0,
            "daily_stats": {},
            "session_history": [],
        }
        for key, value in defaults.items():
            if key not in self._stats:
                self._stats[key] = value
    
    def _save(self):
        """Save statistics to file."""
        try:
            with open(self._stats_path, 'w', encoding='utf-8') as f:
                json.dump(self._stats, f, indent=2, default=str)
        except IOError as e:
            print(f"Error saving stats: {e}")
    
    def start_session(self):
        """Start a new tracking session."""
        self._session_start = datetime.now()
        self._session_alerts = 0
        self._stats["total_sessions"] += 1
        self._save()
    
    def end_session(self):
        """End the current session and save stats."""
        if self._session_start is None:
            return
        
        session_duration = (datetime.now() - self._session_start).total_seconds()
        
        # Update totals
        self._stats["total_game_time_seconds"] += session_duration
        
        # Add to session history (keep last 100)
        session_data = {
            "date": self._session_start.isoformat(),
            "duration_seconds": session_duration,
            "alerts": self._session_alerts,
        }
        self._stats["session_history"].append(session_data)
        self._stats["session_history"] = self._stats["session_history"][-100:]
        
        # Update daily stats
        today = date.today().isoformat()
        if today not in self._stats["daily_stats"]:
            self._stats["daily_stats"][today] = {"alerts": 0, "time_seconds": 0, "sessions": 0}
        
        self._stats["daily_stats"][today]["alerts"] += self._session_alerts
        self._stats["daily_stats"][today]["time_seconds"] += session_duration
        self._stats["daily_stats"][today]["sessions"] += 1
        
        self._session_start = None
        self._save()
        self.stats_updated.emit()
    
    def record_alert(self):
        """Record an alert notification."""
        self._session_alerts += 1
        self._stats["total_alerts"] += 1
        self._save()
        self.stats_updated.emit()
    
    @property
    def total_alerts(self) -> int:
        return self._stats.get("total_alerts", 0)
    
    @property
    def total_sessions(self) -> int:
        return self._stats.get("total_sessions", 0)
    
    @property
    def total_game_time(self) -> float:
        """Total game time in seconds."""
        return self._stats.get("total_game_time_seconds", 0)
    
    @property
    def session_alerts(self) -> int:
        return self._session_alerts
    
    @property
    def current_session_duration(self) -> float:
        """Current session duration in seconds."""
        if self._session_start:
            return (datetime.now() - self._session_start).total_seconds()
        return 0
    
    def get_today_stats(self) -> Dict[str, Any]:
        """Get statistics for today."""
        today = date.today().isoformat()
        return self._stats.get("daily_stats", {}).get(today, {
            "alerts": 0,
            "time_seconds": 0,
            "sessions": 0
        })
    
    def get_weekly_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics for the last 7 days."""
        from datetime import timedelta
        
        total_alerts = 0
        total_time = 0
        total_sessions = 0
        
        for i in range(7):
            day = (date.today() - timedelta(days=i)).isoformat()
            if day in self._stats.get("daily_stats", {}):
                day_stats = self._stats["daily_stats"][day]
                total_alerts += day_stats.get("alerts", 0)
                total_time += day_stats.get("time_seconds", 0)
                total_sessions += day_stats.get("sessions", 0)
        
        return {
            "alerts": total_alerts,
            "time_seconds": total_time,
            "sessions": total_sessions,
        }
    
    def get_average_alerts_per_session(self) -> float:
        """Calculate average alerts per session."""
        if self.total_sessions == 0:
            return 0
        return self.total_alerts / self.total_sessions
    
    def format_time(self, seconds: float) -> str:
        """Format seconds into human-readable string."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}{tr('time_format_hours')} {minutes}{tr('time_format_minutes')} {secs}{tr('time_format_seconds')}"
        elif minutes > 0:
            return f"{minutes}{tr('time_format_minutes')} {secs}{tr('time_format_seconds')}"
        else:
            return f"{secs}{tr('time_format_seconds')}"
    
    def reset_all_stats(self):
        """Reset all statistics."""
        self._stats = {
            "total_alerts": 0,
            "total_sessions": 0,
            "total_game_time_seconds": 0,
            "daily_stats": {},
            "session_history": [],
        }
        self._save()
        self.stats_updated.emit()


