#!/usr/bin/env python
#-*- conding:utf-8 -*-

import statistics
import numpy as np
import csv
import os.path

import logger

log = logger.Logger('skating')

class Player:
    def __init__(self, _num, _name):
        self.number = _num # 背番号
        self.name = _name # 名前
        self.score = 0 # 確定順位
        self.order = [] # 審査結果
        self.majorityNum = 0 # 多数決継続数
        self.sumSuperiorNum = 0 # 上位加算結果

    def setOrder(self, _order):
        self.order.append(_order)

    def printPropaty(self):
        print("number         : " + str(self.number))
        print("name           : " + str(self.name))
        print("score          : " + str(self.score))
        print("order          : " + str(self.order))
        print("majorityNum    : " + str(self.majorityNum))
        print("sumSuperiorNum : " + str(self.sumSuperiorNum))

# 同着処理
# 対象リストに対して、同着順位を付与する
# 引数
#   1, 対象リスト
#   2, 決定順位
def same_score(_players, _deside_num):
    log.debug("start same_score")

    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    for player in _players:
        print("背番号" + str(player.number) + " : "+ str(_deside_num) +"位(同着)")

        player.score = _deside_num
    
    log.debug("end same_score")


# 下位比較
# 対象リストに対して、下位比較を行い順位を付与する
# 順位を確定できない場合、対象者を同着とする
# 引数
#   1, 対象リスト
#   2, 決定順位
def compare_subordinate(_players, _deside_num):
    log.debug("start compare_subordinate")

    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    # 再帰処理終了
    if len(_players) <= 0:
        log.debug("end compare_subordinate")
        return
    elif len(_players) == 1:
        # 対象者が1人のため、順位を確定する
        print("背番号" + str(_players[0].number) + " : "+ str(_deside_num) +"位(下位比較)")
        _players[0].score = _deside_num

        return

    center = int(len(_players[0].order)/2) # + 1

    compareSubordinate_list = []
    for player in _players:
        player.order.sort()

        subordinate_num = []
        for i in range(center, len(player.order)-1):
            subordinate_num.append(player.order[i])

        compareSubordinate_list.append(subordinate_num)

    compareSubordinate_list =  np.array(compareSubordinate_list).T.tolist()

    check_list = []
    for i in range(0,len(compareSubordinate_list)):
        # 転置したリストに対して、
        # 最小値の個数 と リストの長さ を比較し
        # 異なった場合、最小値を持つ選手を抽出する
        if len(compareSubordinate_list[i]) != compareSubordinate_list[i].count(min(compareSubordinate_list[i])):
            check_list = [player for player in _players if player.order[center + i] == min(compareSubordinate_list[i])]
            break
        
        # 対象者が完全一致の場合、
        # 同着とする
        if i == len(compareSubordinate_list):
            log.debug("下位比較 完全一致")

            check_list = _players


    if len(check_list) == 1:
        # 最大値が一つであれば、その値を持つ選手に順位を決定する
        print("背番号" + str(check_list[0].number) + " : "+ str(_deside_num) +"位(下位比較)")
        check_list[0].score = _deside_num

    # 複数ある場合は、同着処理を行う
    elif  len(check_list) > 1:
        # 同着処理へ
        same_score(check_list, _deside_num)
    else :
        # TODO 不要か確認するためにログを出力する
        log.debug("下位比較 check_listが0以下")

        check_list = _players
        same_score(check_list, _deside_num)

    _players =  list( set(_players) ^ set(check_list))
    
    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)
    compare_subordinate(_players,_deside_num)

# 上位加算
# 対象リストに対して、上位加算を行い順位を付与する
# 順位を確定できない場合、対象者に対して下位比較を行う
# 引数
#   1, 対象リスト
#   2, 決定順位
def total_superior(_players, _deside_num):
    log.debug("start total_superior")

    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    # 再帰処理終了
    if len(_players) <= 0:
        log.debug("end total_superior")
        return

    center = int(len(_players[0].order)/2) # + 1

    for player in _players:
        player.order.sort()

        # 中央値から右側を比較していき、その時の数を計算する
        player.sumSuperiorNum = 0
        for i in range(0,center):
            player.sumSuperiorNum += player.order[i]
        
        # print("name:" +  player.name)
        # print("sumSuperiorNum:" +  str(player.sumSuperiorNum))

    sumSuperiorNumList = []
    for player in _players:
        sumSuperiorNumList.append(player.sumSuperiorNum)

    # 過半数の対象者を抽出するため、初期化する
    check_list = []
    check_list = [player for player in _players if player.sumSuperiorNum == min(sumSuperiorNumList) ]

    # 上位加算による最大値が1件である場合、
    # 順位が確定する
    if len(check_list) == 1:
        # 最大値が一つであれば、その値を持つ選手に順位を決定する
        print("背番号" + str(check_list[0].number) + " : "+ str(_deside_num) +"位(上位加算)")
        check_list[0].score = _deside_num
        
    # 複数ある場合は、下位比較加算を行う
    else :
        # 下位比較へ
        compare_subordinate(check_list, _deside_num)

    # 対象差集合をset()を用いて取得する
    _players =  list( set(_players) ^ set(check_list))

    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)
    total_superior(_players,_deside_num)

