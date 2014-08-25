from datetime import date, datetime
from server.core.log import *

def timestamp():
	return '%s %s' % (date.today().isoformat(),
					  datetime.now().strftime('%I:%M%p'))

def version():
    """
    """

    return "0.1"


def msg(string, level = INFO):
    """
    """

    if level is INFO:
        print '\033[32m[%s] %s\033[0m' % (timestamp(), string)
    elif level is DEBUG:
        print '\033[34m[%s] %s\033[0m' % (timestamp(), string)
    elif level is ERROR:
        print '\033[31m[%s] %s\033[0m' % (timestamp(), string)

    log(string)


def log(string):
    """ Log string to defined log file
    """

    # XXX - FIX ME
    with open("output.log", 'a+') as f:
        f.write('[%s] %s\n' % (timestamp(), string))
