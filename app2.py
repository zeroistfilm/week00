
from flask import Flask
# JWT 확장 라이브러리 임포트하기
from flask_jwt_extended import *

application = Flask(import_name = __name__)

# 토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
application.config.update(
			DEBUG = True,
			JWT_SECRET_KEY = "I'M IML"
		)

# JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(application)

@application.route("/")
def test_test():
	return "<h1>Hello, I'm IML!</h1>"

if __name__ == '__main__':
	application.run(host = '0.0.0.0',
					port = 5000,
					debug = True)