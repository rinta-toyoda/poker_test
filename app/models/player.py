from app.models.cards import Deck

class Player():
    def __init__(self, name: str, chips: int):
        self._name = name
        self._chips = chips
        self._chips_bet = 0

    def set_chips(self, chips: int) -> None:
        self._chips = chips

    def set_chips_bet(self, chips_bet: int) -> None:
        self._chips_bet = chips_bet

class PlayerFactory():
    @staticmethod
    def create_player(name: str, chips: int) -> Player:
        return Player(name=name, chips=chips)