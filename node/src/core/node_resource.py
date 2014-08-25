from src.core import config
from src.core.log import *
from src.core import utility
from hashlib import sha256
from re import findall
import fileinput
import requests
import os
import json


def register_node():
    """ Register the local node
    """

    if not config.SERVER_IP:
        utility.msg("Server IP not configured", ERROR)
        return False

    data = {
        "skey": sha256(config.SERVER_KEY).hexdigest(),
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

    # reload config module
    reload(config)


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


def log_hash():
    """ Fetches the SHA256 hash of the current session's status file.
    """

    BLOCK_SIZE = 8960  # multiple of 256
    if not os.path.isdir(config.MONITOR_DIR):
        return None

    with open(config.MONITOR_DIR + '/' + config.SESSION + '/status.txt') as f:
        obj = sha256()
        while True:
            data = f.read(BLOCK_SIZE)
            if not data:
                break

            obj.update(data)

    return obj.hexdigest()


def register_crash(crash):
    """ Accepts a dictionary of {crash_idx : crash_file_path} and attempts to
    POST them to the remote server.  If the server already has the crash data,
    it will not be sent.
    """

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


def send_status_update():
    """ Pull the current iteration from the status file and post it to
    the remote server
    """

    try:
        data = None
        spath = config.MONITOR_DIR + '/' + config.SESSION + '/' + 'status.txt'
        with open(spath) as f:
            data = f.read().split('\n')

        # chop it up
        status = None
        data = [x for x in data if len(x) > 0]
        if 'Test finished' in data[-1]:
            status = 'Completed'
        else:
            (cidx, total) = findall("Iteration (.*?) of (.*?) :", data[-1])[0]
            status = '%s/%s' % (cidx, total)

        # prepare to send
        data = {
            "node_id": config.NODE_ID,
            "skey": sha256(config.SERVER_KEY).hexdigest(),
            "iteration": status
        }

        url = 'http://{0}:{1}/status/'.format(config.SERVER_IP, config.SERVER_PORT)
        response = requests.post(url, data=json.dumps(data))
        if response.status_code is 200 and "Node Updated" in response.content:
            utility.msg("Status '%s' updated" % status, LOG)
        else:
            utility.msg("Failed to submit status: %s" % response.content, ERROR)

    except Exception, e:
        utility.msg("Failed to send status update: %s" % e, ERROR)
