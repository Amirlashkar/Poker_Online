from models import *
from .components import *
from typing import Dict


def start_game(player:Player, game:Game):
    pass


def next_turn(player:Player, game:Game):
    players = game.players.all()
    ids = [p.id for p in players]
    first_player = [id for id in ids if id == game.first_player_of_turn][0]
    ids = ids[ids.index(first_player):] + ids[:ids.index(first_player)]

    if ids.index(player.id) == len(ids) - 1:
        player.is_turn = False
        player.save()
    else:
        player.is_turn = False
        player.save()
        
        for id in ids[ids.index(player.id) + 1:]:
            p = players.get(id=id)
            if p.state not in (PlayerState.fold, PlayerState.allin):
                break
        
        p.is_turn = True
        p.save()


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
def detect_win(player_cards:list, board_cards:list) -> Dict[Wins]:
    wins = {}
    board_kind_d = {}
    board_num_d = {}
    player_kind_d = {}
    player_num_d = {}

    for i, card in enumerate(board_cards):
        if i < 2:
            p_card_kind = player_cards[i].kind
            p_card_num = player_cards[i].num
            if player_kind_d[p_card_kind]:
                player_kind_d[p_card_kind] += 1
            else:
                player_kind_d[p_card_kind] = 1
            
            if player_num_d[p_card_num]:
                player_num_d[p_card_num] += 1
            else:
                player_num_d[p_card_num] = 1
        
        b_card_kind = card.kind
        b_card_num = card.num
        if board_kind_d[b_card_kind]:
            board_kind_d[b_card_kind] += 1
        else:
            board_kind_d[b_card_kind] = 1
        
        if board_num_d[b_card_num]:
            board_num_d[b_card_num] += 1
        else:
            board_num_d[b_card_num] = 1
    
    all_cards_num = board_num_d.copy()
    all_cards_num.update(player_num_d)
    wins[Wins.highcard] = max(list(player_num_d.keys()))

    # detecting flush
    for kind, count in list(player_kind_d.items()):
        if kind in list(board_kind_d.keys()):
            total_count = sum([count, board_kind_d[kind]])
            if total_count == 5:
                if count == 2:
                    wins[Wins.flush] = wins[Wins.highcard].copy()
                else:
                    for card in player_cards:
                        if card.kind == kind:
                            wins[Wins.flush] = card.num

    # detecting straight
    if all_cards_num[1]:
        all_cards_num[14] = all_cards_num[1].copy()
    for num, count in list(all_cards_num.items()):
        if num + 1 in all_cards_num:
            if num + 2 in all_cards_num:
                if num + 3 in all_cards_num:
                    if num + 4 in all_cards_num:
                        commons = set(range(num, num + 6)) & set(player_num_d.keys())
                        if commons:
                            wins[Wins.straight] = {"straight_range":set(range(num, num + 6)),
                                                    "player_inrange":commons}
                        break
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue

    # detecting straightflush
    if Wins.flush in wins and Wins.straight in wins:
        straight_flush = {}
        all_cards = board_cards.append(player_cards)
        for card in all_cards:
            if card.num in wins[Wins.straight]["straight_range"]:
                straight_flush.add(card.kind)

        if len(straight_flush) == 1:
            wins[Wins.straightflush] = wins[Wins.straight]["straight_range"].copy()
            del wins[Wins.flush], wins[Wins.straight]
                

    # detecting pairs
    if not Wins.straightflush in wins:
        for num, count in list(player_num_d.items()):
            if num in list(board_num_d.keys()):
                total_count = sum([count, board_num_d[num]])
                if total_count == 2:
                    if wins[Wins.onepair]:
                        wins[Wins.twopair] = num, wins[Wins.onepair]
                        del wins[Wins.onepair]
                    else:
                        wins[Wins.onepair] = num
                elif total_count == 3:
                    wins[Wins.threekind] = num
                elif total_count == 4:
                    wins[Wins.fourkind] = num
        
        # detecting fullhouse
        if Wins.onepair in wins and Wins.threekind in wins:
            wins[Wins.fullhouse] = wins[Wins.highcard].copy()

    return wins

def player_win(player:Player, game:Game) -> Wins:
    player_cards = [Card().expr2feats(player.card1), Card().expr2feats(player.card2)]
    board_cards = game.board_cards.split("><")
    board_cards = [Card().expr2feats(card) for card in board_cards]
    wins = detect_win(board_cards, player_cards)

