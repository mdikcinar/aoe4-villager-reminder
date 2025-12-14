# Application constants
APP_NAME = "AoE4 Villager Reminder"
APP_VERSION = "1.0.0"

# Timer defaults
DEFAULT_INTERVAL = 25  # seconds (villager production time)
MIN_INTERVAL = 5
MAX_INTERVAL = 60

# Game detection
AOE4_PROCESS_NAMES = ["RelicCardinal.exe", "Age4.exe"]
AOE4_API_URL = "https://aoe4world.com/api/v0/players/{profile_id}/games/last"
PROCESS_CHECK_INTERVAL = 2000  # ms
API_CHECK_INTERVAL = 15000  # ms

# Detection modes
DETECTION_MODE_PROCESS = "process"
DETECTION_MODE_API = "api"
DETECTION_MODE_MANUAL = "manual"

# Notification
DEFAULT_VOLUME = 70  # 0-100

# Config file
CONFIG_FILE = "config.json"
STATS_FILE = "statistics.json"


