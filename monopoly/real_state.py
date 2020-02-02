from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from monopoly.player import BasePlayer


class RealState:
    def __init__(self, price: int, rent_value: int):
        self.price = price
        self.rent_value = rent_value
        self.owner = None

    def bought(self, player: BasePlayer) -> NoReturn:
        self.owner = player
