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
            logger.info(f"Pipeline: {name}")
            try:
                handler_names = [ h.name for h in pipeline._handlers ]
                if "to-archive" in handler_names and "to-notify" not in handler_names:
                    logger.info(f"Added to-notify to {name}")
                    pipeline._handlers.append(config.handlers["to-notify"])
            except Exception as e:
                logger.error(f"Error: {e}")

    def __iter__(self):
        """See `IPipeline`."""
        yield from config.pipelines["default-posting-pipeline"]._handlers
