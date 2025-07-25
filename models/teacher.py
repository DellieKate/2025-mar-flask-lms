from init import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Teacher(db.Model):
    
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(100), nullable = False, unique=True)
    address = db.Column(db.String(100))
    
    courses = db.realtionship("Course", back_populates="teacher")
    
class TeacherSchema(SQLAlchemyAutoSchema):
    courses = fields.List(fields.Nested("CourseSchema", exclude=("teacher",)))
    class Meta:
        model = Teacher 
        load_instance = True
        
teacher_schema = TeacherSchema()

teachers_schema = TeacherSchema(many=True)


