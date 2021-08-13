from mailman.config import config
from mailman.core.i18n import _
from mailman.interfaces.handler import IHandler
from public import public
from zope.interface import implementer
from zope.event import notify


@public
class HandledMessageEvent:
    def __init__(self, mlist, msg, msgdata):
        self.mlist = mlist
        self.msg = msg
        self.msgdata = msgdata


@public
@implementer(IHandler)
class ToEvent:
    name = "to-event"
    description = "Reports message as an event for other plugins to use"

    def process(self, mlist, msg, msgdata):
        notify(HandledMessageEvent(mlist, msg, msgdata))
