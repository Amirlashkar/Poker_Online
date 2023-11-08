from typing import Set
from enum import StrEnum
import random, re


class Kind(StrEnum):
    Clubs = "Clubs"
    Hearts = "Hearts"
    Diamonds = "Diamonds"
    Spades = "Spades"


class Card:
    def __init__(self):
        self._num:int = 0
        self.kind:Kind
        self.is_shown:bool

    def naming(self, num, kind) -> str:
        if num == 1:
            return f"<A of {kind}>"
        elif num == 11:
            return f"<Juvenile of {kind}>"
        elif num == 12:
            return f"<Queen of {kind}>"
        elif num == 13:
            return f"<King of {kind}>"
        else:
            return f"<{num} of {kind}>"
    
    def expr2feats(self, expression:str):
        num_pattern = r"(\d+)"
        num = re.findall(num_pattern, expression)
        if num:
            self.num = num
        else:
            if "A" in expression:
                self.num = 1
            elif "Juvenile" in expression:
                self.num = 11
            elif "Queen" in expression:
                self.num = 12
            elif "King" in expression:
                self.num = 13
        
        kind_pattern = r"([A-Z])"
        kind = re.findall(kind_pattern, expression)
        if "A" in kind:
            del kind[0]

        kind = kind[0]
        if "C" in kind:
            self.kind = Kind.Clubs
        elif "H" in kind:
            self.kind = Kind.Hearts
        elif "D" in kind:
            self.kind = Kind.Diamonds
        elif "S" in kind:
            self.kind = Kind.Spades
            
    def __str__(self) -> str:
        return self.naming(self.num, self.kind)
    
    def __repr__(self) -> str:
        return self.naming(self.num, self.kind)


class Cards:
    def __init__(self):
        self.unchosen:Set[Card] = set()
        self.chosen:Set[Card] = set()

        self.create_set_of_cards()
    
    def create_set_of_cards(self):
        kinds = set([Kind.Clubs, Kind.Hearts, Kind.Spades, Kind.Diamonds])
        nums = set(range(1, 14))
        
        cards = set()
        for kind in kinds:
            for num in nums:
                card = Card()
                card.kind = kind
                card.num = num
                card.is_shown = False
                cards.add(card)
        
        cards = list(cards)
        random.shuffle(cards)
        self.unchosen = set(cards)

    def choose_a_card(self):
        card = random.sample(list(self.unchosen), 1)[0]
        card.is_shown = True

        self.unchosen.remove(card)
        self.chosen.add(card)

        return card