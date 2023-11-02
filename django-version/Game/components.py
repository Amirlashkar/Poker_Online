class Card:
    def __init__(self) -> None:
        self.num = None
        self.kind = None
        self.shown = False

class GameUser:
    pass


class Game:
    def __init__(self):
        self.stage = 1
        self.cards = []

    def create_cards(self):
        cards = []