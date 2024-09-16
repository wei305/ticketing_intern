import logging

import ddddocr
from PIL import Image
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


ocr = ddddocr.DdddOcr(show_ad=False, beta=True)


def image_to_text(driver, selector):
    """
    screenshot the given element, and execute the OCR
    :return: text
    """

    temp_file = '/tmp/captcha.png'
    captcha = driver.retry_find_element(selector)
    cond = EC.visibility_of_any_elements_located((By.CSS_SELECTOR, selector))
    try:
        # wait for the captcha image to finish loading
        WebDriverWait(driver, 5).until(cond)
        captcha.screenshot(temp_file)
    except TimeoutException as e:
        logging.error('timeout', e)
    captcha.screenshot(temp_file)
    img = Image.open(temp_file)
    return ocr.classification(img)
