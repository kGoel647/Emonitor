import logging
import logging.config

#Sets up the logger function
logging.config.fileConfig('backend/logger.cfg', disable_existing_loggers=False)
logging.getLogger().setLevel(30)
logger = logging.getLogger(__name__)
logger.log(logging.INFO, "Logger Initialized")
