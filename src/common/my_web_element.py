import logging
import time
from asyncio import sleep

from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.common.retry import retry


class MyWebElement(WebElement):
    def __init__(self, element: WebElement):
        super().__init__(element.parent, element.id)

    def _find_elements(self, value):
        elements = self.find_elements(By.CSS_SELECTOR, value)
        if len(elements) > 0:
            wrapper_list = []
            for element in elements:
                wrapper_list.append(MyWebElement(element))
            return wrapper_list
        return None

    def retry_find_elements(self, value=None, retries=-1):
        return retry(lambda: self._find_elements(value), retries)

    def retry_find_element(self, value=None, retries=-1):
        web_element = retry(lambda: self.find_element(By.CSS_SELECTOR, value), retries)
        return MyWebElement(web_element)

    def retry_click(self):
        while True:
            try:
                self.click()
                return
            except ElementNotInteractableException as e:
                logging.debug(f'click intercepted: {e}')
            time.sleep(0.2)

    def click_and_forget(self):
        try:
            self.click()
        except Exception as e:
            logging.warning(f'click intercepted: {e}')
