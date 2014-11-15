from src.core.fuzzer import Fuzzer
from src.core import config
from src.core.log import *
from src.core import utility
from hashlib import sha256
from re import findall
import pkgutil
import importlib
import fileinput
import requests
import json


def register_node():
    """ Register the local node
    """

    if not config.SERVER_IP:
        utility.msg("Server IP not configured", ERROR)
        return False

    data = {
        "skey": sha256(config.SERVER_KEY).hexdigest(),
        "fuzzer" : config.SESSION_FUZZER,
        "session" : config.SESSION_NAME
    }

    #
    # POST the skey to the server; we should get back our assigned node ID
    #

    url = "http://{0}:{1}/register/".format(config.SERVER_IP, config.SERVER_PORT)
    try:
        response = requests.post(url, data=data)
    except Exception:
        return False

    if response.status_code is 200 and "Active" in response.content:

        node_id = findall("Node (.*?) Active", response.content)[0]
        _write_id(node_id)
        utility.msg("Node %s now assigned and active" % config.NODE_ID)
        return True

    else:
        utility.msg("Could not register node: %s" % response.content, ERROR)

    return False


def _write_id(node_id):
    """ Write the node ID to our config file
    """

    for line in fileinput.input("src/core/config.py", inplace=True):
        if "NODE_ID = None" in line:
            print "NODE_ID = %s\n" % node_id,
            continue

        print line,

    # instead of force loading the config and losing state, just reassign
    config.NODE_ID = node_id


def check_server():
    """ Simple check server
    """

    url = 'http://{0}:{1}'.format(config.SERVER_IP, 
                                  config.SERVER_PORT)
    try:
        response = requests.get(url)

        if response.status_code is 200:
            utility.msg("Server appears active.")
            return

    except:
        pass

    utility.msg("Could not reach server.", ERROR)


def register_crash(crash):
    """ Accepts a dictionary of {crash_idx : crash_file_path} and attempts to
    POST them to the remote server.  If the server already has the crash data,
    it will not be sent.
    """

    if len(crash.keys()) <= 0:
        return

    base = 'http://{0}:{1}'.format(config.SERVER_IP, config.SERVER_PORT)
    uri = '/node/%d/?crash={0}' % config.NODE_ID
    for (cidx, cpath) in crash.iteritems():

        try:
            response = requests.get(base + uri.format(cidx))
            if response.status_code is 200 and "Invalid crash" in response.content:

                # crash does not exist on server, POST it
                data = {
                    "node_id": config.NODE_ID,
                    "skey": sha256(config.SERVER_KEY).hexdigest(),
                    "crash_idx": str(cidx),
                    "crash": open(cpath).read()
                }

                response = requests.post(base + "/crash/", data=json.dumps(data))
                if response.status_code is 200 and "Node updated" in response.content:
                    utility.msg("Crash %s posted successfully" % cidx, LOG)
                else:
                    utility.msg("Failed to post crash %s: %s" % (cidx, response.content), ERROR)
                    
        except Exception, e:
            utility.msg("Error contacting remote server: %s" % e, ERROR)                


def send_status_update(status):
    """ Update the server with a fuzzer's status 
    """

    try:

        data = {
                "node_id" : config.NODE_ID,
                "skey" : sha256(config.SERVER_KEY).hexdigest(),
                "state" : status 
        }

        url = "http://{0}:{1}/status/".format(config.SERVER_IP, config.SERVER_PORT)
        response = requests.post(url, data=json.dumps(data))
        if response.status_code is 200 and "Node Updated" in response.content:
            utility.msg("Status '%s' updated" % status, LOG)
        else:
            utility.msg("Failed to submit status: %s" % response.content, ERROR)

    except Exception, e:
        utility.msg("Failed to send status update: %s" % e, ERROR)


def load_fuzzer():
    """ Dynamically load the specified fuzzer 
    """

    load = importlib.import_module("src.fuzzers")
    modules = list(pkgutil.iter_modules(load.__path__))
    for mod in modules:
        
        # pull up the module and iterate over its components, 
        # stop once we find the correct class to invoke.
        dp = mod[0].find_module(mod[1]).load_module(mod[1])
        for e in dir(dp):

            x = getattr(dp, e)
            if e and e != "Fuzzer" and config.SESSION_FUZZER in e and\
               issubclass(x, Fuzzer):
                utility.msg("Loaded fuzzer %s" % e, LOG)
                return x()

    return None
