from init import db


class Student(db.Model):
    __tablename__ = "students"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    address = db.Column(db.String(100))
    
    #Many enrolments to one student
    enrolments = db.relationship("Enrolments", back_populates = "student", cascade="all, delete")
    
    # cascade means when the student drops or student is deleted, the corresponding enrolment should be deleted

