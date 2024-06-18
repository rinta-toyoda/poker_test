from app.models.cards import Card, Suit
from app.models.role import RoleType
from app.models.player import Player

class RoleService():
    @staticmethod
    def decide_winner(players: list[Player]) -> None:
        players_role_type = [player.role.role_type for player in players]
        for role_type in RoleType:
            if role_type in players_role_type:
                highest_role_players = [player for player in players if player.role.role_type == role_type]
                if len(highest_role_players) == 1:
                    return highest_role_players
                else:
                    return _compare_highest_role_players(highest_role_players)

    def __init__(self, hand: list[Card], cards_on_table: list[Card]) -> None:
        cards: list[Card] = hand + cards_on_table

        card_number_mapping = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9":[], "10": [], "11": [], "12": [], "13": []}
        card_suit_mapping = {Suit.HEARTS.value: [], Suit.DIAMONDS.value: [], Suit.SPADES.value: [], Suit.CLUBS.value: []}
        for card in cards:
            card_number_mapping[str(card.number)].append(card)
            card_suit_mapping[str(card.suit.value)].append(card)

        self._card_number_mapping: dict[str, list[Card]] = card_number_mapping
        self._card_suit_mapping: dict[str, list[Card]] = card_suit_mapping
        self._flush_cards: list[Card] = []
        self._pair_list: list[list[Card]] = []
        self._three_of_a_kind_list: list[list[Card]] = []

    def set_flush_cards(self, cards: list[Card]) -> None:
        self._flush_cards = cards

    def check_role(self) -> tuple[RoleType, list[Card]]:
        for cards in self._card_suit_mapping.values():
            if len(cards) == 5:
                sorted_cards = sorted(cards, key=lambda card: card.number)
                sorted_number = [card.number for card in sorted_cards]
                if sorted_number == [1, 10, 11, 12, 13]:
                    return RoleType.ROYAL_FLUSH, sorted_cards
                if set([sorted_number[index+1] - sorted_number[index] for index in range(len(cards)-1)]) == {1}:
                    return RoleType.STRAIGHT_FLUSH, sorted_cards
                self.set_flush_cards(sorted_cards)

        # Lists for checking straight later
        number_list = []
        card_list = []

        for number, cards in self._card_number_mapping.items():
            if len(cards) == 4:
                return RoleType.FOUR_OF_A_KIND, cards
            elif len(cards) == 3:
                self._three_of_a_kind_list.append(cards)
            elif len(cards) == 2:
                self._pair_list.append(cards)

            if len(cards) >= 1:
                number_list.append(int(number))
                card_list.append(cards[0])

        # Check FUll House
        if len(self._three_of_a_kind_list) == 2:
            return RoleType.FULL_HOUSE, self._three_of_a_kind_list[0][0:2] + self._three_of_a_kind_list[1]
        if len(self._three_of_a_kind_list) == 1 and len(self._pair_list) >= 1:
            return RoleType.FULL_HOUSE, self._pair_list[-1] + self._three_of_a_kind_list[0]

        # Check Flush
        if self._flush_cards:
            return RoleType.FLUSH, self._flush_cards

        # Check Straight
        if 1 in number_list and 10 in number_list and 11 in number_list and 12 in number_list and 13 in number_list:
            cards = [card_list[number_list.index(10)], card_list[number_list.index(11)], card_list[number_list.index(12)], card_list[number_list.index(13)], card_list[number_list.index(1)]]
            return RoleType.STRAIGHT, cards

        number_diffs = [number_list[index+1] - number_list[index] for index in range(len(number_list)-1)]
        if number_diffs.count(1) >= 5:
            indexes = sorted([i for i, x in enumerate(number_diffs) if x == 1], reverse=True)
            cards = [card_list[indexes[i]] for i in range(5)]
            return RoleType.STRAIGHT, cards

        # Check Three of a Kind
        if len(self._three_of_a_kind_list) == 1:
            return RoleType.THREE_OF_A_KIND, self._three_of_a_kind_list[0]

        # Check Two Pairs
        if len(self._pair_list) >= 2:
            return RoleType.TWO_PAIRS, self._pair_list[-2] + self._pair_list[-1]

        # Check One Pair
        if len(self._pair_list) == 1:
            return RoleType.ONE_PAIR, self._pair_list[0]

        # No Pair
        cards = card_list[-2:] if card_list[0].number != 1 else card_list[-1] + card_list[0]
        return RoleType.NO_PAIR, card_list[-2:]

def _get_highest_number_players(players: list[Player], highest_card_numbers: list[int] | None = None) -> list[Player]:
        if highest_card_numbers is None:
            highest_card_numbers = [player.role.cards[-1].number if player.role.cards[0] != 1 else 14 for player in players]
        max_indexes = [index for index, number in enumerate(highest_card_numbers) if number == max(highest_card_numbers)]

        higest_number_players = []
        for index in max_indexes:
            higest_number_players.append(players[index])
        return higest_number_players

def _compare_highest_role_players(highest_role_players: list[Player]) -> list[Player]:
    role_type = highest_role_players[0].role.role_type

    if role_type == RoleType.ROYAL_FLUSH:
        return highest_role_players
    elif role_type == RoleType.FULL_HOUSE:
        highest_card_numbers = [player.role.cards[-1].number for player in highest_role_players]
        return _get_highest_number_players(highest_role_players, highest_card_numbers)
    else:
        return _get_highest_number_players(highest_role_players)