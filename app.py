from datetime import timedelta
import time
import jwt
import flask
from flask import Flask, render_template, jsonify, request, session, escape, redirect, flash, url_for
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

# client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
client = MongoClient('mongodb://test:test@54.180.91.148', 27017)
# db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.
db = client.jungglebook
app.secret_key = b"!@#$1234"


# ----------------------------SH-----------------------------------
# ----------------------------SH-----------------------------------
# ----------------------------SH-----------------------------------

@app.route('/qna/add', methods=['POST'])
def addQNA():
    content_receive = request.form['content_give']
    type_receive = request.form['type_give']

    if type_receive == 'q':
        db.QandA.insert_one({'qa_uid': str(id_receive)})

        return jsonify({"result": "success"})


@app.route('/qna/modify')
def modifyQNA():
    qnas = db.QandA.find({}, {'_id': False})


@app.route('/qna/delete', methods=['POST'])
def deleteQNA():
    id_receive = request.form['id_give']
    type_receive = request.form['type_give']

    if type_receive == 'q':
        print('q')
        db.QandA.delete_one({'qa_uid': str(id_receive)})
    else:
        print('a')
        db.QandA.update_one({'qa_uid': str(id_receive)}, {'$set': {'answer': '', 'userkey_a': ''}})

    return jsonify({"result": "success"})


# ----------------------------SH-----------------------------------
# ----------------------------SH-----------------------------------
# ----------------------------SH-----------------------------------


# ----------------------------JH-----------------------------------
# ----------------------------JH-----------------------------------
# ----------------------------JH-----------------------------------

@app.route('/')
def home():
    if "userkey" in session:
        return redirect(url_for('loadhome'))
    else:
        return render_template('login_page.html')


@app.route('/main')
def loadhome():
    if "userkey" in session:
        qnas = db.QandA.find({}, {'_id': False})
        cnt_user = db.userDB.find_one({'key': session['userkey']})
        crn_user_name = cnt_user['name']
        cnt_user_status = cnt_user['usertype']
        cnt_status = "-1"
        if cnt_user_status == "1":
            cnt_status = "교육생"
        elif cnt_user_status == "2":
            cnt_status = "운영진"
        else:
            cnt_status = "UNKOWN"

        infos = list(db.info.find({}, {"_id": False}))
        infosFinduser = []
        for info in infos:
            key = info["userkey"]
            user = db.userDB.find_one({'key': str(key)})
            if user != None:
                infosFinduser.append(user)

        print(len(infos))
        print(len(infosFinduser))

        infos_package = [infos, infosFinduser]

        return render_template('main.html', qnas=qnas, infos_package=infos_package, cnt_user=crn_user_name,
                               cnt_status=cnt_status)
    else:
        return render_template('login_page.html')


@app.route('/postinfo', methods=['POST'])
def postInfo():
    now = time.gmtime(time.time())
    info_title_receive = request.form["info_title_give"]
    info_contents_receive = request.form["info_contents_give"]
    info_url_receive = request.form["info_url_give"]
    info_uid = "info." + str(now.tm_year) + "." + str(now.tm_mon) + "." + str(now.tm_mday) + "." + str(
        now.tm_hour) + "." + str(now.tm_min) + "." + str(now.tm_sec)

    info = {
        "title": info_title_receive,
        "contents": info_contents_receive,
        "url": info_url_receive,
        "uid": info_uid,
        "userkey": session["userkey"]
    }

    db.info.insert_one(info)

    return jsonify({"result": "success"})


@app.route('/signup', methods=['POST'])
def signUp():
    id_receive = request.form["id_give"]
    password_receive = request.form["password_give"]
    name_receive = request.form["name_give"]
    usertype_receive = request.form["usertype"]
    encoded_password = jwt.encode({'password': password_receive}, "junglebook", algorithm='HS512')
    now = time.gmtime(time.time())
    key = str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec)
    userInfo = {'id': id_receive, 'password': encoded_password, "name": name_receive, "usertype": usertype_receive,
                "key": key}
    print(userInfo)

    # # 3. mongoDB에 데이터를 넣기
    db.userDB.insert_one(userInfo)
    return jsonify({"result": "success"})


@app.route('/login', methods=['POST', 'GET'])
def session_test():
    result = ""
    if request.method == "GET":
        if "userkey" in session:
            print("유지중")
            result = session["userkey"]
        else:
            print("세션없음")
            result = "세션없음"

        return result

    else:
        user_id = request.form['id_give']
        user_password = request.form['password_give']
        encoded_password = jwt.encode({'password': user_password}, 'junglebook', algorithm='HS512')
        user = db.userDB.find_one({'id': user_id, 'password': encoded_password})

        if user:
            if "userkey" in session:
                print("유지중")
                result = escape(session['userkey'])
            else:
                print("세션생성")
                session['userkey'] = user['key']
                result = escape(session['userkey'])

            return jsonify({"result": "success"})
        else:
            return jsonify({"result": "일치하는 유저가 없습니다."})


@app.route('/logout')
def logout():
    session.pop('userkey', None)
    print('로그아웃 되었습니다.')
    return redirect(url_for('home'))


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


# ----------------------------JH-----------------------------------
# ----------------------------JH-----------------------------------
# ----------------------------JH-----------------------------------

# ----------------------------YD-----------------------------------
# ----------------------------YD-----------------------------------
# ----------------------------YD-----------------------------------


@app.route('/develophistory', methods=['POST'])
def post_develophistory():
    title_receive = request.form['title_give']  # 클라이언트로부터 url을 받는 부분
    contents_receive = request.form['contents_give']  # 클라이언트로부터
    id_receive = request.form['id_give']  #
    userKey = session['userkey']

    history = {'id': id_receive, 'title': title_receive, 'contents': contents_receive, 'userkey': userKey}
    db.history.insert_one(history)

    return jsonify({'result': 'success'})


@app.route('/develophistory', methods=['GET'])
def read_develophistory():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    # user = db.userDB.find_one({'key': str(key)})

    historys = list(db.history.find({}, {'_id': 0}))
    userKey = session['userkey']

    print(historys)
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'historys': historys})


# ----------------------------YD-----------------------------------
# ----------------------------YD-----------------------------------
# ----------------------------YD-----------------------------------
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
