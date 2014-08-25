from server.core import utility
from server.core.log import *
from server.models import Crash, Node
from hashlib import sha256
from re import findall
import server.settings as settings
import json
import os


def _get_crash_data(node_id, crash_id):
    """ Given a node ID and crash ID, pull the crash data and return it
    """

    data = ""
    try:
        cdir = settings.NODE_DIR + '/' + str(node_id)
        with open(cdir + '/' + str(crash_id) + '/crash_description.txt') as f:
            data = f.read()

    except Exception, e:
        utility.msg("Failed to read crash %d data: %s" % (node_id, e), LOG)
        data = None

    return data


def _write_crash(data, node):
    """ Write a new crash into a node's path 
    """

    npath = settings.NODE_DIR + '/' + str(node.id)
    if not os.path.isdir(npath):
        os.mkdir(npath)

    # crash folder
    cdir = npath + '/' + data["crash_idx"]
    os.mkdir(cdir)
    with open(cdir + '/' + 'crash_description.txt', "w+") as f:
        f.write(data['crash'])


def _validate_crash(crash_id, node):
    """ Check if the incoming crash ID exists and is attributed to the
    given node
    """

    valid = False
    try:
        crash = Crash.objects.filter(fault_index=crash_id, node_index=node.id)
        if len(crash) > 0:
            valid = True
    except:
        pass

    return valid


def _validate_node(request):
    """ Validate an incoming request; returns the node if found,
        otherwise None
    """

    try:
        data = json.loads(request.body)
        node_id = data["node_id"]
        skey = data["skey"]
        node = Node.objects.get(id = node_id)

        if node.ip != request.META.get("REMOTE_ADDR"):
            utility.msg("Remote address %s does not match node %s IP (%s)" % 
                        (request.META.get("REMOTE_ADDR"), node.id, node.ip), LOG)
            node = None

        if sha256(settings.SECRET_KEY).hexdigest() != skey:
            utility.msg("Invalid key found for node %s from ip %s" %
                        (node.id, request.META.get("REMOTE_ADDR")), LOG)
            node = None

    except Exception, e:
        utility.msg("Failed to validate node: %s" % e, LOG)
        node = None
        
    return node


def parse_key(key, data):
    """ Parse out a key from the output of !exploitable
    """

    value = findall("%s:(.*?)\n" % key.upper(), data)
    if value and len(value) > 0:
        return value[0]