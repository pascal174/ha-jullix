"""Constants for the Jullix EMS integration."""

DOMAIN = "jullix"
DEFAULT_NAME = "Jullix EMS"

# Config keys
CONF_LOCAL_IP = "local_ip"

# Update interval (seconds)
SCAN_INTERVAL_LOCAL = 10

# Local API base
LOCAL_API_BASE = "http://{ip}/api/ems"

# Local endpoints
ENDPOINT_SOLAR   = "/solar"
ENDPOINT_BATTERY = "/battery"
ENDPOINT_METER   = "/meter"
ENDPOINT_CHARGER = "/charger"
ENDPOINT_PLUG    = "/plug"
