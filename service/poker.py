from poker_test.models.cards import Card, Deck

class Poker():
    def __init__(self) -> None:
        self._deck: Deck = Deck()

    def draw_card(self) -> Card:
        card_num = self._deck.card_num
        self._deck.set_card_num(card_num - 1)

        deck_cards = self._deck.cards
        card = deck_cards.pop()
        self._deck.set_cards(deck_cards)

        return card