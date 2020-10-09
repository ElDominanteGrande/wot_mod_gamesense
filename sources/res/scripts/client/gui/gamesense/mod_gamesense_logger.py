from enum import Enum
from debug_utils import LOG_ERROR, LOG_WARNING, LOG_NOTE
from config import Config as cfg

class LOG_LEVEL(object):
    NONE = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    TRACE = 4
    DEBUG = 5

logPrefix = cfg["code_config"]["log_prefix"]
logLevel = cfg["code_config"]["log_level"]

def logError(*msg):
    if logLevel >= LOG_LEVEL.ERROR:
        LOG_ERROR(logPrefix, map(str, msg))

def logWarning(*msg):
    if logLevel >= LOG_LEVEL.WARNING:
        LOG_WARNING(logPrefix, map(str, msg))

def logInfo(*msg):
    if logLevel >= LOG_LEVEL.INFO:
        LOG_NOTE(logPrefix, map(str, msg))

def logTrace(*msg):
    if logLevel >= LOG_LEVEL.TRACE:
        print(logPrefix + "[TRACE] ", map(str, msg))

def logDebug(*msg):
    if logLevel >= LOG_LEVEL.DEBUG:
        print(logPrefix + "[DEBUG] ", map(str, msg))