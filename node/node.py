from argparse import ArgumentParser
from src.core import node_resource as nr
from src.core import monitor
from src.core import config
from src.core import utility
from core.log import *
import sys
import os


def check_node():
    """ Validate this node by ensuring it's properly authd to the remote server.
        We'll also perform a few checks to ensure the session information is available to us.
    """

    valid = False
    if config.MONITOR_DIR and (config.NODE_ID or nr.register_node()):
        valid = True

    # pry open MONITOR_DIR and check for SESSION or grab latest
    if config.MONITOR_DIR and os.path.isdir(config.MONITOR_DIR):

        if config.SESSION:
            # validate session exists
            if config.SESSION not in os.listdir(config.MONITOR_DIR):
                utility.msg("Session %s not found at %s" % (config.SESSION, config.MONITOR_DIR))
            else:
                valid = True

        else:
            # grab latest session
            config.SESSION = os.listdir(config.MONITOR_DIR)[-1]
            utility.msg("Setting session to %s" % config.SESSION, LOG)
            valid = True

    else:
        utility.msg("Directory '%s' not found" % config.MONITOR_DIR, ERROR)
        valid = False

    return valid


def parse_args():
    """
    """

    parser = ArgumentParser()
    parser.add_argument("--check", help="Check server connectivity",
                        action='store_true', dest='check')

    opts = parser.parse_args(sys.argv[1:])
    return opts


if __name__ == "__main__":

    args = parse_args()
    if args.check:
        nr.check_server()
        sys.exit(1)

    if check_node():
        # node is registered, kick off monitoring
        monitor.monitor()
