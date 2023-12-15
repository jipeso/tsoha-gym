from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets


def login(username, password):
    sql = text("SELECT id, password, username, role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["user_role"] = user.role
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]
    del session["csrf_token"]

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password,role) VALUES (:username,:password,:role)")
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def username():
    return session.get("username", 0)

def user_role():
    return session.get("user_role",0)

def get_courses():
    user_id = session.get("user_id", 0)

    sql = text("""SELECT c.id
                FROM users u   
                JOIN enrollments e ON u.id = e.user_id
                JOIN courses c ON e.course_id = c.id
                WHERE e.user_id = :user_id
                """)
    res = db.session.execute(sql, {"user_id": user_id})
    courses = res.fetchall()
    if courses:
        course_id_list = [course[0] for course in courses]
        return course_id_list
    else:
        return []
    
def get_enrollments():   
        user_id = session.get("user_id", 0)
        sql = text("SELECT course_id FROM enrollments WHERE user_id=:user_id")
        res = db.session.execute(sql,{"user_id":user_id})
        enrollments = res.fetchall()
        if not enrollments:
            return []
        else:
            list = [enrollment[0] for enrollment in enrollments]
            return list
    
def leave_course(course_id):
    user_id = session.get("user_id", 0)
    if user_id:
        try:
            sql = text("DELETE FROM enrollments WHERE user_id = :user_id AND course_id = :course_id")
            db.session.execute(sql, {"user_id": user_id, "course_id": course_id})
            db.session.commit()
            return True
        except:
            return False 
    return False


def get_correct_mc_list():
    user_id = session.get("user_id", 0)
    sql = text("SELECT multiple_choice_id FROM user_correct_choices WHERE user_id=:user_id")
    res = db.session.execute(sql, {"user_id":user_id})
    answers = res.fetchall()

    if not answers:
        return [] 
    else:
        mc_list = [answer[0] for answer in answers]
        return mc_list
  
def get_correct_ta_list():
    user_id = session.get("user_id", 0)
    sql = text("SELECT text_assignment_id FROM user_correct_answers WHERE user_id=:user_id")
    res = db.session.execute(sql, {"user_id":user_id})
    answers = res.fetchall()

    if not answers:
        return []
    else:
        ta_list = [answer[0] for answer in answers]
        return ta_list
    
