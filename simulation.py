import logging
import sys

from constants import SIMULATIONS_QUANTITY
from monopoly.board import Board
from monopoly.dice import Dice
from monopoly.game import Game
from monopoly.player import (
    RandomPlayer,
    CautiousPlayer,
    DemandingPlayer,
    ImpulsivePlayer,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

study_cases = [
    [RandomPlayer, CautiousPlayer],
    [RandomPlayer, DemandingPlayer],
    [RandomPlayer, ImpulsivePlayer],
    [CautiousPlayer, RandomPlayer],
    [CautiousPlayer, DemandingPlayer],
    [CautiousPlayer, ImpulsivePlayer],
    [DemandingPlayer, RandomPlayer],
    [DemandingPlayer, CautiousPlayer],
    [DemandingPlayer, ImpulsivePlayer],
    [ImpulsivePlayer, RandomPlayer],
    [ImpulsivePlayer, CautiousPlayer],
    [ImpulsivePlayer, DemandingPlayer],
]

simulations_quantity = SIMULATIONS_QUANTITY


def main():
    for case_index, study_case in enumerate(study_cases):

        # Print output header
        print(
            "\n________________________________________________________________________________"
        )
        print(f"\n --  STUDY CASE {case_index + 1}  --")
        study_players = [
            (f"Player{ind + 1} ({player.__name__})", player.__name__)
            for ind, player in enumerate(study_case)
        ]
        print(f"\nPlayers: {[player[0] for player in study_players]}")
        print("Executing simulations...")

        # Execute simulations
        results = []
        for simulation in range(simulations_quantity):
            # Print progress bar
            prog_bar(simulation + 1, simulations_quantity, 30)

            # Instantiate new players
            players = [
                player(f"Player{ind + 1}") for ind, player in enumerate(study_case)
            ]
            # Instantiate new dice
            dice = Dice()
            # Instantiate new board
            board = Board()
            # Instantiate new game
            game = Game(board=board, dice=dice, players=players)

            # Run a simulation
            winner, rounds, timeout = game.simulate()

            results.append(
                {
                    "winner_type": winner.__class__.__name__,
                    "rounds": rounds,
                    "timeout": timeout,
                }
            )

        # Results analisys
        timout_count = sum(1 for result in results if result["timeout"] is True)
        average_rounds = round(
            sum(result["rounds"] for result in results) / len(results), 2
        )
        wins = {}
        for player_description, player_type in study_players:
            wins[player_description] = sum(
                1 for result in results if result["winner_type"] == player_type
            )
        # TODO: What about a tie?
        max_win_count = 0
        best_player = None
        for player_description, win_count in wins.items():
            if win_count > max_win_count:
                best_player = player_description
                max_win_count = win_count

        # Print results
        print("\n\nResults:")
        print(f"  - timeouts: {timout_count}")
        print(f"  - avarage round count: {average_rounds}")
        print("  - wins:")
        for player_description, win_count in wins.items():
            print(
                f"    - {player_description}: {round(win_count / len(results) * 100, 2)}%"
            )
        print(f"  - best behaviour: {best_player}")


# Copied from https://geekyisawesome.blogspot.com/2016/07/python-console-progress-bar-using-b-and.html
def prog_bar(curr, total, full_progbar):
    frac = curr / total
    filled_progbar = round(frac * full_progbar)
    print(
        "\r",
        "#" * filled_progbar + "-" * (full_progbar - filled_progbar),
        "[{:>7.2%}]".format(frac),
        end="",
    )


if __name__ == "__main__":
    main()
