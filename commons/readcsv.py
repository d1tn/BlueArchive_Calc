import csv
import pandas as pd
import numpy as np

#csvフォルダ
csvFolder = "static/csv/"
#生徒データ
stuData = pd.DataFrame(pd.read_csv(csvFolder + "Main/00_Students_Data.csv", encoding="utf-8"))

#生徒の必要オーパーツ数データ
    #欠損値処理　NaNは平均値+1
    #小数型→整数型に 数値型以外はエラーとなるため無視する
stuOP = pd.DataFrame(pd.read_csv(csvFolder + "Main/11_Students_OP.csv", encoding="utf-8"))
stuOP = stuOP.fillna(stuOP.mean(numeric_only=True)+1).astype('int',errors='ignore')

#その他データ
schl = pd.DataFrame(pd.read_csv(csvFolder + "Main/01_School.csv", encoding="utf-8"))
clb = pd.DataFrame(pd.read_csv(csvFolder + "Main/02_Club.csv", encoding="utf-8"))
typ = pd.DataFrame(pd.read_csv(csvFolder + "Main/03_Type.csv", encoding="utf-8"))
cls = pd.DataFrame(pd.read_csv(csvFolder + "Main/04_Class.csv", encoding="utf-8"))
wpn = pd.DataFrame(pd.read_csv(csvFolder + "Main/05_Weapon.csv", encoding="utf-8"))
pstn = pd.DataFrame(pd.read_csv(csvFolder + "Main/06_Position.csv", encoding="utf-8"))
area = pd.DataFrame(pd.read_csv(csvFolder + "Main/07_Area.csv", encoding="utf-8"))
eqs = pd.DataFrame(pd.read_csv(csvFolder + "Main/08_Eqs.csv", encoding="utf-8"))
ops = pd.DataFrame(pd.read_csv(csvFolder + "Main/09_Ops.csv", encoding="utf-8"))
illust = pd.DataFrame(pd.read_csv(csvFolder + "Main/10_Illustrators.csv", encoding="utf-8"))
itemCategoty = pd.DataFrame(pd.read_csv(csvFolder + "Main/12_ItemCategory.csv", encoding="utf-8"))
itemData = pd.DataFrame(pd.read_csv(csvFolder + "Main/13_Item_Data.csv", encoding="utf-8")).fillna("")

#必要経験値等
ratio = pd.DataFrame(pd.read_csv(csvFolder + "Exp/00_Ratio.csv", encoding="utf-8"))
charLv = pd.DataFrame(pd.read_csv(csvFolder + "Exp/01_CharLv.csv", encoding="utf-8"))
eqLv = pd.DataFrame(pd.read_csv(csvFolder + "Exp/02_EqLv.csv", encoding="utf-8")).astype('int',errors='ignore')
exLv = pd.DataFrame(pd.read_csv(csvFolder + "Exp/03_ExLv.csv", encoding="utf-8"))
sklLv = pd.DataFrame(pd.read_csv(csvFolder + "Exp/04_SkillLv.csv", encoding="utf-8"))
# sklLv_Unique = pd.DataFrame(pd.read_csv(csvFolder + "Exp/05_SkillLv_Unique.csv", encoding="utf-8"))

###入力フォーム用数値作成
#キャラIDリスト、キャラ名リスト(五十音順の表示用)
studentsList = []
stuIds_and_Names = stuData.loc[:,['Stu_Id','Stu_Name','Sort_Id']]
#五十音順にソート
stuIds_and_Names = stuIds_and_Names.sort_values('Sort_Id', ascending=True)
stuIds_and_Names = stuIds_and_Names.loc[:,['Stu_Id','Stu_Name']]
studentsList = stuIds_and_Names.values.tolist()

# プルダウン用リスト
eqLv_Lista = eqLv["CurrentLv"][:].dropna().apply(lambda x: str(int(x)))
eqLv_Listb = eqLv["CurrentLv_text"][:].dropna()
eqLv_List =[]
for i ,j in zip(eqLv_Lista, eqLv_Listb):
    eqLv_List.append([i, j])

# キャラIDリスト（必ずしも連続性があるとは限らないためリスト型として格納）
# 範囲外のIdを削除するために使用
stuIds = []
for i in stuData['Stu_Id'][:].dropna().astype('int'):
    stuIds.append(int(i))

# 最大値・最小値
# キャラLv
# 最小値
charLv_min = charLv["CurrentLv"].min().astype('int')
# charLv_max = charLv["CurrentLv"].max()
# 最大値
charLv_max = 78

# 装備Lv
eqLv_min = eqLv["CurrentLv"].min().astype('int')
eqLv_max = eqLv["CurrentLv"].max().astype('int')

# ExスキルLv
# 最小値
exLv_min = exLv["CurrentLv"].min().astype('int')
# 最大値
exLv_max = exLv["CurrentLv"].max().astype('int')

# その他スキルLv
# 最小値
sklLv_min = sklLv["CurrentLv"].min().astype('int')
# 最大値
sklLv_max = sklLv["CurrentLv"].max().astype('int')


########################################
#　　　テキストデータ読み込み
#######################################
PagesTexts = pd.DataFrame(pd.read_csv(csvFolder + "Texts/00_Contents.csv", encoding="utf-8"))

def getTextsFromCsv(pagename):
    row = PagesTexts[PagesTexts['page'] == pagename]
    title = [item for item in row['title']][0]
    classes = [str(item[4]) for item in row.itertuples()]
    headings = [str(item[5]) for item in row.itertuples()]
    texts = [str(item[6]) for item in row.itertuples()]
    return title, classes, headings, texts
