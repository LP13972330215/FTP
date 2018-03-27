import logging
from logging.handlers import RotatingFileHandler, SysLogHandler


class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def setup_logger(log_file, log_id):
        """
        :param log_file: output_file as you
        :param log_id: kobesystem or engine_server
        :return:
        """
        output_file = log_file
        logger = logging.getLogger(log_id)
        logger.setLevel(logging.DEBUG)
        try:
            handler = RotatingFileHandler(output_file, mode='a', maxBytes=1024 * 1024 * 10, backupCount=10)
        except Exception as e:
            handler = SysLogHandler()

        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("[%(asctime)s -%(levelname)5s- %(filename)20s:%(lineno)3s] %(message)s"))
        logger.addHandler(handler)
        return logger
