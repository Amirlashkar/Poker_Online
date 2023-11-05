from models import *


def next_turn(user:GameUser, game:Game, ids:list):
    users = game.users.all()

    if ids.index(user.id) == len(ids) - 1:
        user.is_turn = False
        user.save()
    else:
        user.is_turn = False
        user.save()
        
        for id in ids[ids.index(user.id) + 1:]:
            u = users.get(id=id)
            if u.state not in (GameUserState.fold, GameUserState.allin):
                break
        
        u.is_turn = True
        u.save()
            

    ids = ids[1:] + ids[0]
    return ids


# stages have some repeatitive states
def check(user:GameUser, game:Game, ids:list):
    if game.lowest_stage_money == user.onboard_money:
        user.state = GameUserState.check
        user.save()

        next_turn(user, game, ids)
    else:
        return "Call or Fold!"


def fold(user:GameUser, game:Game, ids:list):
    user.state = GameUserState.fold
    user.save()

    next_turn(user, game, ids)


def raise_(user:GameUser, game:Game, ids:list, amount:int):
    if amount == user.ingame_money:
        user.state = GameUserState.allin
    else:
        user.state = GameUserState.raised

    user.onboard_money += amount
    user.save()

    game.lowest_stage_money = user.onboard_money
    game.save()

    next_turn(user, game, ids)


def call(user:GameUser, game:Game, ids:list):
    diff = game.lowest_stage_money - user.onboard_money
    user.onboard_money = game.lowest_stage_money
    user.ingame_money -= diff
    user.save()

    next_turn(user, game, ids)