from enum import Enum

class ActionType(Enum):
    CALL = "call"
    RAISE = "raise"
    FOLD = "fold"


class Action():
    def __init__(self, player_name: str, action_type: ActionType, amount: int) -> None:
        self._player_name = player_name
        self._action_type = action_type
        self._amount = amount

    @property
    def player_name(self) -> str:
        return self._player_name

    @property
    def action_type(self) -> ActionType:
        return self._action_type

    @property
    def amount(self) -> int:
        return self._amount