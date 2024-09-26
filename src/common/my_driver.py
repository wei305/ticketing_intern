from typing import List

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.common.my_web_element import MyWebElement
from src.common.retry import retry


def _get_options() -> Options:
    options = Options()
    options.set_capability('pageLoadStrategy', "eager")
    options.add_experimental_option("detach", True)
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-translate')
    options.add_argument('--lang=zh-TW')
    options.add_argument('--disable-web-security')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    return options


class MyDriver(WebDriver):
    def __init__(self) -> None:
        super().__init__(options=_get_options())

    def _find_elements(self, value):
        elements = self.find_elements(By.CSS_SELECTOR, value)
        if len(elements) > 0:
            wrapper_list = []
            for element in elements:
                wrapper_list.append(MyWebElement(element))
            return wrapper_list
        return None

    def retry_find_elements(self, value, retries=-1) -> List[MyWebElement]:
        return retry(lambda: self._find_elements(value), retries)

    def retry_find_element(self, value, retries=-1):
        web_element = retry(lambda: self.find_element(By.CSS_SELECTOR, value), retries)
        if web_element is not None:
            return MyWebElement(web_element)
        return None

    # use javascript to enforce clicking the button
    def enforce_click(self, element):
        self.execute_script("arguments[0].click();", element)
