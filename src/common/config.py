from attr import dataclass


@dataclass
class TicketPlusConfig:
    # ticket website info
    default_page: str
    ticket_count: int
    priority_zone_index: int

    # account info
    phone: str
    country: str
    country_index: int
    password: str


@dataclass
class TixcraftConfig:
    # ticket website info
    target_page: str

    # account info
    facebook_account: str
    facebook_password: str

    # interns
    num_of_interns: int
