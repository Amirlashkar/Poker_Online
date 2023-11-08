from models import *


def start_game(player:Player, game:Game):
    pass


def next_turn(player:Player, game:Game):

    users = game.users.all()
    ids = [u.id for u in users]
    first_player = [id for id in ids if id == game.first_player_of_turn][0]
    ids = ids[ids.index(first_player):] + ids[:ids.index(first_player)]

    if ids.index(player.id) == len(ids) - 1:
        player.is_turn = False
        player.save()
    else:
        player.is_turn = False
        player.save()
        
        for id in ids[ids.index(player.id) + 1:]:
            u = users.get(id=id)
            if u.state not in (PlayerState.fold, PlayerState.allin):
                break
        
        u.is_turn = True
        u.save()


# stages have some repeatitive states
def check(player:Player, game:Game):
    if game.lowest_stage_money == player.onboard_money:
        player.state = PlayerState.check
        player.save()

        next_turn(player, game)
    else:
        return "Call or Fold!"


def fold(player:Player, game:Game):
    player.state = PlayerState.fold
    player.save()

    next_turn(player, game)


def raise_(player:Player, game:Game, amount:int):
    if amount == player.ingame_money:
        player.state = PlayerState.allin
    else:
        player.state = PlayerState.raised

    player.onboard_money += amount
    player.save()

    game.lowest_stage_money = player.onboard_money
    game.save()

    next_turn(player, game)


def call(player:Player, game:Game):
    diff = game.lowest_stage_money - player.onboard_money
    player.onboard_money = game.lowest_stage_money
    player.ingame_money -= diff
    player.save()

    next_turn(player, game)


# winning strategies
def player_win(player:Player, game:Game) -> Wins:
    card1 = player.card1