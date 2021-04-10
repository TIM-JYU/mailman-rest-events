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
    description = 'A dummy pipeline that injects to_notify handler to other pipelines.'

    def __init__(self):
        for name, pipeline in config.pipelines.items():
            try:
                if "to-archive" in pipeline._handlers and "to-notify" not in pipeline._handlers:
                    logger.info(f"Added to-notify to {pipeline.name}")
                    pipeline._handlers.append("to-notify")
            except:
                pass

    def __iter__(self):
        """See `IPipeline`."""
        yield from config.pipelines["default-posting-pipeline"]._handlers
