from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.teacher import Teacher
from schemas.schemas import teachers_schema, teacher_schema

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teachers")

# Routes
# GET / teachers/
@teacher_bp.route("/")
def get_teachers():
    department = request.args.get("department")
    if department:
        stmt = db.select(Teacher).where(Teacher.department == department).order_by(Teacher.id)
    else:
        # Define the GET statement
        # SELECT * FROM teacher;
        stmt = db.select(Teacher).order_by(Teacher.id)
        
    teachers_list = db.session.scalars(stmt) #Python object
    data = teachers_schema.dump(teachers_list) #JavaScript JSON object
    
    #to print names in python object
    # For understanding Python objects and JSON objects
    # teachers_list_a = list(db. session. scalars(stmt))
    # print([teacher. name for teacher in teachers_list_al)
    # teacher_json = [teacher ["name"] for teacher in datal
    # print(teacher_json)

    if data:
        #fetch only names in Json data
        #teacher_json = [teacher["name"] for teacher in data]
        #print(teacher_json)
    
        return jsonify(data)
    else:
        return {"message": "No teacher records found."}, 404
    
    
@teacher_bp.route("/<int:teacher_id>")
def get_a_teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)
    
    if teacher:
        #serialise it
        data = teacher_schema.dump(teacher)
        return jsonify(data)
    else: 
        return {"message": f"Teacher with id {teacher_id} does not exist."}, 404
                                    

@teacher_bp.route("/", methods=["POST"])
def create_a_teacher():
    try:
        body_data = request.get_json()
        new_teacher = Teacher(
            name = body_data.get("name"),
            department = body_data.get("department"),
            address = body_data.get("address")
        )
        
        db.session.add(new_teacher)
        db.session.commit()
        
        return jsonify(teacher_schema.dump(new_teacher)), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null."}, 400 
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Department has to be unique."}, 400
        else:    
            return {"message": "Unexpected error occured."}, 400
        
@teacher_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)
    
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {"message": f"Teacher '{teacher.name}' has been removed successfully."}, 200
    
    else:
        return {"message": f"Teacher with id '{teacher_id}' does not exist"}, 404


@teacher_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)
    if teacher:
        body_data = request.get_json()
        teacher.name = body_data.get("name") or teacher.name
        teacher.department = body_data.get("department") or teacher.department
        teacher.address = body_data.get("address") or teacher.address
       
        db.session.commit()
        
        return jsonify(teacher_schema.dump(teacher))
    
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist."}, 404
        
        
        

    
    
    

