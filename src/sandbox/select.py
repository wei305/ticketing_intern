import logging
from asyncio import sleep

import ddddocr
from PIL import Image
from selenium.common import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.common.my_driver import MyDriver


ocr = ddddocr.DdddOcr()

counter = {
    'count': 0
}


def main():
    driver = MyDriver()
    # driver.maximize_window()
    driver.execute_script("document.body.style.zoom='60%'")
    driver.get('https://tixcraft.com/ticket/ticket/24_yugyeom/17676/1/49')

    # close consent
    reject_all = driver.retry_find_element('button#onetrust-reject-all-handler')
    reject_all.click()
    while True:
        try:
            execution(driver)
        except UnexpectedAlertPresentException:
            pass
        sleep(1)


def execution(driver):
    quantity = driver.retry_find_element('#TicketForm_ticketPrice_01')
    print(quantity)
    select = Select(quantity)
    print(select)
    print(f"options len: {len(select.options)}")
    for option in select.options:
        print(option)

    # try to select max quantity
    select.select_by_index(len(select.options) - 1)

    # check agreement
    agreement = driver.retry_find_element('#TicketForm_agree')
    driver.enforce_click(agreement)
    enter_captcha(driver)
    submit = driver.retry_find_element('.btn-primary')
    driver.enforce_click(submit)
    check_alert(driver)


def check_alert(driver):
    try:
        alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
        sleep(1)
        alert.accept()
    except TimeoutException as e:
        pass


def enter_captcha(driver):
    temp_file = '/tmp/captcha.png'
    selector = 'img#TicketForm_verifyCode-image'
    captcha = driver.retry_find_element(selector)
    cond = EC.visibility_of_any_elements_located((By.CSS_SELECTOR, selector))
    try:
        # wait for the captcha image to finish loading
        WebDriverWait(driver, 5).until(cond)
        captcha.screenshot(temp_file)
    except TimeoutException as e:
        logging.error('timeout', e)

    img = Image.open(temp_file)

    result = ocr.classification(img)
    logging.info(f'ocr: {result}')
    captcha_input = driver.retry_find_element('input#TicketForm_verifyCode')
    counter['count'] += 1
    if counter['count'] >= 3:
        captcha_input.send_keys(result)
    else:
        captcha_input.send_keys("faker")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main()
