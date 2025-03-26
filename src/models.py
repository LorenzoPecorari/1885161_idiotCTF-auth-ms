from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    matricola=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    surname=db.Column(db.String(30), nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True)
    gender=db.Column(db.String(10), nullable=False)
    dob=db.Column(db.Date, nullable=True) #DateOfBirth
    password=db.Column(db.String(20), nullable=False)
    university=db.Column(db.String(50), nullable=False)
    role=db.Column(db.String(15), nullable=False)
    is_activated=db.Column(db.Boolean, default=False)

    def to_dict(self):
        return  {"matricola": self.matricola, "name": self.name, "surname": self.surname,
                 "email": self.email, "gender": self.gender, "dob": self.dob,
                 "password": self.password, "university": self.university, "role": self.role,
                 "is_activated": self.is_activated}