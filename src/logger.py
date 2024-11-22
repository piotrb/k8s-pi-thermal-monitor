import logging

logger = logging.getLogger("thermal-monitor")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

logger.addHandler(ch)
