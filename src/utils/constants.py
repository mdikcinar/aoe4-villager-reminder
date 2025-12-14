# Application constants
APP_NAME = "AoE4 Villager Reminder"
APP_VERSION = "1.0.0"

# Timer defaults
DEFAULT_INTERVAL = 25  # seconds (villager production time)
MIN_INTERVAL = 5
MAX_INTERVAL = 60

# Game detection via aoe4world.com API
AOE4_API_URL = "https://aoe4world.com/api/v0/players/{profile_id}/games/last"
API_CHECK_INTERVAL = 10000  # ms (check every 10 seconds for match status)

# Game executable detection
AOE4_EXECUTABLE = "RelicCardinal.exe"
PROCESS_CHECK_INTERVAL = 10000  # ms (check every 10 seconds if game is running)

# Detection modes
DETECTION_MODE_API = "api"
DETECTION_MODE_MANUAL = "manual"

# Notification
DEFAULT_VOLUME = 70  # 0-100

# Config file
CONFIG_FILE = "config.json"
STATS_FILE = "statistics.json"


