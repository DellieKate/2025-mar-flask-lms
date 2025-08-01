from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.course import Course
from schemas.schemas import courses_schema, course_schema

course_bp = Blueprint ("course", __name__, url_prefix="/courses")

@course_bp.route("/")
def get_courses():
    stmt = db.select(Course)
    courses_list = db.session.scalars(stmt) #Python object
    data = courses_schema.dump(courses_list) #JavaScript JSON object
    
    #to print names in python object
    # For understanding Python objects and JSON objects
    # courses_list_a = list(db. session. scalars(stmt))
    # print([course. name for course in courses_list_al)
    # course_json = [course ["name"] for course in datal
    # print(course_json)

    if data:
        #fetch only names in Json data
        #course_json = [course["name"] for course in data]
        #print(course_json)
    
        return jsonify(data)
    else:
        return {"message": "No course records found."}, 404
    
    
@course_bp.route("/<int:course_id>")
def get_a_course(course_id):
    stmt = db.select(Course).where(Course.id == course_id)
    course = db.session.scalar(stmt)
    
    if course:
        #serialise it
        data = course_schema.dump(course)
        return jsonify(data)
    else: 
        return {"message": f"Course with id {course_id} does not exist."}, 404
                                    
# POST /
@course_bp.route("/", methods=["POST"])
def create_a_course():
    try:
        # GET info from the REQUEST body
        body_data = request.get_json()
        
        #Create a Course Object from Course class with body response data
        new_course = Course(
            name = body_data.get("name"),
            duration = body_data.get("duration"),
            teacher_id = body_data.get("teacher_id")
        )
        
        # Add the new course data to the session
        db.session.add(new_course)
        
        # commit the session
        db.session.commit()
        
        
        return jsonify(course_schema.dump(new_course)), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"Required field {err.orig.diag.column_name} cannot be null."}, 400 
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Course name has to be unique."}, 400
        else:    
            return {"message": "Unexpected error occured."}, 400
        
@course_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    stmt = db.select(Course).where(Course.id == course_id)
    course = db.session.scalar(stmt)
    
    if course:
        db.session.delete(course)
        db.session.commit()
        return {"message": f"Course '{course.name}' has been removed successfully."}, 200
    
    else:
        return {"message": f"Course with id '{course_id}' does not exist"}, 404


@course_bp.route("/<int:course_id>", methods=["PUT", "PATCH"])
def update_course(course_id):
    try:
        stmt = db.select(Course).where(Course.id == course_id)
        course = db.session.scalar(stmt)
        if course:
            # get the course with id
            body_data = request.get_json()
            course.name = body_data.get("name") or course.name
            course.duration = body_data.get("duration") or course.duration
            course.teacher_id = body_data.get("teacher_id") or course.teacher_id
        
            db.session.commit()
            
            return jsonify(course_schema.dump(course))
        
        else:
            return {"message": f"Course with id {course_id} does not exist."}, 404
        
    except IntegrityError:
        return {"message": "Name must be unique."}, 400
    except DataError as err:     
        return {"message": err.orig.diag.message_primary}, 400
        

    
    
    





