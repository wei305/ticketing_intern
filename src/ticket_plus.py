import logging
import traceback
from time import sleep

import yaml
from selenium.webdriver import Keys

from src.common.audio_util import play_audio_async
from src.common.config import TicketPlusConfig
from src.common.excluded_keywords import excluded_keywords
from src.common.my_driver import MyDriver
from src.common.state import State, CurrentState


class TicketPlus:

    def __init__(self, config: TicketPlusConfig):
        self.config = config
        self.driver = MyDriver()
        self.state = CurrentState()
        self.is_first_confirm = True

    def setup_browser(self):
        self.driver.get(self.config.default_page)
        self.driver.maximize_window()
        self.driver.execute_script("document.body.style.zoom='60%'")
        logging.info(f'driver.title: {self.driver.title}')
        assert 'Ticket Plus遠大售票系統' in self.driver.title

    def login(self):
        # login
        login_btn = self.driver.retry_find_element('div.v-toolbar__content > div > div > button')
        login_btn.click()

        country_code_input = self.driver.retry_find_element('div.country-selector > input')

        # hard-coded the index of taiwan country code
        country_code_input.send_keys(Keys.ARROW_DOWN)
        for i in range(self.config.country_index):
            country_code_input.send_keys(Keys.ARROW_UP)
        country_code_input.send_keys(Keys.ENTER)

        phone_input = self.driver.retry_find_element('div.input-tel > input')
        phone_input.send_keys(self.config.phone)

        pwd_input = self.driver.retry_find_element('div.v-text-field__slot > input')
        pwd_input.send_keys(self.config.password)

        login_button = self.driver.retry_find_element('form.v-form > button.nextBtn')
        login_button.click()
        self.state.set_state(State.LOGIN)

    def handle_event(self):
        logging.info(f'enter page: {self.driver.title}')
        event_list = self.driver.retry_find_elements('div#buyTicket > div.sesstion-item > div.row')
        for event in event_list:
            button = event.retry_find_element('button')
            button.click()
            self.state.set_state(State.EVENT_ENTERED)

    def handle_seat(self):
        # select seat
        if self.state.get_state() == State.ORDER_SENT:
            sleep(0.5)
            return

        logging.info(f'enter page: {self.driver.title}')
        seat_list = self.driver.retry_find_elements('div.seats-area > div')

        index = self.config.priority_zone_index
        for seat in seat_list[index:] + seat_list[:index]:
            if any(keyword in seat.text for keyword in excluded_keywords()):
                continue  # skip the seat if it contains the excluded keyword

            seat_expansion = seat.retry_find_element('button')
            seat_expansion.click()
            expansion_content = seat.retry_find_element('div.v-expansion-panel-content')
            sleep(0.2)
            if '開賣時間' in expansion_content.text:
                self.driver.refresh()
                return
            if '已售完' not in expansion_content.text:
                plus = expansion_content.retry_find_element('button.light-primary-2')
                for i in range(self.config.ticket_count):
                    plus.ignore_click_intercepted()
                next_step_btn = self.driver.retry_find_element('div.order-footer').retry_find_element('button.nextBtn')
                next_step_btn.click()
                self.state.set_state(State.ORDER_SENT)
                return

    def handle_confirm(self):
        if self.is_first_confirm:
            logging.info(f'enter page: {self.driver.title}')
            play_audio_async()

            self.is_first_confirm = False
            self.state.set_state(State.ORDER_ENTERED)


def main():
    config = TicketPlusConfig(**load_yaml())
    app = TicketPlus(config)
    app.setup_browser()
    app.login()

    while True:
        url = app.driver.current_url
        try:
            if 'activity' in url:
                app.handle_event()
            elif 'order' in url:
                app.handle_seat()
            elif 'confirm' in url:
                app.handle_confirm()

        except Exception as e:
            print(traceback.format_exc())
            logging.error(f'get error at {app.state.get_state()}, error: {e}')


def load_yaml():
    with open("config.yaml") as stream:
        return yaml.safe_load(stream)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Running against ticket plus...")

    main()
