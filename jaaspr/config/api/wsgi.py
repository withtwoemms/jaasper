from enum import auto
import logging

from jaaspr.core.enums import FromEnviron


class WsgiEnvironment(FromEnviron):
    WSGI_SERVER = auto()
    WSGI_SERVER_LOG_LEVEL = auto()


waitress_logger = logging.getLogger(WsgiEnvironment.WSGI_SERVER.value)
waitress_logger.setLevel(WsgiEnvironment.WSGI_SERVER_LOG_LEVEL.value)
