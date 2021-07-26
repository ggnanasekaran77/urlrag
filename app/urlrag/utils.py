"""
Utilis methods for urlrag module
"""
import os.path
from csv import reader
import logging
import coloredlogs


# get root logger
logger = logging.getLogger(__name__)

coloredlogs.install(fmt='%(asctime)s,%(msecs)03d - %(name)-15s - %(levelname)-6s - %(message)s')


class LoggerService:

    @staticmethod
    def info(msg):
        logger.info(msg)

    @staticmethod
    def warn(msg):
        logger.warning(msg)

    @staticmethod
    def error(msg):
        logger.error(msg)


def get_file_path(url):

    return url.replace('file://', '')


def file_path_validation(url):
    """for the given input validating file"""
    file_path = get_file_path(url)

    return os.path.isfile(file_path)


def file_header_validation(url):
    """CSV header validation. Headers should be name,url"""
    file_path = get_file_path(url)

    with open(file_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)

        if header[0] == 'name' and header[1] == 'url':
            return True
        else:
            return False


def sample_csv():
    """Sample CSV file"""
    data = '''name,url
google,https://www.google.com'''

    return data
