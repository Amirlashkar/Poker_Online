from django.db import models
from Login.models import User    


class Game(models.Model):
    stage = models.IntegerField(max_length=50, default=1)
    board_cards = models.CharField(max_length=50, default=None)


class GameUserState(models.IntegerChoices):
    satout = 0, "satout"
    action_needed = 1, "action_needed"
    fold = 2, "fold"
    check = 3, "check"
    called = 4, "called"
    raised = 5, "raised"


class Wins(models.IntegerChoices):
    highcard = 0, "highcard"
    onepair = 1, "onepair"
    twopair = 2, "twopair"
    threekind = 3, "threekind"
    straight = 4, "straight"
    flush = 5, "flush"
    fullhouse = 6, "fullhouse"
    fourkind = 7, "fourkind"
    straightflush = 8, "straightflush"


class GameUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(choices=GameUserState.choices, default=GameUserState.satout,
                                             null=True, blank=True, primary_key=False, editable=True)
    card1 = models.CharField(max_length=10)
    card2 = models.CharField(max_length=10)
    ingame_money = models.IntegerField(max_length=50)
    current_win = models.PositiveSmallIntegerField(choices=Wins.choices ,default=Wins.highcard, 
                                                   null=True, blank=True, primary_key=False, editable=True)