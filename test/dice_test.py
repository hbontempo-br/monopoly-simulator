import unittest

from monopoly.dice import Dice

number_of_faces = 10
test_quantity = 100_000


class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(number_of_faces=10)

    def test_roll_values(self):
        for i in range(test_quantity):
            value = self.dice.roll()
            self.assertGreaterEqual(
                value, 1, "dice roll lower than 1",
            )
            self.assertLessEqual(
                value, number_of_faces, "dice roll greater than the number of faces",
            )
