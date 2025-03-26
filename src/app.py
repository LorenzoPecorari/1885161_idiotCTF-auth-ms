from flask import Flask
from flask_cors import CORS
from config import SQLALCHEMY_DATABSE_URI
from models import db
from user_routes import bp_user
from auth_routes import bp_auth

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=SQLALCHEMY_DATABSE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db.init_app(app)
app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)

@app.cli.command("create-db")
def create_db():
    with app.app_context():
        db.create_all()


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8080, debug=True)