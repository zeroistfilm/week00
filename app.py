from datetime import timedelta

import flask
from flask import Flask, render_template, jsonify, request, session, escape, redirect, flash, url_for
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

# client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
client = MongoClient('mongodb://test:test@54.180.91.148', 27017)
# db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.
db = client.jungglebook
app.secret_key = b"!@#$1234"

#----------------------------SH-----------------------------------
#----------------------------SH-----------------------------------
#----------------------------SH-----------------------------------

@app.route('/qna/add', methods=['POST'])
def addQNA():
    content_receive = request.form['content_give']
    type_receive = request.form['type_give']


    if type_receive=='q':
        db.QandA.insert_one({'qa_uid': str(id_receive)})

        return jsonify({"result": "success"})

@app.route('/qna/modify')
def modifyQNA():
    qnas = db.QandA.find({}, {'_id': False})

@app.route('/qna/delete', methods=['POST'])
def deleteQNA():
    id_receive = request.form['id_give']
    type_receive = request.form['type_give']

    if type_receive=='q':
        print('q')
        db.QandA.delete_one({'qa_uid': str(id_receive)})
    else:
        print('a')
        db.QandA.update_one({'qa_uid': str(id_receive)}, {'$set': {'answer':'','userkey_a':''}})

    return jsonify({"result": "success"})

#----------------------------SH-----------------------------------
#----------------------------SH-----------------------------------
#----------------------------SH-----------------------------------


#----------------------------JH-----------------------------------
#----------------------------JH-----------------------------------
#----------------------------JH-----------------------------------

@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for('loadhome'))
    else:
        return render_template('login_page.html')

@app.route('/main')
def loadhome():
    qnas = db.QandA.find({}, {'_id': False})
    if "username" in session:
        return render_template('main.html', qnas=qnas)
    else:
        return render_template('login_page.html')

@app.route('/signup', methods=['POST'])
def signUp():
    # id_receive = request.form['id']  # 클라이언트로부터 id을 받는 부분
    # password_receive = request.form['password']  # 클라이언트로부터 password 받는 부분
    id_receive = 'zeroistfilm'
    password_receive = '1234'
    userInfo = {'id': id_receive, 'password': password_receive}
    # 3. mongoDB에 데이터를 넣기
    db.userDB.insert_one(userInfo)

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
        user_id = request.form['id_give']
        user_password = request.form['password_give']
        user = db.userDB.find_one({'id': str(user_id), 'password': str(user_password)})

        if user:
            if "username" in session:
                print("유지중")
                result = escape(session['username'])
            else:
                print("세션없음")
                session['username'] = user_id
                result = escape(session['username'])

            return jsonify({"result": "success"})
        else:

            return jsonify({"result": "일치하는 유저가 없습니다."})

@app.route('/logout')
def logout():
    session.pop('username', None)
    print('로그아웃 되었습니다.')
    return redirect(url_for('home'))

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

#----------------------------JH-----------------------------------
#----------------------------JH-----------------------------------
#----------------------------JH-----------------------------------


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
