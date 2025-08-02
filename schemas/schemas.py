from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.enrolment import Enrolment

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        include_relationships = True
        fields = ("id", "name", "email", "address", "enrolments")
        ordered = True
    
    #needs to in a list since a student can have multiple enrolments
    enrolments = fields.List(fields.Nested("EnrolmentSchema", only=("id", "enrolment_date", "course")))
        

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
        ordered = True
        fields = ("id", "name", "duration", "teacher", "enrolments")
        
        
    # name = fields.String(required=True, validate=And(
    #   Length(min=2, error="Course names must be at least 2 characters long."),
    #   Regexp("[A-Za-z][A-Za-z0-9 ]*$", error="Only letters, numbers and spaces are allowed.")  
    # ))
    
    # duration = fields.Float(allow_nan=False, required=False)
    
    teacher = fields.Nested("TeacherSchema", only=("id","name", "department"))
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=("course",)))
    
class EnrolmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrolment
        load_instance = True
        include_relationships = True
        include_fk = True
        ordered = True
        fields = ("id", "enrolment_date","student_id", "course_id","student", "course")
        
        
    student = fields.Nested("StudentSchema", only=("id", "name"))
    course = fields.Nested("CourseSchema", only=("id", "name"))


#Student Schema for converting a single entry
student_schema = StudentSchema()
#Student Schema for converting multiple entries
students_schema = StudentSchema(many=True)
     
teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)  

enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many=True)  

