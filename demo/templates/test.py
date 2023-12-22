from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def top_page():
    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True) #仮想サーバで動作させるにはhost指定しないと動かなかった