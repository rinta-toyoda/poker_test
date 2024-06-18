from unittest import TestCase

from app.models.cards import Card, Suit
from app.models.role import RoleType, Role
from app.models.player import Player, PlayerFactory
from app.service.role import RoleService
from app.service.poker import PokerService

class TestRoleService(TestCase):
    def test_decide_winner(self) -> None:
        player1 = PlayerFactory.create_player(name="Player 1", chips=100)
        player2 = PlayerFactory.create_player(name="Player 2", chips=100)
        player3 = PlayerFactory.create_player(name="Player 3", chips=100)
        player4 = PlayerFactory.create_player(name="Player 4", chips=100)

        player2_role = Role(role_type=RoleType.STRAIGHT, cards=[Card(Suit.DIAMONDS, 1), Card(Suit.DIAMONDS, 2), Card(Suit.HEARTS, 3), Card(Suit.CLUBS, 4), Card(Suit.HEARTS, 5)])
        player2.set_role(player2_role)
        player3_role = Role(role_type=RoleType.NO_PAIR, cards=[Card(Suit.CLUBS, 10), Card(Suit.CLUBS, 1)])
        player3.set_role(player3_role)
        player4_role = Role(role_type=RoleType.TWO_PAIRS, cards=[Card(Suit.CLUBS, 10), Card(Suit.HEARTS, 10), Card(Suit.CLUBS, 1), Card(Suit.HEARTS, 1)])
        player4.set_role(player4_role)


        # Pattern1: Player 1 wins with higher role
        player1_role = Role(role_type=RoleType.FULL_HOUSE, cards=[Card(Suit.CLUBS, 10), Card(Suit.DIAMONDS, 10), Card(Suit.CLUBS, 2), Card(Suit.DIAMONDS, 2), Card(Suit.HEARTS, 2)])
        player1.set_role(player1_role)

        winners = RoleService.decide_winner([player1, player2, player3, player4])
        self.assertEqual(winners, [player1])

        # Pattern2: Player 1 wins with same role as player 2 but with higher card number
        player1_role = Role(role_type=RoleType.STRAIGHT, cards=[Card(Suit.DIAMONDS, 2), Card(Suit.HEARTS, 3), Card(Suit.CLUBS, 4), Card(Suit.HEARTS, 5), Card(Suit.DIAMONDS, 6)])
        player1.set_role(player1_role)

        winners = RoleService.decide_winner([player1, player2, player3, player4])
        self.assertEqual(winners, [player1])

        # Pattern3: Player 1 and Player 2 wins with the same role
        player1_role = Role(role_type=RoleType.STRAIGHT, cards=[Card(Suit.DIAMONDS, 1), Card(Suit.DIAMONDS, 2), Card(Suit.HEARTS, 3), Card(Suit.CLUBS, 4), Card(Suit.HEARTS, 5)])
        player1.set_role(player1_role)

        winners = RoleService.decide_winner([player1, player2, player3, player4])
        self.assertEqual(winners, [player1, player2])


    def test_check_role(self) -> None:
        player1 = PlayerFactory.create_player(name="Player 1", chips=100)
        player1.set_hand([Card(Suit.DIAMONDS, 1), Card(Suit.DIAMONDS, 2)])

        poker_service = PokerService()
        poker_service.add_cards_on_table([Card(Suit.DIAMONDS, 3), Card(Suit.DIAMONDS, 4), Card(Suit.DIAMONDS, 5), Card(Suit.CLUBS, 1), Card(Suit.CLUBS, 2)])

        role_service = RoleService(player1.hand, poker_service.cards_on_table)
        role_type, cards = role_service.check_role()
        self.assertEqual(role_type, RoleType.STRAIGHT_FLUSH)
        for index, card in enumerate(cards):
            number = index + 1
            self.assertEqual(card.number, number)
            self.assertEqual(card.suit, Suit.DIAMONDS)