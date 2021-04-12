import logging
import requests
from mailman.config import config
from mailman.config.config import external_configuration
from mailman.interfaces.plugin import IPlugin
from public import public
from zope.interface import implementer
from zope.event import subscribers

from mailman.interfaces.member import SubscriptionEvent, UnsubscriptionEvent
from mailman_rest_event.handlers.to_event import HandledMessageEvent
from mailparser import MailParser

logger = logging.getLogger("mailman.plugins")


def mlist_to_json(mlist):
    return {
        "id": mlist.list_id,
        "name": mlist.list_name,
        "host": mlist.mail_host,
    }


def member_to_json(member):
    return {
        "user_id": member.user_id,
        "address": {
            "email": member.address.email,
            "name": member.address.display_name,
        },
    }


def message_to_obj(msg):
    msg_obj = MailParser(msg)
    if msg_obj.mail.get("date"):
        msg_obj.mail["date"] = msg_obj.date.isoformat()
    return msg_obj.mail


def init():
    cfg = external_configuration(
        config.plugin.mailman_rest_event.configuration)
    event_webhook_url = cfg.get("general", "webhook_url", fallback=None)
    try:
        timeout = int(cfg.get("general", "timeout", fallback=2))
    except:
        timeout = 2
    auth_user = cfg.get("auth", "user", fallback=None)
    auth_key = cfg.get("auth", "key", fallback=None)

    auth = None
    if auth_user and auth_key:
        auth = (auth_user, auth_key)

    if not event_webhook_url:
        logger.info("Webhook URL not set, will not be sending events")
        return

    logger.info(f"Webhook URL: {event_webhook_url}")

    handlers = {
        SubscriptionEvent: (lambda evt: {
            "event": "user_subscribed",
            "mlist": mlist_to_json(evt.mlist),
            "member": member_to_json(evt.member)
        }),
        UnsubscriptionEvent: (lambda evt: {
            "event": "user_unsubscribed",
            "mlist": mlist_to_json(evt.mlist),
            "member": member_to_json(evt.member)
        }),
        HandledMessageEvent: (lambda evt: {
            "event": "new_message",
            "mlist": mlist_to_json(evt.mlist),
            "message": message_to_obj(evt.msg)
        }),
    }

    def handle_event(evt):
        t = type(evt)
        if t in handlers:
            try:
                logger.info(f"Posting: {type(evt)}")
                result = requests.post(
                    event_webhook_url,
                    json=handlers[t](evt),
                    auth=auth,
                    timeout=timeout)
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
