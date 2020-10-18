import logging
import coloredlogs
import sys
from time import ctime

def setup():
    """Setups logging."""
    FORMAT = u'%(levelname)-8s [%(asctime)s]  %(message)s ### %(filename)s[LINE:%(lineno)d]'

    logger = logging.getLogger()

    logger.addHandler(
        logging.StreamHandler())
    logger.addHandler(
        logging.FileHandler(
            f"logs/{ctime()}.log"))
    

    coloredlogs.install(level='INFO',
            fmt=FORMAT,
            logger=logger)

    logging.getLogger("discord").setLevel(logging.WARNING)