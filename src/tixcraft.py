import logging
import time
import traceback
from time import sleep

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from src.common.alert_util import close_alert
from src.common.audio_util import play_audio_async
from src.common.my_driver import MyDriver
from src.common.ocr_util import image_to_text


class TixCraft:
    default_page = 'https://tixcraft.com/'

    def __init__(self, config):
        self.config = config
        self.driver = MyDriver()
        self.consent_is_closed = False
        self.confirm_page_visited = False

    def setup_browser(self):
        self.driver.get(self.default_page)
        self.driver.maximize_window()
        self.driver.execute_script("document.body.style.zoom='60%'")

    def close_consent(self):
        if not self.consent_is_closed:
            reject_all = self.driver.retry_find_element('button#onetrust-reject-all-handler')
            reject_all.click()
            self.consent_is_closed = True
            time.sleep(0.75)

    def enter_captcha(self):
        selector = 'img#TicketForm_verifyCode-image'
        result = image_to_text(self.driver, selector)

        logging.info(f'ocr: {result}')
        captcha_input = self.driver.retry_find_element('input#TicketForm_verifyCode')
        captcha_input.send_keys(result)

    def login(self):
        sign_in = self.driver.retry_find_element('a.justify-content-center')
        sign_in.click()
        facebook_sign_in = self.driver.retry_find_element('#loginFacebook')
        facebook_sign_in.retry_click()
        email = self.driver.retry_find_element('#email')
        email.send_keys(self.config.facebook_account)
        password = self.driver.retry_find_element('#pass')
        password.send_keys(self.config.facebook_password)
        consent = self.driver.retry_find_element(
            '.x1ja2u2z.x78zum5.x2lah0s.x1n2onr6.xl56j7k.x6s0dn4.xozqiw3.x1q0g3np.xi112ho.x17zwfj4.x585lrc.x1403ito.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.xn6708d.x1ye3gou.xtvsq51.x1r1pt67')
        consent.retry_click()
        login_button = self.driver.retry_find_element('#loginbutton')
        login_button.click()
        continue_button = self.driver.retry_find_element(
            '.x1ja2u2z.x78zum5.x2lah0s.x1n2onr6.xl56j7k.x6s0dn4.xozqiw3.x1q0g3np.xi112ho.x17zwfj4.x585lrc.x1403ito.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.xn6708d.x1ye3gou.xtvsq51.x1r1pt67')
        continue_button.click()
        WebDriverWait(self.driver, 5).until(expected_conditions.url_contains(self.default_page))

    def execute(self):
        def handle_events():
            events = self.driver.retry_find_elements('#gameList > table > tbody > tr')

            # TODO: [P2] only select a target date
            # TODO: [P1] select the event randomly
            # TODO: [P1] avoid to choose the unavailable event
            for event in events:
                find_tickets_button = event.retry_find_element('button')
                find_tickets_button.click()

                seats = self.driver.retry_find_elements('.area-list > li > a')
                for seat in seats:
                    seat.ignore_click_intercepted()

        def handle_tickets():
            quantity = self.driver.retry_find_element('#TicketForm_ticketPrice_01')

            # select max quantity
            select = Select(quantity)
            select.select_by_index(len(select.options) - 1)

            # check agreement
            agreement = self.driver.retry_find_element('#TicketForm_agree')
            self.driver.enforce_click(agreement)

            # enter_captcha
            self.enter_captcha()

            # click submit button
            submit = self.driver.retry_find_element('.btn-primary')
            self.driver.enforce_click(submit)

            close_alert(self.driver)

        def handle_confirm():
            if not self.confirm_page_visited:
                play_audio_async()
                self.confirm_page_visited = True
                sleep(1)

        self.driver.get(self.config.target_page)
        while True:
            url = self.driver.current_url
            try:
                if '/activity/detail' in url:
                    self.driver.get(url.replace('detail', 'game'))
                elif '/activity/game' in url:
                    handle_events()
                elif '/ticket/ticket' in url:
                    handle_tickets()
                elif '/ticket/order' in url:
                    handle_confirm()

            except Exception as e:
                print(traceback.format_exc())
                logging.error(f'get error: {e}')
