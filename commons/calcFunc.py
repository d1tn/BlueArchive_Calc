import csv
import pandas as pd
import numpy as np
from commons.readcsv import *
import uuid # ハッシュ値生成用

#データの入力列数
col = 18

#関数
columns=["生徒ID", "ToDo", "アイテムID", "数量"]

#キャラレベル強化
#必要キャラ経験値、クレジットの取得
def getStuExpCredit(stuNo,fromLv,toLv):
    res = []
    if fromLv < toLv:
        obj = "生徒Lv " + str(fromLv) +"→" + str(toLv)
        res.append([stuNo, obj , 2, sum(charLv[(charLv["CurrentLv"] >= fromLv) & (charLv["NextLv"] <= toLv)]["Exp"].astype('int',errors='ignore'))])
        res.append([stuNo, obj , 3, sum(charLv[(charLv["CurrentLv"] >= fromLv) & (charLv["NextLv"] <= toLv)]["Credit"].astype('int',errors='ignore'))])
    return res

#装備必要経験値、クレジット、設計図計算
def getEqExpCredit(stuNo,eqNo,fromLv,toLv):
    res = []
    if fromLv < toLv:
        eqNo = "Stu_EQ" + str(eqNo)
        fromText = eqLv[eqLv["CurrentLv"] == fromLv]["CurrentLv_text"].item()
        toText = eqLv[eqLv["NextLv"] == toLv]["NextLv_text"].item()
        obj = eqs[eqs["Id"]== (stuData[stuData["Stu_Id"]==stuNo][eqNo].item()) ]["Name"].item() +" "+ str(fromText) +"→" + str(toText)

        itemId_T2 = itemData[(itemData["EQTier"]== 2)&(itemData["EQId"]== (stuData[stuData["Stu_Id"]==stuNo][eqNo].item()))]["ItemId"].item()
        itemId_T3 = itemData[(itemData["EQTier"]== 3)&(itemData["EQId"]== (stuData[stuData["Stu_Id"]==stuNo][eqNo].item()))]["ItemId"].item()
        itemId_T4 = itemData[(itemData["EQTier"]== 4)&(itemData["EQId"]== (stuData[stuData["Stu_Id"]==stuNo][eqNo].item()))]["ItemId"].item()
        itemId_T5 = itemData[(itemData["EQTier"]== 5)&(itemData["EQId"]== (stuData[stuData["Stu_Id"]==stuNo][eqNo].item()))]["ItemId"].item()
        res.append([stuNo, obj, 1, sum(eqLv[(eqLv["CurrentLv"] >= fromLv) & (eqLv["NextLv"] <= toLv)]["Exp"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, 3, sum(eqLv[(eqLv["CurrentLv"] >= fromLv) & (eqLv["NextLv"] <= toLv)]["Credit"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, itemId_T2, sum(eqLv[(eqLv["CurrentLv"] >= fromLv) & (eqLv["NextLv"] <= toLv)]["Bp_T2"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, itemId_T3, sum(eqLv[(eqLv["CurrentLv"] >= fromLv) & (eqLv["NextLv"] <= toLv)]["Bp_T3"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, itemId_T4, sum(eqLv[(eqLv["CurrentLv"] >= fromLv) & (eqLv["NextLv"] <= toLv)]["Bp_T4"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, itemId_T5, sum(eqLv[(eqLv["CurrentLv"] >= fromLv) & (eqLv["NextLv"] <= toLv)]["Bp_T5"].astype('int',errors='ignore'))])
    return res

#EXレベル
def getExItems(stuNo,fromLv,toLv):
    res = []
    if fromLv < toLv :
        #初期設定
        fromText = str(fromLv)
        toText = str(toLv)
        obj = "EXスキルLv "+ fromText +"→" + toText
        #BD名特定
        cateID = 7
        Bd1 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 1)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        Bd2 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 2)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        Bd3 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 3)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        Bd4 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 4)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        #append
        res.append([stuNo, obj, 3, sum(exLv[(exLv["CurrentLv"] >= fromLv) & (exLv["NextLv"] <= toLv)]["Credit"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Bd1, sum(exLv[(exLv["CurrentLv"] >= fromLv) & (exLv["NextLv"] <= toLv)]["Bd_1"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Bd2, sum(exLv[(exLv["CurrentLv"] >= fromLv) & (exLv["NextLv"] <= toLv)]["Bd_2"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Bd3, sum(exLv[(exLv["CurrentLv"] >= fromLv) & (exLv["NextLv"] <= toLv)]["Bd_3"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Bd4, sum(exLv[(exLv["CurrentLv"] >= fromLv) & (exLv["NextLv"] <= toLv)]["Bd_4"].astype('int',errors='ignore'))])

        #OP数計算
        cateID = 6
        for i in range(1,3):
            #OP種別特定
            searchCol = "Stu_OP" +str(i)
            OPId = stuData[stuData["Stu_Id"]==stuNo][searchCol].item()
            str1= "_OP"+str(i)
            for i in range(fromLv+1,toLv+1):
                #レベル範囲
                str2 = "EX"+"to"+str(i)+str1
                for i in range(1,5):
                    #OPレア度総当たり
                    str3 = str2 + "g" + str(i)
                    try:
                        #カラム検索して該当する場合にOP名、レア度、数量を出力
                        quants = stuOP[stuOP["Stu_Id"] == stuNo][str3].item()
                        itemId = itemData[(itemData["CategoryId"]==  cateID)&\
                                        (itemData["Rarity"]== i)&\
                                        (itemData["OPId"]== OPId)]["ItemId"].item()
                        res.append([stuNo, obj, itemId, quants])

                    except:
                        continue
    return res

#サブスキルレベル
def getSsItems(stuNo,SSName,fromLv,toLv):
    res = []
    if fromLv < toLv:
        #初期設定
        fromText = str(fromLv)
        toText = str(toLv)
        obj = SSName + fromText +"→" + toText
        #技術ノート名特定
        cateID = 8
        Nt1 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 1)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        Nt2 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 2)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        Nt3 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 3)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        Nt4 = itemData[(itemData["CategoryId"]==  cateID)&\
                              (itemData["Rarity"]== 4)&\
                              (itemData["SchoolId"]== stuData[stuData["Stu_Id"]==stuNo]["Stu_School"].item())]["ItemId"].item()
        #秘伝ノート
        NtSc = itemData[(itemData["CategoryId"]==  cateID)&(itemData["Rarity"]== "")&(itemData["SchoolId"]== "")]["ItemId"].item()
        #append
        res.append([stuNo, obj, 3, sum(sklLv[(sklLv["CurrentLv"] >= fromLv) & (sklLv["NextLv"] <= toLv)]["Credit"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Nt1, sum(sklLv[(sklLv["CurrentLv"] >= fromLv) & (sklLv["NextLv"] <= toLv)]["Note_1"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Nt2, sum(sklLv[(sklLv["CurrentLv"] >= fromLv) & (sklLv["NextLv"] <= toLv)]["Note_2"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Nt3, sum(sklLv[(sklLv["CurrentLv"] >= fromLv) & (sklLv["NextLv"] <= toLv)]["Note_3"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, Nt4, sum(sklLv[(sklLv["CurrentLv"] >= fromLv) & (sklLv["NextLv"] <= toLv)]["Note_4"].astype('int',errors='ignore'))])
        res.append([stuNo, obj, NtSc, sum(sklLv[(sklLv["CurrentLv"] >= fromLv) & (sklLv["NextLv"] <= toLv)]["Note_secret"].astype('int',errors='ignore'))])
        #OP数計算
        cateID = 6
        for i in range(1,3):
            #OP種別特定
            searchCol = "Stu_OP" +str(i)
            OPId = stuData[stuData["Stu_Id"]==stuNo][searchCol].item()
            str1= "_OP"+str(i)
            for i in range(fromLv+1,toLv+1):
                #レベル範囲
                str2 = "SS"+"to"+str(i)+str1
                for i in range(1,5):
                    #OPレア度総当たり
                    str3 = str2 + "g" + str(i)
                    try:
                        #カラム検索して該当する場合にOP名、レア度、数量を出力
                        quants = stuOP[stuOP["Stu_Id"] == stuNo][str3].item()
                        itemId = itemData[(itemData["CategoryId"]==  cateID)&\
                                        (itemData["Rarity"]== i)&\
                                        (itemData["OPId"]== OPId)]["ItemId"].item()
                        res.append([stuNo, obj, itemId, quants])


                    except:
                        continue
    return res

#関数の実行
def runCalc(stuNo, stuLv_from, eq1Lv_from, eq2Lv_from, eq3Lv_from, exLv_from, nsLv_from, psLv_from, ssLv_from, stuLv_to, eq1Lv_to, eq2Lv_to, eq3Lv_to, exLv_to, nsLv_to, psLv_to, ssLv_to, DoOrNot):
    if DoOrNot == 1 :
        result = []
        result.extend(getStuExpCredit(stuNo,stuLv_from,stuLv_to))
        result.extend(getEqExpCredit(stuNo,1,eq1Lv_from ,eq1Lv_to))
        result.extend(getEqExpCredit(stuNo,2,eq2Lv_from ,eq2Lv_to))
        result.extend(getEqExpCredit(stuNo,3,eq3Lv_from ,eq3Lv_to))
        result.extend(getExItems(stuNo,exLv_from,exLv_to))
        result.extend(getSsItems(stuNo,"ノーマルスキル",nsLv_from,nsLv_to))
        result.extend(getSsItems(stuNo,"パッシブスキル",psLv_from,psLv_to))
        result.extend(getSsItems(stuNo,"サブスキル",ssLv_from,ssLv_to))
        # print('StuId',stuNo,": calculation ok")
        return result
    else:
        # print('StuId',stuNo,": calculation skipped")
        return []

# 数字or空白のみの多次元配列を数値型=>文字列型に変換
def IntToStr(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            # 最初と最後の行（生徒IDと計算対象チェック）以外の値が0の場合、空白文字として格納
            if j != 0 and j!= 17:
                if array[i][j] == 0:
                    array[i][j] = ''
            array[i][j] = str(array[i][j])

# 数字or空白のみの多次元配列を数値型=>文字列型に変換
# DB保存用のため空白には直さない
def IntToStrKeepZero(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            array[i][j] = str(array[i][j])


# 数字のみの多次元配列を文字列型=>数値型に変換
def StrToInt(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == '':
                array[i][j] = 0
            array[i][j] = int(array[i][j])

#18 x n の入力クエリを n行18列に変換する
#クエリから文字列として受け取った数値を指定幅に切り分けて多次元配列化する
def InputToArray(input):
    array =[]
    err = []
    length = 18
    for i in range(len(input)//length):
        lst = []
        for j in range(length):
            if input[i*length+j] == '':
                err.append('未入力の箇所があります。')
                continue
            try:
                lst.append(int(input[i*length+j]))
            except:
                err.append('不正な値が送信されました。')
                continue
        if err == []:
            array.append(lst)
    return array,err

# 最大値・最小値チェック
def ValidateInMinToMax(stuNo, stuLv_from, eq1Lv_from, eq2Lv_from, eq3Lv_from, exLv_from, nsLv_from, psLv_from, ssLv_from, stuLv_to, eq1Lv_to, eq2Lv_to, eq3Lv_to, exLv_to, nsLv_to, psLv_to, ssLv_to, DoOrNot):
    if DoOrNot == 1 :
        if stuLv_from in range(1, charLv_max +1) and exLv_from in range(exLv_min, exLv_max +1) and eq1Lv_from in range(eqLv_min, eqLv_max +1) and eq2Lv_from in range(eqLv_min, eqLv_max +1) and eq3Lv_from in range(eqLv_min, eqLv_max +1) and nsLv_from in range(sklLv_min, sklLv_max +1) and psLv_from in range(sklLv_min, sklLv_max +1) and ssLv_from in range(sklLv_min, sklLv_max +1) and stuLv_to in range(1, charLv_max +1) and exLv_to in range(exLv_min, exLv_max +1) and eq1Lv_to in range(eqLv_min, eqLv_max +1) and eq2Lv_to in range(eqLv_min, eqLv_max +1) and eq3Lv_to in range(eqLv_min, eqLv_max +1) and nsLv_to in range(sklLv_min, sklLv_max +1) and psLv_to in range(sklLv_min, sklLv_max +1) and ssLv_to in range(sklLv_min, sklLv_max +1):
            # print('StuId',stuNo,": min_to_max validation ok")
            return []
        else:
            # print('StuId',stuNo,": min_to_max validation ERROR!!")
            return ['範囲外の数値が入力されています。']

    else:
        pass
        # print('StuId',stuNo,": min_to_max validation skipped")

##########################################################
# 以下、sqliteのデータ処理専用
##########################################################
# 多次元配列 => 文字列への変換([[1,2,3],[4,5,6]] => '1,2,3,4,5,6')
def ArrayToStr(array):
    str1 = ''
    for i in array:
        for j in i:
            str1 +=str(j)+','
    return str1[:-1]

# 文字列 => 多次元配列への変換('1,2,3,4,5,6' => [[1,2,3],[4,5,6]])
def StrToArray(string):
    arr1 = [int(i) for i in string.split(',')]
    print('●',len(arr1),col)
    arr2 = []
    for i in range(int(len(arr1)/col)):
        arr2.append([ arr1[i*col + j] for j in range(col)])
    return arr2

#データと紐づけるためのキー文字列の生成（アルファベット大文字・小文字のみ）
import random, string
def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

##########################################################
# ハッシュ値生成
##########################################################
# ハッシュ値生成
def set_submit_token(request):
    #ハッシュ値生成
    submit_token = str(uuid.uuid4())
    #セッションにトークンを格納
    request.session['submit_token'] = submit_token
    #クライアント用に同じ値のトークンを返す
    return submit_token

# ハッシュ値チェック
def exist_submit_token(request):
    #クライアントから送信されたトークンを取得
    token_in_request = request.POST.get('submit_token')
    #一度使用したトークンだった場合セッションから破棄
    token_in_session = request.session.pop('submit_token', '')

    if not token_in_request:
        return False
    if not token_in_session:
        return False
    return token_in_request == token_in_session
