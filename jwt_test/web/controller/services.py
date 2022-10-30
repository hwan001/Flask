from datetime import datetime

from flask import Flask
from flask import Response

from web import config


class Services:
    def __init__(self, current_app):
        self.current_app = current_app
    
    # token을 decode하여 반환함, decode에 실패하는 경우 payload = None으로 반환
    def check_access_token(self, access_token):
        try:
            payload = jwt.decode(access_token, self.current_app.config['JWT_SECRET_KEY'], "HS256")
            if payload['exp'] < datetime.utcnow():  # 토큰이 만료된 경우
                payload = None
        except jwt.InvalidTokenError:
            payload = None

        return payload


    # decorator 함수
    def login_required(self, f):
        def decorated_function(*args, **kwagrs):
            access_token = request.headers.get('Authorization') # 요청의 토큰 정보를 받아옴
            if access_token is not None: # 토큰이 있는 경우
                payload = self.check_access_token(access_token) # 토큰 유효성 확인
                if payload is None: # 토큰 decode 실패 시 401 반환
                    return  Response(status=401)
            else: # 토큰이 없는 경우 401 반환
                return Response(status=401)

            return f(*args, **kwagrs)

        return decorated_function
