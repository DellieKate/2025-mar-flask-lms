from flask import Blueprint, jsonify
from init import db
from models.student import Student, students_schema

student_bp = Blueprint("student", __name__, url_prefix="/students")

@student_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt) #Python object
    data = students_schema.dump(students_list) #JavaScript JSON object
    
    if data != []:
        return jsonify(data)
    else:
        return {"message": "No student records found."}, 404
    




