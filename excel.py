import pandas as pd
from os import listdir

# csvファイルを配列に入れる
csvs = []
for i in listdir('./csv/'):
    raw_csv = pd.read_csv('./csv/' + i)

    # startからendまで加工する
    valid_index = raw_csv.index[raw_csv['StartFinish'] == 1].tolist()
    valid_csv = raw_csv[valid_index[0]:valid_index[1]+1]

    # インデックスを整理
    csv = valid_csv.drop(['StartFinish'], axis=1)
    csv = csv.reset_index(drop=True)
    
    csvs.append(csv)

# csvファイルを結合する
csv_result = csvs[0]
for i, csv in enumerate(csvs):
    if i != 0:
        csv_result = pd.concat([csv_result, csv], axis=1)

csv_result.to_csv('./csv/result.csv')
