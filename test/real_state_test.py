import unittest
from unittest.mock import Mock

from monopoly.real_state import RealState

price = 10
rent_value = 1


class TestRealState(unittest.TestCase):
    def setUp(self):
        self.real_state = RealState(price=price, rent_value=rent_value)

    def test_buy_action(self):
        player = Mock()
        self.real_state.bought(player=player)
        self.assertEqual(self.real_state.owner, player)
