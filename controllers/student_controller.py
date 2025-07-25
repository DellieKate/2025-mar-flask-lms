from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.student import Student, students_schema, student_schema

student_bp = Blueprint("student", __name__, url_prefix="/students")

@student_bp.route("/")
def get_students():
    stmt = db.select(Student)
    students_list = db.session.scalars(stmt) #Python object
    data = students_schema.dump(students_list) #JavaScript JSON object
    
    #to print names in python object
    # For understanding Python objects and JSON objects
    # students_list_a = list(db. session. scalars(stmt))
    # print([student. name for student in students_list_al)
    # student_json = [student ["name"] for student in datal
    # print(student_json)

    if data:
        #fetch only names in Json data
        #student_json = [student["name"] for student in data]
        #print(student_json)
    
        return jsonify(data)
    else:
        return {"message": "No student records found."}, 404
    
    
@student_bp.route("/<int:student_id>")
def get_a_student(student_id):
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    
    if student:
        #serialise it
        data = student_schema.dump(student)
        return jsonify(data)
    else: 
        return {"message": f"Student with id {student_id} does not exist."}, 404
                                    

@student_bp.route("/", methods=["POST"])
def create_a_student():
    try:
        body_data = request.get_json()
        new_student = Student(
            name = body_data.get("name"),
            email = body_data.get("email"),
            address = body_data.get("address")
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        return jsonify(student_schema.dump(new_student)), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null."}, 400 
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Email has to be unique."}, 400
        else:    
            return {"message": "Unexpected error occured."}, 400
        
@student_bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    
    if student:
        db.session.delete(student)
        db.session.commit()
        return {"message": f"Student '{student.name}' has been removed successfully."}, 200
    
    else:
        return {"message": f"Student with id '{student_id}' does not exist"}, 404


@student_bp.route("/<int:student_id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    if student:
        body_data = request.get_json()
        student.name = body_data.get("name") or student.name
        student.email = body_data.get("email") or student.email
        student.address = body_data.get("address") or student.address
       
        db.session.commit()
        
        return jsonify(student_schema.dump(student))
    
    else:
        return {"message": f"Student with id {student_id} does not exist."}, 404
        
        
        

    
    
    

