import random
from enum import Enum

class Suit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    SPADES = "spades"
    CLUBS = "clubs"

class Card():
    def __init__(self, suit: Suit, num: int) -> None:
        self.suit = suit
        self.num = num

class Deck():
    def __init__(self) -> None:
        hearts = [Card(Suit.HEARTS, i) for i in range(1, 14)]
        diamonds = [Card(Suit.DIAMONDS, i) for i in range(1, 14)]
        spades = [Card(Suit.SPADES, i) for i in range(1, 14)]
        clubs = [Card(Suit.CLUBS, i) for i in range(1, 14)]
        unshuffled_cards = hearts + diamonds + spades + clubs
        shuffled_cards = random.shuffle(unshuffled_cards)

        self._card_num = len(shuffled_cards)
        self._cards = set(shuffled_cards)

    @property
    def cards(self) -> set[Card]:
        return self._cards

    @property
    def card_num(self) -> int:
        return self._card_num

    def set_cards(self, cards: list[Card]) -> None:
        self._cards = cards

    def set_card_num(self, card_num: int) -> None:
        self._card_num = card_num
