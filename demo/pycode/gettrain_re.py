# 各種module install
# 加えて，fugashi, unidic-lite が必要
import mysql.connector
from tqdm import tqdm
import faiss 
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA 

def getTrainData(input_text):
    
    pca_value = 100 # 50
    shot = 3

    model = SentenceTransformer("cl-nagoya/sup-simcse-ja-base")

    # 検索ベクトルの作成
    input_embedding = model.encode([input_text])

    # DB接続
    cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='lsesjsts',  # パスワード
        host='localhost',  # ホスト名(IPアドレス）
        database='mydb'  # データベース名
    )

    #カーソルを開く
    cursor = cnx.cursor()
    sql = '''select count(*) from train_data'''
    cursor.execute(sql)
    
    # 訓練データ数を取得
    num_article = cursor.fetchall()[0][0]
    
    cursor.close()

    cursor = cnx.cursor()
    fetch_sql = '''select * from train_data where art_id = %s '''
    
    sample_data = []

    # DB上のデータを読み出し
    for i in range(num_article):
        cursor.execute(fetch_sql, (i+1, ))
        art_content = cursor.fetchall()[0]
        paral = art_content[1] + "\t" + art_content[2]

        sample_data.append(paral)
    
    cursor.close()
    
    temp = model.encode(sample_data)

    # PCAで次元圧縮
    df = pd.DataFrame(temp, columns = ["dim_"+str(i) for i in range(768)])
    pca = PCA(n_components=pca_value)
    pca.fit(df)
    vec = pca.transform(df)

    # 検索ベクトルの圧縮
    df_in = pd.DataFrame(input_embedding, columns = ["dim_"+str(i) for i in range(768)])
    query = pca.transform(df_in)

    # 対象テキストの追加
    index = faiss.IndexFlatIP(pca_value)
    index.add(vec)

    # 近傍探索の実行。
    D, I = index.search(query, 3)

    # I: インデックスをもとに，対応するid のペアを抽出
    cursor = cnx.cursor()
    fetch_sql = '''select * from train_data where art_id = %s '''

    fetch_pair = []
    art_id = I.tolist()[0]
    for i in range(shot):
        cursor.execute(fetch_sql, (art_id[i]+1, ))
        fetch_pair.append(cursor.fetchall())
    
    cursor.close()

    sample_pair = []

    for i in range(shot):
        sample_pair.append(fetch_pair[i][0][1])
        sample_pair.append(fetch_pair[i][0][2])
    
    print(sample_pair)
    
    if cnx is not None and cnx.is_connected():
        cnx.close()

    return sample_pair

if __name__=='__main__':
    input_text = 'シークワーサー独特の苦みを残した大人向けの味といい、試行錯誤して煮詰めた自信作を買い物客らに売り込んだ。'
    print(getTrainData(input_text))
