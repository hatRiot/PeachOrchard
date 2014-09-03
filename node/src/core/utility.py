from datetime import date, datetime
from src.core.log import *
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