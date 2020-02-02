from __future__ import annotations

import random
from typing import NoReturn, TYPE_CHECKING

from constants import INITIAL_AMOUNT

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from monopoly.real_state import RealState


class BasePlayer:
    def __init__(self, name: str, initial_amount: int = INITIAL_AMOUNT):
        self.name = name
        self.amount = initial_amount
        self.position = 0
        self.has_loosed = False
        self.real_states = []
        self.description = f"{name} ({self.__class__.__name__})"

    def decide(self, real_state_price: int, real_state_rent_value: int) -> bool:
        raise NotImplementedError("BasePlayer doesnt have a defined buying behaviour")

    def __has_money(self, required_amount: int) -> int:
        return self.amount > required_amount

    def decide_to_buy(self, real_state: RealState) -> NoReturn:
        if not self.__has_money(required_amount=real_state.price):
            return
        should_buy = self.decide(
            real_state_price=real_state.price,
            real_state_rent_value=real_state.rent_value,
        )
        if should_buy:
            self.__buy_real_state(real_state=real_state)

    def __remove_money(self, amount: int) -> NoReturn:
        self.amount = self.amount - amount

    def add_money(self, amount: int) -> NoReturn:
        self.amount = self.amount + amount

    def new_position(self, position: int) -> NoReturn:
        self.position = position

    def __buy_real_state(self, real_state: RealState) -> NoReturn:
        self.real_states.append(real_state)
        self.__remove_money(amount=real_state.price)
        real_state.bought(player=self)

    def pay_rent(self, real_state: RealState) -> NoReturn:
        if self.__has_money(required_amount=real_state.rent_value):
            amount = real_state.rent_value
        else:
            amount = self.amount
            self.__loose()
        self.__transfer_money(receiver=real_state.owner, amount=amount)

    def __transfer_money(self, receiver: BasePlayer, amount: int) -> NoReturn:
        self.__remove_money(amount=amount)
        receiver.add_money(amount=amount)

    def __loose(self) -> NoReturn:
        # TODO: should the properties go to the "bank"?
        self.has_loosed = True


class RandomPlayer(BasePlayer):
    def decide(self, real_state_price: int, real_state_rent_value: int) -> bool:
        return random.choice([True, False])


class ImpulsivePlayer(BasePlayer):
    def decide(self, real_state_price: int, real_state_rent_value: int) -> bool:
        return True


class DemandingPlayer(BasePlayer):
    def __init__(self, name: str, initial_amount: int = 300, min_rent_value: int = 50):
        BasePlayer.__init__(self, name=name, initial_amount=initial_amount)
        self.min_rent_value = min_rent_value

    def decide(self, real_state_price: int, real_state_rent_value: int) -> bool:
        if real_state_rent_value > self.min_rent_value:
            return True
        return False


class CautiousPlayer(BasePlayer):
    def __init__(
        self, name: str, initial_amount: int = 300, min_reserve_amount: int = 80
    ):
        BasePlayer.__init__(self, name=name, initial_amount=initial_amount)
        self.min_reserve_amount = min_reserve_amount

    def decide(self, real_state_price: int, real_state_rent_value: int) -> bool:
        if real_state_rent_value > self.min_reserve_amount:
            return True
        return False
