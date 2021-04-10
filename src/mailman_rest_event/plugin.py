import logging

from mailman.interfaces.plugin import IPlugin
from public import public
from zope.interface import implementer

logger = logging.getLogger("mailman.plugins")


@public
@implementer(IPlugin)
class RestEventPlugin:

    def pre_hook(self):
        logger.info("Initialized RestEventPlugin")

    def post_hook(self):
        logger.info("Closed RestEventPlugin")

    @property
    def resource(self):
        return None