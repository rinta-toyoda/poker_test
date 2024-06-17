from app.models.cards import Card, Deck
from app.models.player import Player
from app.models.action import Action, ActionType

class Poker():
    def __init__(self) -> None:
        self._deck: Deck = Deck()
        self._players: dict[str, Player] = {}
        self._player_num: int = 0
        self._minimal_bets: int = 0
        self._total_bets: int = 0

    def set_players(self, players: dict) -> None:
        self._players = players

    def set_player_num(self, num: int) -> None:
        self._player_num = num

    def set_minimal_bets(self, minimal_bets: int) -> None:
        self._minimal_bets = minimal_bets

    def set_total_bets(self, total_bets: int) -> None:
        self._total_bets = total_bets

    def draw_card(self) -> Card:
        card_num = self._deck.card_num
        self._deck.set_card_num(card_num - 1)

        deck_cards = self._deck.cards
        card = deck_cards.pop()
        self._deck.set_cards(deck_cards)
        return card

    def initialize_deck(self) -> None:
        self._deck = Deck()

    def initialize_players(self, players: list[Player], starting_index: int = 0) -> None:
        self._player_num = len(self._players)
        player_dict = dict()
        players = players[starting_index:] + players[:starting_index] if starting_index > 0 else players
        for player in players:
            starting_hand = self.starting_hand()
            player.set_hand(starting_hand)
            player.set_dropped(False)
            player_dict[player.name] = player
        self.set_players(player_dict)

    def starting_hand(self) -> set[Card]:
        card1 = self.draw_card()
        card2 = self.draw_card()
        return set([card1, card2])

    def initialize_round(self, players: list[Player], starting_index: int = 0) -> None:
        self.initialize_players(players, starting_index)
        self.initialize_deck()

        # small blind
        small_blind_action = Action(players[starting_index-2].name, action_type=ActionType.RAISE, amount=1)
        self.commit_action(small_blind_action)

        # big blind
        big_blind_action = Action(players[starting_index-1].name, action_type=ActionType.RAISE, amount=2)
        self.commit_action(big_blind_action)


    def commit_action(self, action: Action) -> None:
        if action.action_type == ActionType.CALL:
            self._total_bets += action.amount
            player_chips = self._players[action.player_name].chips
            self._players[action.player_name].set_chips(player_chips - action.amount)
        elif action.action_type == ActionType.RAISE:
            self._total_bets += action.amount
            self._minimal_bets = action.amount
            player_chips = self._players[action.player_name].chips
            self._players[action.player_name].set_chips(player_chips - action.amount)
        elif action.action_type == ActionType.FOLD:
            self._players[action.player_name].set_dropped(True)