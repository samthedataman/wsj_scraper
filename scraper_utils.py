from inspect import getframeinfo, stack
import os


def log(message):
    caller = getframeinfo(stack()[1][0])
    print("%s:%d - %s" % (os.path.basename(caller.filename), caller.lineno, message))
