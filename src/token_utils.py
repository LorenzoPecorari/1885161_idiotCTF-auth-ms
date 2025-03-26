import jwt
import datetime

key="LabAdvanceProgramming"
valid_time=30

class Token:
    def token_generation(email):
        try:
            creation_time=datetime.datetime.now()
            expiration_time=creation_time+datetime.timedelta(minutes=valid_time)
            payload={
                "email": email,
                "creation_time": creation_time.timestamp(),
                "expiration_time": expiration_time.timestamp()
            }
            token=jwt.encode(payload, key, algorithm="HS256")
            return token
        except jwt.InvalidKeyError:
            return "Invalid key error"
        except jwt.InvalidAlgorithmError:
            return "Invalid algorithm error"
        except jwt.PyJWKError as e:
            return f"Error: {e}"
        except:
            return "An error has occurred"

    def token_is_valid(token):
        current_time=datetime.datetime.now()
        try:
            payload=jwt.decode(token, key, algorithms="HS256")
            expiration_time=datetime.datetime.fromtimestamp(payload["expiration_time"])
            if current_time<expiration_time:
                return True
            else:
                return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        except:
            return False
        
    def get_email(token):
        try:
            payload=jwt.decode(token, key, algorithms="HS256")
            return payload["email"]
        except:
            return "Invalid token"