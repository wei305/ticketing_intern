import logging
import time

import ddddocr
from PIL import Image

from src.common.my_driver import MyDriver


ocr = ddddocr.DdddOcr()


class TixCraft:
    def __init__(self):
        self.driver = MyDriver()
        self.consent_is_closed = False

    def setup_browser(self):
        self.driver.get('https://tixcraft.com/')
        self.driver.maximize_window()
        # self.driver.execute_script("document.body.style.zoom='60%'")
        logging.info(f'driver.title: {self.driver.title}')

    def close_consent(self):
        if not self.consent_is_closed:
            reject_all = self.driver.retry_find_element('button#onetrust-reject-all-handler')
            reject_all.click()
            self.consent_is_closed = True
            time.sleep(0.75)

    def enter_captcha(self):
        temp_file = '/tmp/captcha.png'
        captcha = self.driver.retry_find_element('img#TicketForm_verifyCode-image')
        captcha.screenshot(temp_file)
        img = Image.open(temp_file)

        result = ocr.classification(img)
        logging.info(f'ocr: {result}')
        captcha_input = self.driver.retry_find_element('input#TicketForm_verifyCode')
        captcha_input.send_keys(result)


def main():
    app = TixCraft()
    app.setup_browser()
    app.close_consent()
    # app.enter_captcha()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Running against tixcraft...")

    main()
