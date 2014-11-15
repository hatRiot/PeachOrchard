from src.core.fuzzer import Fuzzer
from src.core import config
from src.core import utility
from src.core.log import *
import os

class afl(Fuzzer):
    """ Tested with AFL 0.45b
    """

    def __init__(self):
        self.name = "American Fuzzy Lop"

    def fetch_crashes(self):
        """ AFL has a simple output format to parse; we essentially just
        grab all of the files in the /crashes directory and index them
        with a count
        """

        base = config.MONITOR_DIR + '/crashes' 
        crashes = {}

        # build a list of crashes
        pot_files = []
        for (root, subFolders, files) in os.walk(base):
            for file in files:
                f = os.path.join(root, file)
                pot_files.append(f.replace('\\', '/'))
        
        for (idx, entry) in enumerate(pot_files):
            crashes[idx] = entry

        return crashes

    def get_status(self):
        """  
        """

        try:
            status = None
            data = None
            base = config.MONITOR_DIR + '/fuzzer_stats'
            
            with open(base) as f:
                data = f.read().split('\n')

            # afl runs indefinitely, so we'll just grab the total cycles completed
            if len(data) > 0:
                status = "%s cycles" % data[0].split(':')[1].lstrip()

        except Exception, e:
            utility.msg("Failed to parse status update: %s" % e, ERROR)
            status = "Error"

        return status

    def check_session(self):
        """
        """

        valid = False
        try:

            if config.MONITOR_DIR and os.path.isdir(config.MONITOR_DIR):
                valid = True
                
        except Exception, e:
            utility.msg("Error checking session: %s" % e, ERROR)
            valid = False

        return valid
