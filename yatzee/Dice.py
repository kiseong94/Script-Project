import random

class Dice:

    def rollDice(self):
        self.roll = random.randint(1, 6)

    def getRoll(self):
        return self.roll