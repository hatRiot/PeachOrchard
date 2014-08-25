from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import Node, Crash
from hashlib import sha256
from core.log import *
import core.utility as utility
import settings as settings
import core.view_utility as vu
import json


def home(request):
    """ Load home template
    """

    nodes = Node.objects.all()
    return render_to_response("home.html",
                              {"nodes": nodes},
                              context_instance=RequestContext(request))


def node(request, node_id=-1):
    """ Load a node and render pertinent info
    """

    ret = render_to_response('node.html',
                             {'node': False},
                             context_instance=RequestContext(request))

    try:
        node = Node.objects.get(id=node_id)

        if 'crash' in request.GET:
            crash_id = int(request.GET.get('crash'))
            if vu._validate_crash(crash_id, node):
                ret = render_to_response('crash.html',
                                         {'node': node,
                                          'crash_id': crash_id,
                                          'crash': vu._get_crash_data(node.id, crash_id)},
                                         context_instance=RequestContext(request))
            else:
                ret = HttpResponse("Invalid crash")

        else:
            crashes = Crash.objects.filter(node_index=node)
            ret = render_to_response('node.html',
                                     {'node': node,
                                     'crashes': crashes},
                                     context_instance=RequestContext(request))

    except Node.DoesNotExist:
        pass

    return ret


@csrf_exempt
def register(request):
    """ Register a new node
    """

    if request.method != 'POST':
        return HttpResponse("Invalid GET")

    #
    # Registration requires only the exchange of a PSK.
    #

    # hash
    skey = request.POST.get('skey')
    node_id = None
    if 'node_id' in request.POST:
        node_id = request.POST.get('node_id')

    # compare
    if sha256(settings.SECRET_KEY).hexdigest() != skey:
        return HttpResponse("Invalid Key")

    try:
        node = Node.objects.get(id=node_id)
    except Node.DoesNotExist:

        # new node
        node = Node.objects.create(
            ip=request.META.get('REMOTE_ADDR'),
            active=True,
            start_time=utility.timestamp()
        )

        node.save()

    return HttpResponse("Node %d Active" % node.id)


@csrf_exempt
def crash(request):
    """ Register crash data with the server
    """

    if request.method != 'POST':
        return HttpResponse('Invalid GET')

    node = vu._validate_node(request)
    if not node:
        return HttpResponse("Invalid node")

    #
    # checks out; with this we generate a new crash object,
    # tie it to the node ID, and write the crash data to
    # its respective file
    #

    try:
        data = json.loads(request.body)
        node.faults += + 1
        crash = Crash.objects.create(
            fault_index=data['crash_idx'],
            node_index=node,
            crash_time=utility.timestamp(),
            exception_type=vu.parse_key("EXCEPTION_TYPE", data['crash']),
            classification=vu.parse_key("CLASSIFICATION", data['crash'])
        )

        crash.save()
        node.save()
        vu._write_crash(data, node)
    except Exception, e:
        utility.msg("Failed to log crash: %s" % e, ERROR)
        return HttpResponse("Failed")

    utility.msg("Node %d posted crash" % node.id)
    return HttpResponse("Node updated")


@csrf_exempt
def status(request):
    """ Register node status update
    """

    if request.method != "POST":
        return HttpResponse("Invalid GET")

    node = vu._validate_node(request)
    if not node:
        return HttpResponse("Invalid node")

    try:
        data = json.loads(request.body)
        node.iteration = data['iteration']
        node.save()
    except Exception:
        return HttpResponse("Bad node data")

    utility.msg("Node %d updated" % node.id)
    return HttpResponse("Node Updated")