from __future__ import annotations

import logging
from typing import List, NoReturn, TYPE_CHECKING

from constants import MAX_ROUNDS, AROUND_BOARD_BONUS

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from monopoly.board import Board
    from monopoly.dice import Dice
    from monopoly.player import BasePlayer


class Game:
    def __init__(
        self,
        board: Board,
        dice: Dice,
        players: List[BasePlayer],
        max_rounds: int = MAX_ROUNDS,
        around_the_board_bonus: int = AROUND_BOARD_BONUS,
    ):
        self.board = board
        self.dice = dice
        self.all_players = players
        self.active_players = players
        self.max_rounds = max_rounds
        self.around_the_board_bonus = around_the_board_bonus
        self.winner = None

    def simulate(self) -> NoReturn:

        logging.debug(msg="Starting new game")
        logging.debug(
            msg=f"Players: {[player.description for player in self.active_players]}",
        )

        for current_round in range(1, self.max_rounds + 1):

            self.__play_round()
            winner = self.__check_for_winner()
            if winner:
                return winner, current_round, False

        winner = self.__find_winner()

        logging.log(
            level=logging.DEBUG,
            msg=f"Winner: {winner.description} / Round: {current_round}",
        )

        return winner, current_round, True

    def __find_winner(self) -> BasePlayer:

        max_amount = 0
        possible_winners = []

        # Filter players with max cash
        for player in self.active_players:
            if player.amount > max_amount:
                max_amount = player.amount
                possible_winners = [player.amount]
            if player.amount == max_amount:
                possible_winners.append(player)

        # Get the first on to play that has the maximum amount
        for player in self.all_players:
            if player in possible_winners:
                return player

    def __play_round(self) -> NoReturn:

        # Get current Player
        current_player = self.active_players.pop(0)

        # Dice is rolled
        dice_roll = self.dice.roll()
        # Move Player
        new_position, cycles_around_board = self.board.new_position(
            current_position=current_player.position, spaces_to_move=dice_roll
        )

        # Verify if player has cycled the board
        if cycles_around_board > 0:
            # Player get around the Board bonus
            current_player.add_money(
                amount=cycles_around_board * self.around_the_board_bonus
            )
        current_player.new_position(position=new_position)
        # Checks position RealState
        current_real_state = self.board.check_space(position=new_position)

        # If RealState has no owner Player
        if current_real_state.owner is None:
            current_player.decide_to_buy(real_state=current_real_state)

        # If RealState is owned by another Player
        elif current_real_state.owner is not current_player:
            current_player.pay_rent(real_state=current_real_state)

        if not current_player.has_loosed:
            self.active_players.append(current_player)

    def __check_for_winner(self) -> BasePlayer:

        # Check if there is only one player left
        if len(self.active_players) == 1:
            winner = self.active_players[0]
            return winner
