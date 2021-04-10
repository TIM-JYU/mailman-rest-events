import logging
import requests
from mailman.config import config
from mailman.config.config import external_configuration
from mailman.interfaces.plugin import IPlugin
from public import public
from zope.interface import implementer
from zope.event import subscribers

from mailman.interfaces.member import SubscriptionEvent


logger = logging.getLogger("mailman.plugins")


def mlist_to_json(mlist):
    return {
        "id": mlist.list_id,
        "name": mlist.list_name,
        "host": mlist.mail_host,
    }


def member_to_json(member):
    return {
        "id": member.member_id,
        "user_id": member.user_id,
        "address": {
            "email": member.address.email,
            "name": member.address.display_name,
        },
    }


def init():
    cfg = external_configuration(
        config.plugin.mailman_rest_event.configuration)
    event_webhook_url = cfg.get("general", "webhook_url")

    if not event_webhook_url:
        logger.info("Webhook URL not set, will not be sending events")
        return

    logger.info(f"Webhook URL: {event_webhook_url}")

    handlers = {
        SubscriptionEvent: (lambda evt: {
            "event": "user_subscribed",
            "mlist": mlist_to_json(evt.mlist),
            "member": member_to_json(evt.member)
        })
    }

    def handle_event(evt):
        t = type(evt)
        if t in handlers:
            try:
                logger.info(f"Posting: {type(evt)}")
                result = requests.post(event_webhook_url, json=handlers[t](evt))
                logger.info(f"Result: {result.status_code}")
            except Exception as e:
                logger.error(f"Failed to post: {e}")

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
