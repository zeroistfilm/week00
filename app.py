from flask import Flask, render_template, jsonify, request,session
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

#client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
client = MongoClient('mongodb://test:test@54.180.91.148',27017)
#db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.
db = client.jungglebook

@app.route('/')
def home():

    return render_template('login_page.html')



@app.route('/login', methods=['POST'])
def signUp():
    # id_receive = request.form['id']  # 클라이언트로부터 id을 받는 부분
    # password_receive = request.form['password']  # 클라이언트로부터 password 받는 부분
    id_receive = 'zeroistfilm'
    password_receive = '1234'
    userInfo = {'id': id_receive, 'password': password_receive}
    # 3. mongoDB에 데이터를 넣기
    db.userDB.insert_one(userInfo)



@app.route('/login', methods=['GET'])
def checkUser():
    result = list(db.userDB.find({}, {'_id': 0}))
   

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)