from enum import Enum

class State(Enum):
    NOT_STARTED = 0
    LOGIN = 1
    EVENT_ENTERED = 2
    ORDER_SENT = 3
    ORDER_ENTERED = 4

class CurrentState:
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state