from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import sqlite3
import csv
import pandas as pd
import numpy as np
from commons.readcsv import *
from commons.calcFunc import *
from .forms import *
import copy

########################################
#　　　　　　１．計算ページ
########################################
#１．キャラ選択画面
def charchoise(request):
    temp_name = "charchoise.html"
    page = 'top'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    classes = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]

    temp_name = "charchoise.html"

    # 配列の生成
    inputs = []
    # 初期化方法
    for i in charId:
        #入力配列の初期設定（最後の1は計算するかどうか　0は計算しない）
        inputs.append([int(i),1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0])


    # 生成した初期値をセッション変数に格納
    request.session['inputs'] = inputs

    context = {
    'pagetitle':title,
    'contentsClass':classes,
    'txts':zip(headings, texts),
    'chars' : zip(charId,charName),
    }
    return render(request,temp_name,context)

# ２．育成状況・育成目標入力画面
def input(request):
    # print('\n\n▼ Input Page ▼')
    temp_name = "input.html"
    page = 'input'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    classes = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]


    # 入力済みデータが存在する場合はそちらから読み込む
    try:
        request.session['yourCharData']
        # print('yourCharData:',request.session['yourCharData'])
        if request.session['yourCharData'] !=[]:
            # print('your data is exist!')
            inputs = request.session['yourCharData']
        else:
            # print('your data is not exist 1')
            inputs = request.session['inputs']
            request.session['yourCharData'] =inputs

    except:
        # セッション変数から初期値の受取
        # print('your data is not exist 2')
        inputs = request.session['inputs']
        request.session['yourCharData'] =inputs

    # 入力データを文字列=>数値型に変換
    StrToInt(inputs)

    #入力済みデータにいないキャラが追加されていた場合は初期値を追加
    for i in range(len(charId)):
        if charId[i] not in [input[0] for input in inputs]:
            # print('New stuID:',charId[i])
            inputs.append([int(charId[i]),1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0])


    #対象キャラIDをリクエストから受取
    charIds = request.POST.getlist('char', None)
    charNames = []
    # 入力データの文字列変換用
    charInputs = []
    for i in range(len(inputs)):
        for j in range(len(charIds)):
            # チェックした生徒IDと初期配列0列目（キャラID）の比較
            # 一致している場合（チェックされている場合）のみ処理
            if int(inputs[i][0]) == int(charIds[j]):
                # 計算対象であるフラグを立てる
                inputs[i][17] = 1
                charInputs.append(inputs[i])
            # 文字列変換用
            #クエリから来たキャラIDを元にキャラ名を検索
            charNames.append(stuData.loc[stuData["Stu_Id"] == int(charIds[j])]["Stu_Name"].item())
    # print('charInputs:',charInputs)
    # # セッション変数を更新
    # request.session['inputs'] = inputs
    #テンプレートに投げる為に一時的に文字列に変換
    IntToStr(charInputs)
    # print('charInputs:',charInputs)

    ths = ['キャラ','装備1','装備2','装備3','EXスキル','ノーマルスキル','パッシブスキル','サブスキル']
    context = {
    'pagetitle':title,
    'contentsClass':classes,
    'txts':zip(headings, texts),
    'ths':ths,
    'charDatas' : zip(charInputs,charNames),
    #プルダウン用リスト、最大値最小値等をreadcsv.pyから取得
    'eqLv_List':eqLv_List,
    'max_min':[[charLv_max,charLv_min], [exLv_max, exLv_min], [sklLv_max, sklLv_min]],
    }
    return render(request,temp_name,context)

