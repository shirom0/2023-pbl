from flask import Flask, render_template, request, redirect,  url_for, redirect, session
import random
from pycode import gettrain, gettrain_re
from datetime import timedelta 

app = Flask(__name__)

@app.route('/')
def top_page():
    return render_template('form.html')

@app.route('/input_reset', methods = ["POST"])
def move_top():
    return redirect(url_for('top_page'))

@app.route('/got_samples', methods = ["POST"])
def random_select():
    if request.method == "POST":
        mode = str(request.form.get('mode', ''))    #ランダム or 関連
        original = request.form.get('original_text')    #平易化したい原文の取得
        input_text = str(original)
        
        # 入力文が空
        if len(input_text) == 0:
            error_message = "入力に不備があります"
            return render_template('form.html', error_message = error_message)

        # modeによって呼び出す関数を変える
        if mode == "random":
            data = gettrain.getTrainData()  #サンプルデータをリスト構造で取得
        if mode == "related":
            data = gettrain_re.getTrainData(input_text)
        if mode == "":
            error_message = "サンプル文の選択方法を指定してください"
            return render_template('form.html', error_message = error_message)
        
        
        return render_template('form.html', o1 = data[0], s1 = data[1], o2 = data[2], s2 = data[3], o3 = data[4], s3 = data[5], original = original)

@app.route('/got_answer', methods = ["GET", "POST"])
def submit_texts():
    if request.method == "POST":
        o1 = request.form.get('sample_o1')
        s1 = request.form.get('sample_s1')
        o2 = request.form.get('sample_o2')
        s2 = request.form.get('sample_s2')
        o3 = request.form.get('sample_o3')
        s3 = request.form.get('sample_s3')
        original = request.form.get('original_area')
        simpled = "平易化済み文出力予定"
        if o1 != '' and s1 != '' and o2 != '' and s2 != '' and o3 != '' and s3 != '' and original != '':
            return render_template('form.html', o1 = o1, s1 = s1, o2 = o2, s2 = s2, o3 = o3, s3 = s3,
                                                original = original, simpled = simpled)
        else:
            error_message = "入力に不備があります"
            return render_template('form.html', error_message = error_message)
    else:
        return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True) #仮想サーバで動作させるにはhost指定しないと動かなかった