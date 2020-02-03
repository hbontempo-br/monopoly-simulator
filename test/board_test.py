import unittest

from monopoly.board import Board
from monopoly.real_state import RealState


number_of_spaces = 1_000
min_real_state_price = 100
max_real_state_price = 200
min_real_state_rent_price_proportion = 50
max_real_state_rent_price_proportion = 100


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(
            number_of_spaces=number_of_spaces,
            min_real_state_price=min_real_state_price,
            max_real_state_price=max_real_state_price,
            min_real_state_rent_price_proportion=min_real_state_rent_price_proportion,
            max_real_state_rent_price_proportion=max_real_state_rent_price_proportion,
        )

    def test_board_size(self):
        self.assertEqual(number_of_spaces, len(self.board.spaces), "wrong board size")

    def test_all_spaces_have_real_state(self):
        for space in self.board.spaces:
            self.assertIsInstance(space, RealState, "space doesnt contain a RealState")

    def test_check_method(self):
        for index, real_state in enumerate(self.board.spaces):
            self.assertEqual(
                self.board.check_space(position=index),
                real_state,
                "check method is returning wrong real_state",
            )

    def test_real_state_prices(self):
        for real_state in self.board.spaces:
            self.assertGreaterEqual(
                real_state.price,
                min_real_state_price,
                "generated RealState has a lower price than the minimum requested",
            )
            self.assertLessEqual(
                real_state.price,
                max_real_state_price,
                "generated RealState has a higher price than the maximum requested",
            )

    def test_real_state_rent(self):
        # Loose validation, not important to be REALLY precise
        for real_state in self.board.spaces:
            proportion = round((real_state.rent_value / real_state.price), 1)
            self.assertGreaterEqual(
                proportion,
                min_real_state_rent_price_proportion / 100,
                "generated RealState has a lower rent than the minimum requested",
            )
            self.assertLessEqual(
                proportion,
                max_real_state_rent_price_proportion / 100,
                "generated RealState has a higher rent than the maximum requested",
            )

    def test_distinct_real_states(self):
        unique_real_state = set(self.board.spaces)
        self.assertEqual(
            len(unique_real_state),
            len(self.board.spaces),
            "not all real_states are unique",
        )

    def test_new_position_no_around_the_board(self):
        new_position, around_the_board_count = self.board.new_position(
            current_position=1, spaces_to_move=1
        )
        self.assertEqual(new_position, 2, "wrong new position")
        self.assertEqual(around_the_board_count, 0, "wrong around the board count")

    def test_new_position_around_the_board(self):
        new_position, around_the_board_count = self.board.new_position(
            current_position=number_of_spaces - 1, spaces_to_move=1
        )
        self.assertEqual(new_position, 0, "wrong new position")
        self.assertEqual(around_the_board_count, 1, "wrong around the board count")

    def test_new_position_multiple_around_the_board(self):
        new_position, around_the_board_count = self.board.new_position(
            current_position=0, spaces_to_move=3 * number_of_spaces
        )
        self.assertEqual(new_position, 0, "wrong new position")
        self.assertEqual(around_the_board_count, 3, "wrong around the board count")
