from enum import Enum

from app.models.cards import Card

class RoleType(Enum):
    ROYAL_FLUSH = "royal_flush"
    STRAIGHT_FLUSH = "straight_flush"
    FOUR_OF_A_KIND = "four_of_a_kind"
    FULL_HOUSE = "full_house"
    FLUSH = "flush"
    STRAIGHT = "straight"
    THREE_OF_A_KIND = "three_of_a_kind"
    TWO_PAIRS = "two_pair"
    ONE_PAIR = "one_pair"
    NO_PAIR = "no_pair"

class Role():
    def __init__(self, role_type: RoleType, cards: list[Card]) -> None:
        self.role_type = role_type
        self.cards = cards