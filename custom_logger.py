import os
import sys
import logging

import structlog

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL_PARAMETER = 'LOG_LEVEL'
LOG_DESTINATION_PARAMETER = 'LOG_DESTINATION'

STD_OUTPUTS = {
    'stdout': sys.stdout,
    'stderr': sys.stderr,
}

LOG_LEVELS = {
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'WARNING': logging.WARN,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

log_level = LOG_LEVELS.get(os.getenv(LOG_LEVEL_PARAMETER, logging.CRITICAL))
log_destination = os.getenv(LOG_DESTINATION_PARAMETER, 'stdout')

if log_destination in STD_OUTPUTS:
    logging.basicConfig(
        stream=STD_OUTPUTS[log_destination],
        format='%(message)s',
        level=log_level
    )
else:
    logging.basicConfig(
        filename=log_destination,
        format='%(message)s',
        level=log_level
    )

logger = structlog.getLogger()

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", key="timestamp_iso_utc"),
        structlog.processors.TimeStamper(fmt=None, key="timestamp_epoch_time"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
