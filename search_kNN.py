from tqdm import tqdm
import faiss 
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA 

# simCSEでベクトル作成 -> faissで検索
def use_simcse(input_text):
    pca_value = 100 # 50

    model = SentenceTransformer("cl-nagoya/sup-simcse-ja-base")

    # 検索ベクトルの作成
    input_embedding = model.encode([input_text])


    # 検索対象文の読み込み、ベクトル化 -> データベースから持ってくる
    # 変更する部分
    ################################################################################
    with open('/home/yanamoto/lecture/master_pbl/datasets/jades/train.comp', 'r') as f:
        lines = f.readlines()
        temp = model.encode(lines)
    ################################################################################

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

    # 確認
    # print(D)
    # print(I[0])
    # print('検索文：', input_text)
    # print('検索結果')
    # print([lines[I[0][0]].strip(), lines[I[0][1]].strip(), lines[I[0][2]].strip()])

    # 変更する部分
    ################################################################################
    # 類似文3つに対して、対応する平易文をデータベースからとってくる
    # [lines[I[0][0]].strip(), lines[I[0][1]].strip(), lines[I[0][2]].strip()]
    ################################################################################

    return [lines[I[0][0]].strip(), lines[I[0][1]].strip(), lines[I[0][2]].strip()]

if __name__=='__main__':
    input_text = 'シークワーサー独特の苦みを残した大人向けの味といい、試行錯誤して煮詰めた自信作を買い物客らに売り込んだ。'
    print(use_simcse(input_text))
