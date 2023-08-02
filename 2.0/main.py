from functions import *
import pandas as pd

def generate_game_results(n):
    for _ in range(n):
        slot_winning, win_list = start_base_game(bet_amount=1)
        if isinstance(win_list, list) and win_list:
            yield slot_winning, tuple(win_list)

def run_multiple_games_with_numpy(n):
    total_slot_winning = 0
    hits = {}

    for slot_winning, win_combination in generate_game_results(n):
        if win_combination in hits:
            hits[win_combination] += 1
        else:
            hits[win_combination] = 1
        total_slot_winning += slot_winning

    average_slot_winning = total_slot_winning / n

    return average_slot_winning, hits

n = 10000000  # 根據需要設置 n 的值。
average_slot_winning, hits = run_multiple_games_with_numpy(n)
print("平均 Slot 贏得金額：", average_slot_winning)
print("中獎組合次數：", hits)









