"""Constants for the Jullix EMS integration."""

DOMAIN = "jullix"
DEFAULT_NAME = "Jullix EMS"

# Config keys
CONF_LOCAL_IP = "local_ip"
CONF_INSTALL_ID = "install_id"
CONF_API_TOKEN = "api_token"
CONF_USE_CLOUD = "use_cloud"

# Update intervals (seconds)
SCAN_INTERVAL_LOCAL = 10
SCAN_INTERVAL_CLOUD = 30

# Local API base
LOCAL_API_BASE = "http://{ip}/api/ems"

# Cloud API base
CLOUD_API_BASE = "https://mijn.jullix.be/api/v1"

# Local endpoints
ENDPOINT_SOLAR   = "/solar"
ENDPOINT_BATTERY = "/battery"
ENDPOINT_METER   = "/meter"
ENDPOINT_CHARGER = "/charger"
ENDPOINT_PLUG    = "/plug"

# Cloud endpoints
ENDPOINT_CLOUD_POWER_SUMMARY  = "/actual/{install_id}/summary/power"
ENDPOINT_CLOUD_BATTERY_DETAIL = "/actual/{install_id}/detail/battery"
ENDPOINT_CLOUD_CHARGER_DETAIL = "/actual/{install_id}/detail/charger"
ENDPOINT_CLOUD_GRID_DETAIL    = "/actual/{install_id}/detail/grid"
ENDPOINT_CLOUD_SOLAR_DETAIL   = "/actual/{install_id}/detail/solar"
ENDPOINT_CLOUD_HOME_DETAIL    = "/actual/{install_id}/detail/home"
ENDPOINT_CLOUD_CHARGER_STATUS = "/charger/{mac}/status"
