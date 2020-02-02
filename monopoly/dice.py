from random import randint

from constants import NUMBER_FACES


class Dice:
    def __init__(self, number_of_faces: int = NUMBER_FACES):
        self.number_of_faces = number_of_faces

    def roll(self) -> int:
        return randint(1, self.number_of_faces)
