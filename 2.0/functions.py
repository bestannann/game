from constant import *
#裝飾器
def Decorator(func):
    return func

#檢查符合哪些中獎組合
def checkwin_case(index,pattern,win_case,slot_result):  #index:檢查第幾列中的元素  pattern:圖案 win_case:可能的中獎組合
    if index > 4:
        return [pattern*index]
    if pattern == "M1": #假設最左邊的那個圖案是百搭
        temp_list = {} #因為是百搭開頭，往下檢查後要檢查的圖案可能會有多種，所以需要一個暫時的list用來儲存可能要往下檢查哪些圖案
        temp_answer = []
        for i in range(len(slot_result[index])):
            if str(i) in [x[index] for x in win_case]: #檢查時只需檢查中獎組合中的第index個的值，例如 index = 2 win_case = ["11011",""11211"]，就是當i = 0 或 2時才繼續去做檢查的動作
                if slot_result[index][i] == "M1":
                    if "M1" not in temp_list: #假設預計要檢查的圖案中還沒有存百搭，就在裡面新增
                        temp_list["M1"] = [str(i)] #圖案:column中的i
                    else: #如果已經預計要檢查百搭，則新增要檢查的column的i
                        temp_list["M1"].append(str(i))
                elif slot_result[index][i] != "C1": 
                    if index == 4:      #前4個百搭且第五個不是百搭
                        temp_answer += [pattern*index]  
                    if slot_result[index][i] not in temp_list:
                            temp_list[slot_result[index][i]] = [str(i)]
                    else:
                            temp_list[slot_result[index][i]].append(str(i))

        for key,value in temp_list.items():
            temp_win_case = [x for x in win_case if x[index] in value]
            temp_answer += checkwin_case(index + 1,key,temp_win_case,slot_result)
        return temp_answer

    else: #假設最左邊的那個圖案不是百搭
        temp_right_list = []
        for i in range(len(slot_result[index])):
            if slot_result[index][i] == pattern or slot_result[index][i] == "M1":
                temp_right_list.append(str(i))
        win_case = [x for x in win_case if x[index] in temp_right_list] #減少檢查的case，不可能的中獎組合不再重複檢查了
        if len(win_case) == 0:
            if index > 1:
                return [pattern*index]
            else:
                return []
        return checkwin_case(index + 1,pattern,win_case,slot_result)

#檢查是否觸發免費轉盤
def check_free_row(slot_result):
    if "C1" in slot_result[1] and "C1" in slot_result[2] and "C1" in slot_result[3]:
        return True
    else :
        return False
	
#	count = 0
#	for column in slot_result:
#		if "C1" in column:
#			count += 1
#	if count == 3:

#	elif count == 4:

#	elif count == 5:

#檢查哪幾列是locked
def check_locked(slot_result,locked = None):
    if not locked:
        locked = []
    for i in range(len(slot_result)):
        if i not in locked and slot_result[i][0] == "M1" and slot_result[i][-1] == "M1": #檢查有沒有新的column需要被固定，如果有則將column的index新增進locked中
            locked.append(i) #在locked中新增需要被lock住的column的index
    for i in locked: #根據locked中的index將需要被固定住的column的符號全部替換成百搭
        slot_result[i] = ["M1" for i in range(len(slot_result[i]))]
    return (slot_result,locked)
	

#透過查表得到所有中獎組合中最高的賠率
def calculate_winnings(win_list,bet_amount):
    if len(win_list) == 0:
        max_odds = 0
    else:
        max_odds = 0
        # 透過查表得到所有中獎組合中最高的賠率
        for win_combination in win_list:
            if win_combination in odds_table:
                max_odds = max(max_odds, odds_table[win_combination])
    return bet_amount*max_odds

def checkresult(bet_amount,slot_result,locked = None,type = "normal",free_game_count = 0,free_game_total_winning=0, base_free_game_max = None): #bet_amount:下注金額 slot_result:轉盤顯示的盤面  locked:儲存哪幾列需要被固定住  type:判斷是一般還是免費轉盤 free_game_count:記錄免費遊戲的執行次數
    #win_list 記錄所有中獎的組合
    player_amount =0
    win_list = []
    # if check_free_row(slot_result):  #step2 : 檢查freeGame
    #     if type == "free":
    #         player_amount = 0 #ex
    #         if base_free_game_max < free_game_max_value:
    #             base_free_game_max += per_free_game_max
    #             start_free_game(player_amount, free_game_count, base_free_game_max,free_game_total_winning=free_game_total_winning, locked = locked)
    #         else:
    #             winning = 0 #ex
    #             return winning
				
    #     else:
    #         player_amount = 0 #ex
    #         base_free_game_max < free_game_max_value
    #         start_free_game(player_amount, free_game_count, base_free_game_max, free_game_total_winning=0, locked = None)
    # slot_result,locked = check_locked(slot_result,locked)    #step3 : 根據locked中的index將需要被固定住的column的符號全部替換成百搭 & 檢查有沒有新的column需要被固定，如果有則將column的index新增進locked中
    for i in range(len(slot_result[0])): #step4 : 找出所有符合中獎線圖的組合
        win_list += checkwin_case(1,slot_result[0][i],win_case[i],slot_result)
    # print(win_list)
    # print("123")
    slot_winning = calculate_winnings(win_list,bet_amount) + player_amount
    return  slot_winning,win_list #step5 : 根據得到的中獎組合去查表得出最高的賠率並且計算玩家贏得了多少獎金

@Decorator
def start_base_game(bet_amount,locked = None):
    slot_result = test_roulette.roll_all()   #step1 : 轉動轉盤得到一個盤面
    return checkresult(bet_amount, slot_result, locked = locked)

def start_free_game(bet_amount, free_game_count, base_free_game_max, free_game_total_winning, locked=None):
    if free_game_count == 0:
        free_game_total_winning = 0
    free_game_count += 1
    slot_result = free_roulette.roll_all()
    #計算方式
    winning = checkresult(bet_amount, slot_result, type="free", free_game_count=free_game_count, locked=locked, base_free_game_max=base_free_game_max)[0]
    win_list = checkresult(bet_amount, slot_result, type="free", free_game_count=free_game_count, locked=locked, base_free_game_max=base_free_game_max)[1]
    if free_game_count < base_free_game_max:
        free_game_count += 1
        
        free_game_total_winning += winning
        
        return winning
    else: #玩到最後一場時加總獲得的總積分
        free_game_total_winning += winning
        
        return free_game_total_winning,win_list

    
#print(general_roulette.roll_all())
# slot_result = general_roulette.roll_all()
#print(slot_result)
test_case = [["M1", "M1", "M1", "M1"], 
            ["M1", "6", "11", "9"], 
            ["M1","7","11","10"], 
            ["C1", "M1", "M1", "M1"], 
            ["4", "4", "11", "7"]]
# win_list=['000']
# bet_amount=1
# print(calculate_winnings(win_list,1))
# print(check_locked(test_case))
# print(checkresult(1,test_case))