from src.core.log import *
from src.core import node_resource as nr
from src.core import config
from src.core import utility
from time import sleep
import os


def monitor(fuzzy):
    """
    """

    # known crashes; key is idx (top level folder before crash info); value is 
    known_crashes = {}

    try:
        utility.msg("Initializing monitor for node %s..." % config.NODE_ID)

        # check monitor dir
        if not os.path.isdir(config.MONITOR_DIR):
            utility.msg("Directory %s not found" % config.MONITOR_DIR, ERROR)
            return

        #
        # prior to monitor loop, lets ensure we're synced with upstream by providing
        # current set of crashes; dupes will be thrown out 
        #

        # register crashes
        current_crashes = fuzzy.fetch_crashes()
        nr.register_crash(current_crashes)
       
        # baseline
        fuzzy.crashes = current_crashes

        while True:

            # status update
            nr.send_status_update(fuzzy.get_status())

            # check for any new crashes 
            temporal_crash = fuzzy.check_new_crashes()
            if temporal_crash:

                # we have new crashes; ship them over
                nr.register_crash(temporal_crash)

            # sleep, now
            sleep(config.CHECK_INTERVAL)

    except KeyboardInterrupt:
        pass
    except Exception, e:
        utility.msg("Error during monitor: %s" % e, ERROR)
