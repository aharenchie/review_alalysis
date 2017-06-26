#!/usr/bin/env pythono3
# -*- coding: utf-8 -*- 

from pyknp import KNP

"""
構文解析結果を保存

in：評価極性語,評価極性語のある文章
out:構文解析結果の辞書

"""
def save_bnst(pn_word,text):        

    bnst_dic ={}    
    pn_id = 0
 
    child_list=[]
    parent_list=[]

    # 1. 構文結果を保存 (1.親id辞書,2.単語id辞書)
    knp = KNP()
    result = knp.parse(text)
    
    for bnst in result.bnst_list():
        word = ""
        dic_value ={}

        # 1-1.単語の結合、評価極性語のidの調査    
        for mrph in bnst.mrph_list():            
            if mrph.midasi == pn_word: 
                pn_id = bnst.bnst_id
                
            word += mrph.midasi 

        # 1-2.辞書追加
        dic_value["parent_id"] = bnst.parent_id
        dic_value["word"]= word

        bnst_dic[bnst.bnst_id] = dic_value

    return bnst_dic,pn_id


"""
係り受け関係のid順を取得する

in：構文解析結果の辞書 
out:係り受け関係のid順

"""                            
def get_bnst_order(bnst_dic):

    bnst_order_dic = {}

    # 1. 全ての文節の係り受け順(id)を取得する
    for my_id in bnst_dic.keys():

        flag = True
        my_list=[my_id]
        serch_id = my_id

        # 1-1. 文節ごとに、最後の係り先になるまでループする
        while flag:
            parent_id = bnst_dic[serch_id]["parent_id"]

            if parent_id != -1: # 係り先が最後じゃないとき、係り先のidを格納
                my_list.append(bnst_dic[serch_id]["parent_id"])
                
            else: # 係り先が最後のとき、ループを抜ける
                flag = False
                
            serch_id = parent_id # 1-2.係り先のidを次の探索idとする
            
        bnst_order_dic[my_id]  = my_list # 1-3.文節ごとに、係り受け順を格納
    
    return bnst_order_dic

"""
最後の係り元idを取得する

in：構文解析結果の辞書
out:最後の係り元idを取得     

"""
def get_bnst_end(bnst_dic):
    
    end_list = []

    # 1. 文節ごとに、他の文節の親になっているか調べる
    for my_id in bnst_dic.keys():

        # 1-1. 他の文節の親を調査
        for value in bnst_dic.values():
            
            if my_id == value["parent_id"]: # 文節の親になっている場合、false
                flag = False
                break
            else: # 文節の親になっていない場合、true
                flag = True

        if flag:
            end_list.append(my_id) # リストに追加する
            
    return end_list

"""
ターゲット単語の左側を取得する

in：構文解析結果の辞書、係り受け関係のid順、ターゲットid
out:ターゲット単語の左側の単語

"""    
def get_bnst_left(bnst_dic,bnst_order_dic,pn_id):
    
    bnst_left = []
    end_list = get_bnst_end(bnst_dic)

    # 1. 係り受けルートにターゲット単語あったとき、左側の単語を取得
    for i in end_list:
        serch_list = bnst_order_dic[i]

        # 1-2. 係り受けルートにターゲット単語があるか調べる
        if pn_id in serch_list:
            p = serch_list.index(pn_id)            
            if p != 0:
                tmp_list = []

                # 1-3. ターゲット単語の左側の単語を取得
                for j in range(p):
                    left_id = serch_list[j]
                    tmp_list.append(bnst_dic[left_id]["word"])

                #1-4. 取得したものをリストに格納
                bnst_left.append(tmp_list)
        
    return bnst_left

"""
ターゲット単語の右側を取得する

in：構文解析結果の辞書、係り受け関係のid順、ターゲットid
out:ターゲット単語の右側の単語    

"""
def get_bnst_right(bnst_dic,bnst_order_dic,pn_id):

    bnst_right = []

    # 1. 係り関係順を元に、ターゲットの右側単語を取得
    for right_id in bnst_order_dic[pn_id]:
        if right_id != pn_id:
            bnst_right.append(bnst_dic[right_id]["word"])

    return bnst_right
