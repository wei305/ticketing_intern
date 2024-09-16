from selenium.common import TimeoutException
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.support.wait import WebDriverWait


def close_alert(driver, timeout=2):
    try:
        alert = WebDriverWait(driver, timeout).until(alert_is_present())
        alert.accept()
    except TimeoutException as e:
        pass
