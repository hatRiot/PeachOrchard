#
# Node configuration file
#

# server PSK
SERVER_KEY = None 

# server IP
SERVER_IP = "127.0.0.1"

# server port
SERVER_PORT = 8000

# debug
DEBUG = True

# node id
# Set to None if you want to reregister this instance
NODE_ID = None

# this is the absolute path to Peach's log directory
MONITOR_DIR = r"/tmp/Logs"

# poll for faults and status updates every 5 minutes
CHECK_INTERVAL = 300

# by default, Peach Orchard will grab the latest session from MONITOR_DIR
# and use that to feed information back; if, by chance, you want to monitor
# another peach session, set that here
SESSION = None