# ３．計算
def result(request):
    title = '計算結果'
    # print('\n\n▼ Result Page ▼')
    result = []
    input = request.POST.getlist('input', None)
    # セッション変数からの受取
    # inputs = request.session['inputs']
    inputs = []
    msg = []
    context = {
    'pagetitle':title,
    }


    # クエリを多次元配列の形に変換
    inputs,msg = InputToArray(input)

    # 最大値・最小値チェック
    for i in range(len(inputs)):
        val = []
        val += ValidateInMinToMax(*inputs[i])
        if val != []:
            msg += val
            break

    # エラーが発生（エラーメッセージがある）した場合は処理をせずエラーメッセージを返す
    if msg != [] and msg != '':
        # print('An error has occured : ',msg)
        return render(request,'input.html',
        {'msg':msg,
        'input':input}
        )


    # 選んだキャラIDとキャラ名
    charIds = [id[0] for id in inputs]
    charNames = []
    # 入力データの文字列変換用
    for i in range(len(charIds)):
        charNames.append(stuData.loc[stuData["Stu_Id"] == int(charIds[i])]["Stu_Name"].item())
    context['chars'] = zip(charIds, charNames)

    # 入力値を元に計算
    res = []
    result = []
    for i in range(len(inputs)):
        res += runCalc(*inputs[i])

    if res == []:
        msg.append(['必要なアイテムはありません。'])
        context['msg'] = msg
    else:
        # DataFrameの取り込み
        res = pd.DataFrame(res,columns=columns)
        #数量が0以下の行を非表示
        res = res[res["数量"]>0]
        #アイテムID,数量の列のみ表示
        res = res.loc[:,["アイテムID","数量"]]
        #アイテムIDでグループ化してソート
        res = res.groupby("アイテムID").sum(numeric_only=True).reset_index()
        #アイテムID順にソート
        #StuId,ItemIdとアイテム名を紐づけ
        res = res.sort_values("アイテムID", ascending=True)
        res["アイテム名"] = list(map(lambda x : itemData.loc[itemData["ItemId"] == x]["Name"].item(),list(res["アイテムID"])))
        res["ソートID"] = list(map(lambda x : itemData.loc[itemData["ItemId"] == x]["SortId"].item(),list(res["アイテムID"])))

        #表示（完成形）
        res = res.loc[:,["アイテムID","アイテム名","数量","ソートID"]]
        res = res.sort_values('ソートID', ascending=True)
        result = res.values.tolist()
        context['result'] = result

    # キャラ育成状況・入力データのセッション変数への上書き保存
    # ID順にソート
    datas = request.session['yourCharData']

    # 数値型に変換
    StrToInt(datas)
    StrToInt(inputs)


    if datas != []:
        for i in range(len(inputs)):
            # print('\nstuId:',inputs[i][0])
            if inputs[i][0] in [d[0] for d in datas]:
                # print('This stuId is already exist.:',datas[[d[0] for d in datas].index(inputs[i][0])])
                datas[[d[0] for d in datas].index(inputs[i][0])] = inputs[i]
                # print('A data was rewrited. :', datas[[d[0] for d in datas].index(inputs[i][0])])
                continue
            else:
                # print('This stuId is new')
                # print(inputs[i])
                datas.append(inputs[i])
                # print('A new data was appended.:',[d[0] for d in datas])
                continue
    else:
        # print('Your data is not exist yet.')
        for input in inputs:
            datas.append(input)

    # 範囲外の生徒IDを削除
    tmp = []
    for i in range(len(datas)):
        if datas[i][0]  in stuIds:
            tmp.append(datas[i])
        else:
            pass
            # print('\nOut-of-range stuId was deleted :',datas[i][0])
    datas = tmp
    # 入力データだけでなく個人データの検証も必要なため、
    # 入力がすべて終了した個人データに対して検証を行う

    # 個人の入力データをセッションIDに保存
    if request.session['yourCharData'] !=[]:
        request.session['yourCharData'] = datas
        # print('\nYour data was saved!! :')
        for i in request.session['yourCharData']:
            pass
            # print(i)

    temp_name = "result.html"
    return render(request,temp_name,context)
########################################
#　　　　　　２．データの保存・読込
########################################
def saveConfirm(request):
    temp_name = "save.html"
    page = 'saveConfirm'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    classes = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]

    #セッションデータの読込
    if request.session['yourCharData'] ==[]:
        texts[0] = "入力データが存在しません。まずは生徒の育成から始めましょう！"

        context = {
        'pagetitle':title,
        'contentsClass':classes,
        'txts':zip(headings, texts),
        'inputData':'none',
        }
        return render(request,temp_name,context)

    else:
        headings += ['入力データ']
        inputs = request.session['yourCharData']
        inputData = ArrayToStr(inputs)

        # 入力データを文字列=>数値型に変換
        StrToInt(inputs)

        #入力済みデータにいないキャラが追加されていた場合は初期値を追加
        for i in range(len(charId)):
            if charId[i] not in [input[0] for input in inputs]:
                # print('New stuID:',charId[i])
                inputs.append([int(charId[i]),1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0])

        charNames = []
        # 入力データの文字列変換用
        charInputs = []
        for i in range(len(inputs)):
            charInputs.append(inputs[i])
            # 文字列変換用
            #クエリから来たキャラIDを元にキャラ名を検索
            charNames.append(stuData.loc[stuData["Stu_Id"] == int(inputs[i][0])]["Stu_Name"].item())
        # print('charInputs:',charInputs)
        # # セッション変数を更新
        # request.session['inputs'] = inputs
        #テンプレートに投げる為に一時的に文字列に変換
        IntToStr(charInputs)
        # print('charInputs:',charInputs)

        ths = ['キャラ','装備1','装備2','装備3','EXスキル','ノーマルスキル','パッシブスキル','サブスキル']
        context = {
        'pagetitle':title,
        'contentsClass':classes,
        'txts':zip(headings, texts),
        'ths':ths,
        'charDatas': zip(charInputs,charNames),
        'inputData':inputData,
        #プルダウン用リストをreadcsv.pyから取得
        'eqLv_List':eqLv_List,
        }
        return render(request,temp_name,context)

def saved(request):
    temp_name = "save.html"
    page = 'saved'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    classes = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]
    input = request.POST.getlist('input', None)

    headings += ['認証キー']
    # キー文字列(英数字6文字)の生成
    key = get_random_string(6)
    texts += ['<span class="ninsho">'+key+'<span>']

    context = {
    'pagetitle':title,
    'contentsClass':classes,
    'txts':zip(headings, texts),
    'inputData':'none',
    }
    return render(request,temp_name,context)


def loadData(request):
    pass

########################################
#　　　　　　３．テキスト表示ページ
########################################
# １．使い方・概要ページ
def howto(request):
    temp_name = "contents.html"
    page = 'howto'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    classes = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]

    context = {
    'pagetitle':title,
    'contentsClass':classes,
    'txts':zip(headings, texts),
    }
    return render(request,temp_name,context)

# ２．その他説明ページ
def about(request):
    temp_name = "contents.html"
    page = 'about'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    classes = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]

    context = {
    'pagetitle':title,
    'contentsClass':classes,
    'txts':zip(headings, texts),
    }
    return render(request,temp_name,context)

# ３．プライバシーポリシー
def privacypolicy(request):
    temp_name = "contents.html"
    page = 'privacypolicy'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    classes = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]

    context = {
    'pagetitle':title,
    'contentsClass':classes,
    'txts':zip(headings, texts),
    }

    return render(request,temp_name,context)
