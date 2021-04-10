import logging

from mailman.interfaces.plugin import IPlugin
from public import public
from zope.interface import implementer
from zope.event import subscribers

logger = logging.getLogger("mailman.plugins")

logger.info("RestEventPlugin start!")


def handle_event(evt):
    logger.info(f"Got event: {type(evt)}")

subscribers.append(evt)

@public
@implementer(IPlugin)
class RestEventPlugin:

    def pre_hook(self):
        pass

    def post_hook(self):
        pass

    @property
    def resource(self):
        return None