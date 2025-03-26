import redis
import json

class MailSender:
    def __init__(self, redis_host='redis', redis_port=6379, queue_name='email_queue'):
        self.queue_name = queue_name
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    def user_activation(self, email):
        email_data = {
            "to_email": email,
            "subject": "User Activation",
            "body": f"Welcome to Idiot-CTF! Please activate your account with the following link: http://localhost:3000/useractivation?email={email}"
        }
        email_data_json = json.dumps(email_data)
        self.redis_client.lpush(self.queue_name, email_data_json)
        print(f"Email data pushed to queue: {email_data_json}")


