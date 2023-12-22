import mysql.connector
import random

def getTrainData():

    shot = 3
    
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

    for i in range(shot):
        art_id = random.randint(1, num_article)
        cursor.execute(fetch_sql, (art_id, ))
        sample_data.append(cursor.fetchall())
    
    cursor.close()

    sample_pair = []
    for i in range(shot):
        sample_pair.append(sample_data[i][0][1])
        sample_pair.append(sample_data[i][0][2])
    
    print(sample_pair)
    
    if cnx is not None and cnx.is_connected():
        cnx.close()

    return sample_pair


