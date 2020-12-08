from flask import Flask, render_template, jsonify, request, session, escape
import requests
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.

app.secret_key = b"!@#$1234"

@app.route('/')
def home():
    return render_template('login_page.html')


@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.articles.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'articles': result})


@app.route('/login', methods=['POST', 'GET'])
def session_test():
    result = "";
    if request.method == "GET":
        if "username" in session:
            print("유지중")
            result = "유지중"
        else:
            print("세션없음")
            result = "세션없음"

        return result

    else:
        if "username" in session:
            print("유지중")
            result = escape(session['username'])
        else:
            print("세션없음")
            session['username'] = request.form['name']
            result = escape(session['username'])

        return render_template("login.html")

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
