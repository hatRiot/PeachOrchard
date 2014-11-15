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
# Set to None if you want to re-register this instance
NODE_ID = None

# this is the absolute path to the fuzzer's log directory.  this
# may vary fuzzer to fuzzer.  As for supported fuzzers:
#   Peach: /path/to/peach/Logs
#   AFL: /path/to/afl/output
MONITOR_DIR = r"/tmp/Logs"

# poll for faults and status updates every 5 minutes
CHECK_INTERVAL = 300

# by default, Peach Orchard will grab the latest session from MONITOR_DIR
# and use that to feed information back; if, by chance, you want to monitor
# another specific session, set that here.  This only applies to fuzzers
# with the concept of a session, such as Peach
SESSION = None

# where debugging/logging messages get written to
LOG_FILE = "./node-output.log"

# fuzzer to use; set via -f
SESSION_FUZZER = None

# session name; set via -n
SESSION_NAME = None
