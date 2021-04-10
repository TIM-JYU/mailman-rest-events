import logging
import requests
from mailman.config import config
from mailman.config.config import external_configuration
from mailman.interfaces.plugin import IPlugin
from public import public
from zope.interface import implementer
from zope.event import subscribers


logger = logging.getLogger("mailman.plugins")
logger.info(f"Pipelines: {config.pipelines}")

def init():
    config = external_configuration(
        config.plugin.mailman_rest_event.configuration)
    event_webhook_url = config.get("general", "webhook_url")

    if not event_webhook_url:
        logger.info("Webhook URL not set, will not be sending events")
        return

    logger.info(f"Webhook URL: {event_webhook_url}")

    def handle_event(evt):
        logger.info(f"Got event: {type(evt)}")

    subscribers.append(handle_event)


init()


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
