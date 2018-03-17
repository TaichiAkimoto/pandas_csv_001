import pandas as pd
from os import listdir
import re

# csvファイルを配列に入れる
csvs = []
names = []
means = []
ave_errs = []
for i in listdir('./csv/'):
    # csvの読み込み
    raw_csv = pd.read_csv('./csv/' + i)

    # .csvを除いたファイル名を取得
    file_name = re.search(r'([^.]+)\.csv', i).group(1)
    names.append(file_name)

    # startから10行取得
    valid_index = raw_csv.index[raw_csv['StartFinish'] is 'start']
    valid_csv = raw_csv[valid_index:10]

    # Stressのみを抽出
    csv = valid_csv[['Stress']]

    # 平均値を求めて配列に入れる
    mean = csv["Stress"].mean()
    means.append(mean)

    # Column名を変更
    csv.columns = [file_name]

    # インデックスを整理
    csv = csv.reset_index(drop=True)

    # 平均値を引いた値のDataFrameを作成
    ave_errs.append(csv - mean)

    csvs.append(csv)

# 平均値のDataFrameを作成 & 列の名前を変更
averages = pd.DataFrame([means], columns=names)

# csvファイルを結合する
csv_result = csvs[0]
for i, csv in enumerate(csvs):
    if i != 0:
        csv_result = pd.concat([csv_result, csv], axis=1)

# 平均値の配列を下に追加してCSV出力
csv_result = pd.concat([csv_result, averages], axis=0)

# 平均値を引いた値のDataFrameに関しても同様の処理を行う
ave_err_result = ave_errs[0]
for i, ave_csv in enumerate(ave_errs):
    if i != 0:
        ave_err_result = pd.concat([ave_err_result, ave_csv], axis=1)

csv_result.to_csv('./csv/stress.csv')
ave_err_result.to_csv('./csv/ave_err.csv')

# TODO 手動で最後の行の名前を'平均に直す'
