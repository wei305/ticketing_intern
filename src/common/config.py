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
    target_page: str = 'https://tixcraft.com/activity/detail/24_yugyeom'
    ticket_count: int = None

    # account info
    facebook_account: str = 'partyhousetw@gmail.com'
    facebook_password: str = 'vi_movie'
