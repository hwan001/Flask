import sys
import subprocess

try:
    import jwt

except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    import jwt


class Jwt():
    def __init__(self, payloads, secret_key):
        self.payloads = payloads
        self.algorithm = "HS256"
        self.secret_key = secret_key

    def create_token(self):
        return jwt.encode(self.payloads, key=self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, key=self.secret_key, algorithms=self.algorithm)
        except jwt.ExpiredSignatureError:
            return "토큰 인증 만료"
        except jwt.InvalidTokenError:
            return "토큰 검증 실패"
        
        return payload


if __name__ == '__main__':
    payload = {"id":"hwan"}
    my_jwt = Jwt(payload, "secret")
    token = my_jwt.create_token()

    print("token : ", token)
    print("payload : ", my_jwt.verify_token(token))
    