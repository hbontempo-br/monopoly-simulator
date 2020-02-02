from random import randint
from typing import Tuple

from constants import (
    NUMBER_SPACES,
    MIN_REAL_STATE_PRICE,
    MAX_REAL_STATE_PRICE,
    MIN_REAL_STATE_RENT_PERCENTAGE,
    MAX_REAL_STATE_RENT_PERCENTAGE,
)
from monopoly.real_state import RealState


class Board:
    def __init__(
        self,
        number_of_spaces: int = NUMBER_SPACES,
        min_real_state_price: int = MIN_REAL_STATE_PRICE,
        max_real_state_price: int = MAX_REAL_STATE_PRICE,
        min_real_state_rent_price_proportion: int = MIN_REAL_STATE_RENT_PERCENTAGE,
        max_real_state_rent_price_proportion: int = MAX_REAL_STATE_RENT_PERCENTAGE,
    ):
        self.number_of_spaces = number_of_spaces
        self.spaces = []
        # Create random RealState for the board
        for i in range(number_of_spaces):
            self.spaces.append(
                self.__random_real_state(
                    min_price=min_real_state_price,
                    max_price=max_real_state_price,
                    min_rent_percentage=min_real_state_rent_price_proportion,
                    max_rent_percentage=max_real_state_rent_price_proportion,
                )
            )

    @staticmethod
    def __random_real_state(
        min_price: int,
        max_price: int,
        min_rent_percentage: int,
        max_rent_percentage: int,
    ) -> RealState:
        price = randint(a=min_price, b=max_price)
        rent_percentage = randint(a=min_rent_percentage, b=max_rent_percentage,) // 100
        rent_value = price * rent_percentage
        real_state = RealState(price=price, rent_value=rent_value)
        return real_state

    def new_position(
        self, current_position: int, spaces_to_move: int
    ) -> Tuple[int, int]:
        new_position = (current_position + spaces_to_move) % self.number_of_spaces
        cycles_around_board = (
            current_position + spaces_to_move
        ) // self.number_of_spaces
        return new_position, cycles_around_board

    def check_space(self, position: int) -> RealState:
        return self.spaces[position]
