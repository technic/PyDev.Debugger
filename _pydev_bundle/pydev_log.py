import sys
from _pydevd_bundle.pydevd_constants import DebugInfoHolder, get_global_debugger
from _pydev_imps._pydev_saved_modules import threading
currentThread = threading.currentThread

import traceback

WARN_ONCE_MAP = {}


def stderr_write(message):
    dbg = get_global_debugger()
    if dbg is None:
        sys.stderr.write(message)
        sys.stderr.write("\n")
    else:
        dbg.cmd_factory.make_log_message()

def _handle(level, message):
    if DebugInfoHolder.DEBUG_TRACE_LEVEL >= level:
        stderr_write(message)

def debug(message):
    _handle(3, message)


def warn(message):
    _handle(2, message)


def info(message):
    _handle(1, message)


def error(message, tb=False):
    stderr_write(message)
    if tb:
        traceback.print_exc()


def user_warning_once(message):
    if message not in WARN_ONCE_MAP:
        WARN_ONCE_MAP[message] = True
        stderr_write(message)

