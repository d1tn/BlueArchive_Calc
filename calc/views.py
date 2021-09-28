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


# ０．セッション削除
def delSession(request):
    temp_name = "charchoise.html"
    del request.session['yourCharData']
    del request.session['inputs']
    # print('your sessions were deleted.')
    return render(request,temp_name)


#１．キャラ選択画面
def charchoise(request):
    temp_name = "charchoise.html"

    # セッション削除
    # del request.session['yourCharData']
    # del request.session['inputs']
    # # print('your sessions were deleted.')

    temp_name = "charchoise.html"
    guide_msg = '強化する生徒を選んでください。\n選び終わったら、「次へ」を押してください。'

    # 配列の生成
    inputs = []
    # 初期化方法
    for i in charId:
        #入力配列の初期設定（最後の1は計算するかどうか　0は計算しない）
        inputs.append([int(i),1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0])


    # 生成した初期値をセッション変数に格納
    request.session['inputs'] = inputs

    context = {
    'chars' : zip(charId,charName),
    'guide_msg':guide_msg,
    }
    return render(request,temp_name,context)

# ２．育成状況・育成目標入力画面
def input(request):
    # print('\n\n▼ Input Page ▼')
    temp_name = "input.html"
    guide_msg = '生徒の育成度合いについて、現時点の数値と育成目標を入力してください。\n入力が終わったら「計算する」を押してください。'


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
    charIds = request.GET.getlist('char', None)
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
    'ths':ths,
    'charDatas' : zip(charInputs,charNames),
    #プルダウン用リスト、最大値最小値等をreadcsv.pyから取得
    'eqLv_List':eqLv_List,
    'max_min':[[charLv_max,charLv_min], [exLv_max, exLv_min], [sklLv_max, sklLv_min]],
    'guide_msg':guide_msg
    }
    return render(request,temp_name,context)


# ２．５　計算完了後の再入力

# ３．計算
def calc(request):
    # print('\n\n▼ Result Page ▼')
    guide_msg =''
    result = []
    input = request.GET.getlist('input', None)
    # セッション変数からの受取
    # inputs = request.session['inputs']
    inputs = []
    msg = []
    context = {
    'guide_msg':guide_msg
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
#　　　　　　テキスト表示ページ
########################################
# ４．使い方・概要ページ
def howto(request):
    temp_name = "contents.html"
    page = 'howto'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    texts = [str(item[5]) for item in row.itertuples()]

    context = {
    'pagetitle':title,
    'txts':zip(headings, texts),
    'guide_msg':'',
    }
    return render(request,temp_name,context)

# ５．その他説明ページ
def about(request):
    temp_name = "contents.html"
    page = 'about'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    texts = [str(item[5]) for item in row.itertuples()]

    context = {
    'pagetitle':title,
    'txts':zip(headings, texts),
    'guide_msg':'',
    }
    return render(request,temp_name,context)

# ６．プライバシーポリシー
def privacypolicy(request):
    temp_name = "contents.html"
    page = 'privacypolicy'
    row = PagesTexts[PagesTexts['page'] == page]
    title = [item for item in row['title']][0]
    headings = [str(item[4]) for item in row.itertuples()]
    texts = [str(item[5]) for item in row.itertuples()]

    context = {
    'pagetitle':title,
    'txts':zip(headings, texts),
    'guide_msg':'',
    }
    return render(request,temp_name,context)

#
# # ４．使い方・概要ページ
# def howto(request):
#     temp_name = "contents.html"
#     pagetitle = '本ツールの使い方'
#     headings = ['使い方','計算される数値について']
#     texts = [
#     '育てたい生徒を選択し、生徒のレベルや装備、各種スキルについて、現在の値と、育成目標となる値を入力すると、素材の必要数が一括で計算・表示されます。\n\n本アプリで入力した数値は、お使いのブラウザのセッションIDに紐づけて保存されます。\n\n育成が進んだときなど、再度計算をやり直したい時に、以前の値を引き継いで使用することが可能です。',
#     '本ツールで使用する生徒パラメータについては、可能な限りゲーム内で実際に確認して正確な数値を把握するように務めておりますが、強化に必要となるオーパーツの数が生徒ごとに異なっており、一部の生徒について必要数が把握し切れておりません。\n\n必要数が未判明の生徒は、既に判明している生徒たちの必要数の平均値で計算する仕様とさせて頂いております。\n\nこのため、一部の生徒でオーパーツ数に誤差が生じる場合がございますが、あらかじめご了承ください。']
#
#
#     context = {
#     'pagetitle':pagetitle,
#     'txts':zip(headings, texts),
#     'guide_msg':'',
#     }
#     return render(request,temp_name,context)
#
# # ５．その他説明ページ
# def about(request):
#     temp_name = "contents.html"
#     pagetitle = '本ツールについて'
#     headings = [
#     '概要',
#     'リンクについて',
#     '免責事項',
#     '著作権について',
#     'お問い合わせ']
#     texts = [
#     'Yostar社提供のスマホゲーム「ブルーアーカイブ（ブルアカ）」の、非公式キャラクター育成支援ツールです。\nブルアカは育成素材の種別が多く管理も大変なため、なんとか快適にできないか？と思い開発に至りました。\n皆様の日々のプレイの助けになれば幸いです。',
#     '当サイトはリンクフリー（掲載許可や連絡は不要）です。\nSNSや動画投稿サイト等にて是非ご友人方へご紹介下さい。\n\nなお、画像等コンテンツへの直リンク行為はご遠慮願います。',
#     '当サイトで表示する一切の情報について、可能な限り正確な情報の掲載に努めておりますが、正確性を保証するものではございません。\n\nまた、当サイトの利用に伴いユーザーに生じた損害については、一切の責任を負いかねます。あらかじめご了承ください。',
#     '当サイトは権利者様の権利侵害を目的としたものではございません。\nまた、当サイトでは、著作権法第32条（研究その他の引用の目的）に基づき画像の引用を行っております。\n\n著作権に関して問題がございましたら、権利者様からお問い合わせ下さい。速やかに対致します。',
#     '当サイトに関するお問い合わせは<a href="https://forms.gle/HeBsiPisRznURhnj8">お問い合わせフォーム</a>、または<a href="https://twitter.com/messages/compose?recipient_id=1438494596707729416">TwitterのDM</a>にて受け付けております。']
#
#     context = {
#     'pagetitle':pagetitle,
#     'txts':zip(headings, texts),
#     'guide_msg':'',
#     }
#     return render(request,temp_name,context)
#
# # ６．プライバシーポリシー
# def privacypolicy(request):
#     temp_name = "contents.html"
#     pagetitle = 'プライバシーポリシー'
#     headings = [
#     '個人情報のお取り扱いについて',
#     '広告について',
#     'アクセス解析ツールについて',
#     'お問い合わせ']
#     texts = [
#     '',
#     '',
#     '',
#     '当サイトに関するお問い合わせは<a href="https://forms.gle/HeBsiPisRznURhnj8">お問い合わせフォーム</a>、または<a href="https://twitter.com/messages/compose?recipient_id=1438494596707729416">TwitterのDM</a>にて受け付けております。']
#
#     context = {
#     'pagetitle':pagetitle,
#     'txts':zip(headings, texts),
#     'guide_msg':'',
#     }
#     return render(request,temp_name,context)
