from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def close_alert(driver, timeout=2):
    try:
        alert = WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert.accept()
    except TimeoutException as e:
        pass
