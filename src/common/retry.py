import logging
import time

from selenium.common import NoSuchElementException


def retry(func, retries=-1, delay=0.25, *args):
    count = 0
    while retries == -1 or count < retries:
        try:
            result = func(*args)
            if result:
                return result
        except NoSuchElementException as e:
            logging.debug(f'Retrying due to: {e.msg}')
        count += 1
        time.sleep(delay)
    logging.error(f'Failed after {retries} retries.')
    return None