# 多数決
# 対象リストに対して、多数決を行い順位を付与する
# 順位を確定できない場合、対象者に対して上位加算を行う
# 引数
#   1, 対象リスト
#   2, 決定順位
def majority(_players, _deside_num):

    log.debug("start majority")
    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    # 再帰処理終了
    if len(_players) <= 0:
        log.debug("end majority")
        return

    # インデックスとして使用するため +1 しない
    # TODO 審査員が偶数の場合に対応できるようにする
    center = int(len(_players[0].order)/2) # + 1

    for player in _players:
        player.order.sort()

        # 中央値から右側を比較していき、その時の数を計算する
        player.majorityNum = 0
        for j in range(1,center-1):
            
            if player.order[center + j] == player.order[center]:

                player.majorityNum += 1
            else :
                # 比較した結果が異なる場合、対象選手の過半数の計上は終了する
                break

    # 各選手の多数決の数をリストに格納する
    majority_list = []
    for player in _players:
        majority_list.append(player.majorityNum)
    
    # 多数決による最大値が1件である場合、
    # 順位が確定する
    # 過半数の対象者を抽出するため、初期化する
    check_list = []
    check_list = [player for player in _players if player.majorityNum == max(majority_list) ]

    if len(check_list) == 1:
        # 最大値が一つであれば、その値を持つ選手に順位を決定する
        print("背番号" + str(check_list[0].number) + " : "+ str(_deside_num) +"位(多数決)")
        check_list[0].score = _deside_num

    # 複数ある場合は、上位加算を行う
    elif len(check_list) > 1:
        # 上位加算へ
        total_superior(check_list, _deside_num)

    # 対象差集合をset()を用いて取得する
    _players =  list( set(_players) ^ set(check_list))

    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)
    majority(_players,_deside_num)



# スケーティング表読み込みマネージャ

# -> ファイル読み込み

# -> 直接入力

# 過半数(中央値)
# 対象リストに対して、過半数比較を行い順位を付与する
# 順位を確定できない場合、対象者に対して多数決を行う
# 引数
#   1, 対象リスト
#   2, 決定順位
def median(_players, _deside_num):

    log.debug("start median")
    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    # 再帰処理終了
    if len(_players) <= 0:
        log.debug("end median")
        return
    
    # 過半数の対象者を抽出するため、初期化する
    check_list = []

    # 対象者抽出
    fetch_num = 1
    while True:
        for player in _players:
            if statistics.median(player.order) == fetch_num:
                check_list.append(player)

        if len(check_list) == 0:
            # 対象者がいないため、抽出する順位を一つ下げる
            fetch_num += 1
        elif len(check_list) > 0:
            break


    if len(check_list) == 1:
        # 順位の付与
        # チェック対象者からの削除
        check_list[0].score = _deside_num
        print("背番号" + str(check_list[0].number) + " : "+ str(_deside_num) +"位(過半数)")

    elif len(check_list) > 1:
        # 対象者に対して多数決の検証をする
        majority(check_list, _deside_num)

    # 対象差集合をset()を用いて取得する
    _players =  list( set(_players) ^ set(check_list))

    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)
    median(_players,_deside_num)

# スケーティング処理開始
def skating(_player_list):
    # 中央値比較を1位から順に決定する
    median(_player_list, 1)

def main():

    # 仮の選手情報
    testPlayer1 = Player(10,"Tanaka")
    testPlayer2 = Player(20,"Sato")
    testPlayer3 = Player(30,"Suzuki")
    testPlayer4 = Player(40,"Morita")
    testPlayer5 = Player(50,"Oda")
    testPlayer6 = Player(60,"Naritake")

    player_list = [testPlayer1,
                   testPlayer2,
                   testPlayer3,
                   testPlayer4,
                   testPlayer5,
                   testPlayer6
                   ]

    # ジャッジ数には奇数を設定する
    # TODO 観客みんなで審査できるように大きな数を入れても問題ないようにする。
    #      現在は1501で10秒ほどかかる
    judge_num = 9

    # 審査結果入力の変わりにランダム値を入れる
    order = list(range(1,len(player_list) + 1))
    rand_order = []
    for i in range(judge_num):
        rand_order = np.random.choice(order, size=6, replace=False)
        for j in range(6):
            player_list[j].setOrder(rand_order[j])

    # 審査結果を表示する
    print("審査内容")
    for player in player_list:
        print(str(player.number) + ":" + str(sorted(player.order)))

    # スケーティング開始
    skating(player_list)
    
    # コンソール結果出力
    print("スケーティング結果")
    for player in player_list:
        print("背番号" +  str(player.number) + " : " +  str(player.score) + "位")

    # csv出力
    if os.path.isfile("./output/csv/skating_result.csv") :
        # 対話形式で確認
        while True:
            print("すでにファイルが存在します。上書きしますか？")
            inp = input("[Y]es/[N]o? >> ").lower()
            if inp in ("y", "yes", "n", "no"):
                inp = inp.startswith("y") # inp[0] == 'y'と同義
                                        # string.startwithは最初の文字列を調べる
                break
            print("Error! Input again.")

        if inp == False:
            print("csv出力せずに終了")
            return

    print("csvファイルを出力")
    with open("./output/csv/skating_result.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["skating result"])
        writer.writerow(["name","number","score","order",])
        for player in player_list:
            player_row = []
            player_row.append(player.name)
            player_row.append(player.number)
            player_row.append(player.score)
            player_row.extend(player.order)
            writer.writerow(player_row)

if __name__ == '__main__':
    main()
