from datetime import date, datetime
#from src.core.fuzzer import Fuzzer
from src.core.log import *
from inspect import isclass
import src.core.fuzzer
import pkgutil
import importlib
import platform
import config


def msg(string, level=INFO):
    """ Handle messages; this takes care of logging and
    debug checking, as well as output colors
    """

    string = "[%s] %s" % (timestamp(), string)
    if 'linux' in platform.platform().lower():
        if level is INFO:
            color_string = '%s%s%s' % ('\033[32m', string, '\033[0m')
        elif level is DEBUG:
            color_string = '%s%s%s' % ('\033[34m', string, '\033[0m')
        elif level is ERROR:
            color_string = '%s%s%s' % ('\033[31m', string, '\033[0m')
        else:
            color_string = string

    if level is DEBUG and not config.DEBUG:
        return

    if not level is LOG:
        print color_string

    log(string)


def timestamp():
    """ Generate a timestamp 
    """

    return '%s %s' % (date.today().isoformat(),
                      datetime.now().strftime("%I:%M%p"))


def log(string):
    """ Log string to file
    """

    with open(config.LOG_FILE, "a+") as f:
        f.write("[%s] %s\n" % (timestamp(), string))


def list_fuzzers():
    """ Dump all of the fuzzers currently loadable
    """

    msg("Currently loaded fuzzers")
    try:
        load = importlib.import_module("src.fuzzers")
        modules = list(pkgutil.iter_modules(load.__path__))
        for mod in modules:

            dp = mod[0].find_module(mod[1]).load_module(mod[1])
            for e in dir(dp):
                x = getattr(dp, e)
                if isclass(x) and e != "Fuzzer" and issubclass(x, src.core.fuzzer.Fuzzer):
                    msg("  %s (%s)" % (x().name, mod[1]))

    except Exception, e:
        msg("Failed to list modules: %s" % e, ERROR)


def dict_delta(first, second):
    """ Returns the delta between two dictionaries
    """

    diff = {}
    comb = dict(first.items() + second.items())
    for key in comb.keys():
        if not first.has_key(key):
            diff[key] = second[key]
        elif not second.has_key(key):
            diff[key] = first[key]

    return diff
