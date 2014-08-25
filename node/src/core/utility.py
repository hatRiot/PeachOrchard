from datetime import date, datetime
from src.core.log import *


def msg(string, level=INFO):
    """
    """

    if level is INFO:
        print '\033[32m[%s] %s\033[0m' % (timestamp(), string)
    elif level is DEBUG:
        print '\033[34m[%s] %s\033[0m' % (timestamp(), string)
    elif level is ERROR:
        print '\033[31m[%s] %s\033[0m' % (timestamp(), string)


def timestamp():
    """
    """

    return '%s %s' % (date.today().isoformat(),
                      datetime.now().strftime("%I:%M%p"))


def log(string):
    """ Log string to file
    """

    pass 
