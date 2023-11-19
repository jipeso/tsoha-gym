from db import db
import users
from flask import session
from sqlalchemy.sql import text


def get_list():
    sql = text("SELECT name FROM courses")
    result = db.session.execute(sql)
    return result.fetchall()

def enroll(course_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO enrollments (user_id, course_id) VALUES (:user_id, :course_id)")
    db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    db.session.commit()
    return True

#def create_course():