from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


from models.student import Student
from models.teacher import Teacher
from models.course import Course

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher 
        load_instance = True
        include_fk = True
        include_relationship = True
        fields = ("id", "name", "department", "address", "courses")
        ordered = True
    
    courses = fields.List(fields.Nested("CourseSchema", exclude=("teacher","id",)))  

class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        include_relationship = True
        fields = ("id", "name", "duration", "teacher")
        
    # name = fields.String(required=True, validate=And(
    #   Length(min=2, error="Course names must be at least 2 characters long."),
    #   Regexp("[A-Za-z][A-Za-z0-9 ]*$", error="Only letters, numbers and spaces are allowed.")  
    # ))
    
    # duration = fields.Float(allow_nan=False, required=False)
    
    teacher = fields.Nested("TeacherSchema", only=("id","name", "department"))
        

student_schema = StudentSchema()

students_schema = StudentSchema(many=True)
     
teacher_schema = TeacherSchema()

teachers_schema = TeacherSchema(many=True)

course_schema = CourseSchema()

courses_schema = CourseSchema(many=True)  

