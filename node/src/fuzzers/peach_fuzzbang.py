from src.core.log import *
from src.core import config
from src.core import utility
from src.core.fuzzer import Fuzzer
from re import findall
import os


class peach_fuzzbang(Fuzzer):
    """ Class implements the interface for the Peach fuzzer.  This has
    been tested with FuzzBang as well as regular ol' Peach.
    """

    def __init__(self):
        self.name = "Peach FuzzBang"


    def fetch_crashes(self):
        """
        """

        base = config.MONITOR_DIR + '/' + config.SESSION
        crashes = {}

        # build a list of files from session root
        pot_files = []
        for (root, subFolders, files) in os.walk(base):
            for file in files:
                f = os.path.join(root, file)
                pot_files.append(f.replace('\\', '/'))

        # massage these into our crashes dictionary
        for entry in pot_files:
            if '_description.txt' in entry:

                # found description entry, parse it
                e = entry.rsplit('/', 2)
                crashes[e[1]] = entry

        return crashes


    def get_status(self):
        """ Parse the status file and pull the latest iteration update 
        """

        try:
            data = None
            spath = config.MONITOR_DIR + '/' + config.SESSION + '/' + 'status.txt'
            with open(spath) as f:
                data = f.read().split('\n')

            # chop it up
            status = None
            data = [x for x in data if len(x) > 0]
            if 'Test finished' in data[:-1]:
                status = 'Completed'
            else:
                (cidx, total) = findall("Iteration (.*?) of (.*?) :", data[-1])[0]
                status = '%s/%s' % (cidx, total)

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

                if config.SESSION:
                    # validate session
                    if config.SESSION not in os.listdir(config.MONITOR_DIR):
                        utility.msg("Session %s not found in %s" % (config.SESSION, config.MONITOR_DIR))
                    else:
                        valid = True

                else:
                    # fetch latest version
                    tmp = os.listdir(config.MONITOR_DIR)
                    if len(tmp) <= 0:
                        utility.msg("No running sessions found", ERROR)
                        valid = False
                    else:
                        config.SESSION = tmp[-1]
                        utility.msg("Setting session to %s" % config.SESSION, LOG)
                        valid = True

            else:
                utility.msg("Directory '%s' not found" % config.MONITOR_DIR, ERROR)
                valid = False

        except Exception, e:
            utility.msg("Error checking session: %s" % e, ERROR)
            valid = False

        return valid
