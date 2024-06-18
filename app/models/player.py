from app.models.cards import Card
from app.models.role import Role

class Player():
    def __init__(self, name: str, chips: int):
        self._name: str = name
        self._chips: int = chips
        self._hand: list[Card] = []
        self._dropped: bool = False
        self._role: Role | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def chips(self) -> int:
        return self._chips

    @property
    def role(self) -> Role:
        return self._role

    @property
    def hand(self) -> list[Card]:
        return self._hand

    def set_chips(self, chips: int) -> None:
        self._chips = chips

    def set_hand(self, hand: list[Card]) -> None:
        self._hand = hand

    def set_dropped(self, dropped: bool) -> None:
        self._dropped = dropped

    def set_role(self, role: Role) -> None:
        self._role = role

    def is_dropped(self) -> bool:
        return self._dropped

class PlayerFactory():
    @staticmethod
    def create_player(name: str, chips: int) -> Player:
        return Player(name=name, chips=chips)