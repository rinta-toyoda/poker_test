from app.models.cards import Card

class Player():
    def __init__(self, name: str, chips: int):
        self._name: str = name
        self._chips: int = chips
        self._hand: set[Card] = None
        self._dropped: bool = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def chips(self) -> int:
        return self._chips

    def set_chips(self, chips: int) -> None:
        self._chips = chips

    def set_hand(self, hand: set[Card]) -> None:
        self._hand = hand

    def set_dropped(self, dropped: bool) -> None:
        self._dropped = dropped

    def is_dropped(self) -> bool:
        return self._dropped

class PlayerFactory():
    @staticmethod
    def create_player(name: str, chips: int) -> Player:
        return Player(name=name, chips=chips)