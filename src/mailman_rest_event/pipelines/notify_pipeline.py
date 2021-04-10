from mailman.config import config
from mailman.interfaces.pipeline import IPipeline
from public import public
from zope.interface import implementer
import logging

logger = logging.getLogger("mailman.plugins")

logger.info("Initing pipeline")

@public
@implementer(IPipeline)
class NotifyPipeline:
    name = 'notify-pipeline'
    description = 'The built-in posting pipeline with notify support.'

    def __init__(self):
        logger.info(f"Pipelines: {config.pipelines}")

    def __iter__(self):
        """See `IPipeline`."""
        yield from config.pipelines["default-posting-pipeline"]._handlers
