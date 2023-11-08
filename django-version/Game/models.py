from django.db import models
from Login.models import User    


class PlayerState(models.IntegerChoices):
    satout = 0, "satout"
    action_needed = 1, "action_needed"
    fold = 2, "fold"
    check = 3, "check"
    called = 4, "called"
    raised = 5, "raised"
    allin = 6, "allin"


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


class Game(models.Model):
    stage = models.IntegerField(max_length=50, default=1, null=True)
    board_cards = models.CharField(max_length=50, default=None, null=True)
    lowest_stage_money = models.IntegerField(max_length=50)
    agregated_money = models.IntegerField(max_length=50, default=None, null=True)
    first_player_of_turn = models.IntegerField(max_length=50, default=None, null=True)
    first_player_of_game = models.IntegerField(max_length=50, default=None, null=True)


class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, 
                             null=True, 
                             related_name='users')
    
    is_turn = models.BooleanField(default=False)
    onboard_money = models.IntegerField(max_length=50)
    state = models.PositiveSmallIntegerField(choices=PlayerState.choices, 
                                            default=PlayerState.satout,
                                            null=True, blank=True, primary_key=False, 
                                            editable=True)

    card1 = models.CharField(max_length=10, null=True)
    card2 = models.CharField(max_length=10, null=True)
    ingame_money = models.IntegerField(max_length=50, null=True)
    current_win = models.PositiveSmallIntegerField(choices=Wins.choices ,default=Wins.highcard,
                                                   null=True, blank=True, primary_key=False, 
                                                   editable=True)