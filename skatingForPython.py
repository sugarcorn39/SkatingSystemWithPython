#!/usr/bin/env python
#-*- conding:utf-8 -*-

import statistics
import numpy as np
import random

import logger

log = logger.Logger('skating')

class Player:
    def __init__(self, _num, _name):
        self.number = _num
        self.name = _name
        self.score = 0
        self.order = []
        self.majorityNum = 0
        self.sumSuperiorNum = 0

    #def setScore(self, ):

    def setOrder(self, _order):
        self.order.append(_order)

    def printPropaty(self):
        print("number : " + str(self.number))
        print("name   : " + str(self.name))
        print("score  : " + str(self.score))
        print("order  : " + str(self.order))
        print("majorityNum  : " + str(self.majorityNum))
        print("sumSuperiorNum  : " + str(self.sumSuperiorNum))

# ソート関数はsorted()を使用するだけなので不要


# 同着
def sameScore(_players, _deside_num):
    log.debug("start sameScore")

    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    for player in _players:
        print("同着により"+ str(_deside_num) +"を決定しました")
        player.score = _deside_num

# 下位比較
def compareSubordinate(_players, _deside_num):
    log.debug("start compareSubordinate")

    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    # 無限ループ防止用
    if len(_players) <= 0:
        log.debug("end compareSubordinate")
        return
    elif len(_players) == 1:
        print("下位比較により"+ str(_deside_num) +"を決定しました")
        _players[0].score = _deside_num

        # 対象者が1人のため、リターンする
        return

    center = int(len(_players[0].order)/2) # + 1

    compareSubordinate_list = []
    for player in _players:
        player.order.sort()

        # 中央値から右側を比較していき、その時の数を計算する
        subordinate_num = []
        for i in range(center, len(player.order)-1):
            subordinate_num.append(player.order[i])

        compareSubordinate_list.append(subordinate_num)

    compareSubordinate_list =  np.array(compareSubordinate_list).T.tolist()

    check_list = []
    for i in range(0,len(compareSubordinate_list)):
        # print("～～～～～～～～～")
        # print(i)
        # print("compareSubordinate_list :" + str(compareSubordinate_list))
        # print("compareSubordinate_list[i] :" + str(compareSubordinate_list[i]))
        # print("min(compareSubordinate_list[i]) :" + str(min(compareSubordinate_list[i])))
        # print("compareSubordinate_list[i].count(min(compareSubordinate_list[i])) :" + str(compareSubordinate_list[i].count(min(compareSubordinate_list[i]))))

        # print("len(compareSubordinate_list) :" + str(len(compareSubordinate_list)))
        # print("len(compareSubordinate_list[i]) :" + str(len(compareSubordinate_list[i])))
        # print("～～～～～～～～～")
        if len(compareSubordinate_list[i]) != compareSubordinate_list[i].count(min(compareSubordinate_list[i])):
            check_list = [player for player in _players if player.order[center + i] == min(compareSubordinate_list[i])]
            break
        
        if i == len(compareSubordinate_list):
            check_list = _players


    if len(check_list) == 1:
        # 最大値が一つであれば、その値を持つ選手に順位を決定する
        print("下位比較により"+ str(_deside_num) +"を決定しました")
        check_list[0].score = _deside_num

    # 複数ある場合は、下位比較加算を行う
    elif  len(check_list) > 1:
        # 同着処理へ
        sameScore(check_list, _deside_num)
    else :
        check_list = _players
        sameScore(check_list, _deside_num)

    _players =  list( set(_players) ^ set(check_list))
    
    # for player in _players:
    #     player.printPropaty()

    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)

    # print("次の順位"+ str(_deside_num) + "を決定する")
    compareSubordinate(_players,_deside_num)

# 上位加算
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
        print("上位加算により"+ str(_deside_num) +"を決定しました")
        check_list[0].score = _deside_num
        
    # 複数ある場合は、下位比較加算を行う
    else :
        # 下位比較へ
        compareSubordinate(check_list, _deside_num)

    # 対象差集合をset()を用いて取得する
    _players =  list( set(_players) ^ set(check_list))

    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)
    # print("次の順位"+ str(_deside_num) + "を決定する")
    total_superior(_players,_deside_num)

# 多数決
# 中央値から右を確認し、一番長い選手に順位を覚醒させる
# 引数
# １、対象の選手リスト
# ２、決定順位
def majority(_players, _deside_num):

    log.debug("start majority")
    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    # 無限ループ防止用
    if len(_players) <= 0:
        log.debug("end majority")
        return

    # インデックスとして使用する場合は、+1 しない
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

    # 不要では？
    log.debug(str(majority_list))
    
    # 多数決による最大値が1件である場合、
    # 順位が確定する
    # 過半数の対象者を抽出するため、初期化する
    check_list = []
    check_list = [player for player in _players if player.majorityNum == max(majority_list) ]

    if len(check_list) == 1:
        # 最大値が一つであれば、その値を持つ選手に順位を決定する
        print("多数決により"+ str(_deside_num) +"を決定しました")
        check_list[0].score = _deside_num

    # 複数ある場合は、上位加算を行う
    elif len(check_list) > 1:
        # 上位加算へ
        total_superior(check_list, _deside_num)

    # 対象差集合をset()を用いて取得する
    _players =  list( set(_players) ^ set(check_list))

    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)
    # print("次の順位"+ str(_deside_num) + "を決定する")
    majority(_players,_deside_num)



# スケーティング表読み込みマネージャ

# -> ファイル読み込み

# -> 直接入力

# 過半数(中央値)
# 再帰的に呼び出し処理を行う。
def median(_players, _deside_num):

    log.debug("start median")
    for player in _players:
        log.debug(str(player.number) + ":" + str(sorted(player.order)) )

    # 無限ループ防止用
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
            # 対象者がいないため、抽出条件の順位を一つ下げる
            fetch_num += 1
        elif len(check_list) > 0:
            break


    if len(check_list) == 1:
        # 順位の付与
        # チェック対象者からの削除
        check_list[0].score = _deside_num
        print("過半数により"+ str(_deside_num) +"を決定しました")
        # print(check_list[0].name)
        # print(check_list[0].score)

    elif len(check_list) > 1:
        # 対象者に対して多数決の検証をする
        majority(check_list, _deside_num)

    # 対象差集合をset()を用いて取得する
    _players =  list( set(_players) ^ set(check_list))

    # 次の順位を決定するため、再帰的に呼び出す
    _deside_num += len(check_list)
    # print("次の順位"+ str(_deside_num) + "を決定する")
    median(_players,_deside_num)

# スケーティング処理開始
def skating(_player_list):
    median(_player_list, 1)

def main():

    # 仮の選手情報
    testPlayer1 = Player(10,"Tanaka")
    testPlayer2 = Player(20,"Sato")
    testPlayer3 = Player(30,"Syzuki")
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
    judge_num = 151
    # 入力の変わりにランダム値を入れる
    order = list(range(1,len(player_list) + 1))
    rand_order = []
    for i in range(judge_num):
        rand_order = random.sample(order, 6)
        for j in range(6):
            player_list[j].setOrder(rand_order[j])

    # 審査結果を表示する
    print("審査内容")
    for player in player_list:
        print(str(player.number) + ":" + str(sorted(player.order)))

    # スケーティング開始
    skating(player_list)
    
    # 結果出力
    print("スケーティング結果")
    for player in player_list:
        print("number :" +  str(player.number) + " score:" +  str(player.score))

if __name__ == '__main__':
    main()