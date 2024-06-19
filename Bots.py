import random

class RSP_Bot():
    def __init__(self, botName) -> None:
        self.choices = ["R", "P", "S"]
        self.botName = botName

    def make_move(self):
        self.computer_choice = random.choice(self.choices)
        return self.computer_choice