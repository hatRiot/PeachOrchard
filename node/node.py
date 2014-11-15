from argparse import ArgumentParser
from src.core import node_resource as nr
from src.core import monitor
from src.core import config
from src.core import utility
from src.core.log import *
import sys
import os


def check_node():
    """ Validate this node by ensuring it's properly authd to the remote server.
        We'll also perform a few checks to ensure the session information is available to us.
    """

    valid = False
    module = None
    
    module = nr.load_fuzzer()
    if not module:
        valid = False
    else: 
        valid = module.check_session()
        config.SESSION_FUZZER = module.name

    if config.MONITOR_DIR and (config.NODE_ID or nr.register_node()):
        valid = True

    if not valid:
        module = None

    return module


def parse_args():
    """
    """

    parser = ArgumentParser()
    parser.add_argument("-f", help="Set fuzzer",
                        action="store", dest='fuzzer', metavar='[fuzzer]')
    parser.add_argument("-n", help="Fuzzing session name",metavar='[name]',
                        action='store', dest='session_name',
                        default='Generic fuzzing session')
    parser.add_argument("--check", help="Check server connectivity",
                        action='store_true', dest='check')
    parser.add_argument("--list", help="List available fuzzers",
                        action='store_true', dest='list_fuzzers',
                        default=False)

    opts = parser.parse_args(sys.argv[1:])

    # set the session name 
    config.SESSION_NAME = opts.session_name
    config.SESSION_FUZZER = opts.fuzzer

    return opts


if __name__ == "__main__":

    args = parse_args()
    if args.check:
        nr.check_server()
        sys.exit(1)

    if args.list_fuzzers:
        utility.list_fuzzers()
        sys.exit(1)

    mod = check_node()
    if mod:
        # node is registered, kick off monitoring
        monitor.monitor(mod)
