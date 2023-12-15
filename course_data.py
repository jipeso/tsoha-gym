from db import db
import users
from flask import session
from sqlalchemy.sql import text


def get_list():
    try: 
        sql = text("SELECT * FROM courses WHERE visible=True")
        res = db.session.execute(sql)
        courses = res.fetchall()
        if not courses:
            return []
        else:
            return courses
    except:
        return False
    
def get_course(course_id):
    try:
        sql = text("SELECT * FROM courses WHERE id=:course_id")
        res = db.session.execute(sql, {"course_id":course_id})
        course = res.fetchone()
        if course is None:
            return False
        if course.visible is False:
            return False
        else:
            return course
    except:
        return None

def create_course(course_name,description, owner):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("INSERT INTO courses (name,description,owner) VALUES (:course_name, :description, :owner)")
        db.session.execute(sql, {"course_name":course_name, "description":description, "owner":owner})
        db.session.commit()
        return True
    except:
        return False
    
def enroll(course_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("INSERT INTO enrollments (user_id, course_id) VALUES (:user_id, :course_id)")
        db.session.execute(sql, {"user_id": user_id, "course_id": course_id})
        db.session.commit()
        return True
    except:
        return False

    
def edit_course(course_id, name, description):
    user_id = users.user_id()
    if user_id == 0:
        return False
    course = get_course(course_id)

    if course is None:
        return False
    
    if course:    
        if name or description:
            if name:
                sql = text("UPDATE courses SET name=:name WHERE id=:course_id")
                db.session.execute(sql, {"name":name, "course_id":course_id})
            if description:
                sql = text("UPDATE courses SET description=:description WHERE id=:course_id")
                db.session.execute(sql, {"description":description, "course_id":course_id})

            db.session.commit()
            return True
        
        return False
    else: 
        return False
    
def create_text_assignment(course_id,question,correct_answer):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("""INSERT INTO text_assignments (course_id, question, correct_answer) 
                   VALUES (:course_id, :question, :correct_answer)""")
        
        db.session.execute(sql, {"course_id":course_id, "question":question, "correct_answer":correct_answer})
        db.session.commit()
        return True
    except:
        return False
    
def get_text_assignment(assignment_id):
    try:
        sql = text("SELECT * FROM text_assignments WHERE id = :assignment_id")
        res = db.session.execute(sql, {"assignment_id":assignment_id})
        assignment = res.fetchone()
        if not assignment:
            return False
        else:
            return assignment
    except:
        return False
    
def get_text_assignments(course_id):
    try:
        sql = text("SELECT * FROM text_assignments WHERE course_id = :course_id")
        res = db.session.execute(sql, {"course_id":course_id})
        assignments = res.fetchall()
        if not assignments:
            return []
        else:
            return assignments
    except:
        return False 
       
def create_multiple_choice(course_id,question,correct_answer,choices):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("""INSERT INTO multiple_choices (course_id, question, correct_answer) 
                   VALUES (:course_id, :question, :correct_answer) RETURNING id""")
        res = db.session.execute(sql, {"course_id":course_id, "question":question, "correct_answer":correct_answer})
        multiple_choice_id = res.fetchone()[0]
        for choice in choices:
            if choice != "":
                sql = text("INSERT INTO choices (multiple_choice_id, choice) VALUES (:multiple_choice_id, :choice)")
                db.session.execute(sql, {"multiple_choice_id":multiple_choice_id, "choice":choice})
        db.session.commit()
        return True
    except:
        return False

def get_multiple_choice(multiple_choice_id):
    try:
        sql = text("SELECT * FROM multiple_choices WHERE id = :multiple_choice_id")
        res = db.session.execute(sql, {"multiple_choice_id":multiple_choice_id})
        assignment = res.fetchone()
        if not assignment:
            return False
        else:
            return assignment
    except:
        return False

def get_multiple_choices(course_id):
    try:
        sql = text("SELECT * FROM multiple_choices WHERE course_id = :course_id")
        res = db.session.execute(sql, {"course_id":course_id})
        assignments = res.fetchall()
        if not assignments:
            return []
        else:
            return assignments
    except:
        return False

def get_choices(multiple_choice_id):
    try:
        sql = text("SELECT id, choice FROM choices WHERE multiple_choice_id = :multiple_choice_id")
        res = db.session.execute(sql, {"multiple_choice_id":multiple_choice_id})
        choices = res.fetchall()
        if not choices:
            return False
        else:
            return choices
    except:
        return False
    
def delete_course(course_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    course = get_course(course_id)
    if course:
        sql = text("UPDATE courses SET visible=False WHERE id=:course_id")
        db.session.execute(sql, {"course_id":course_id})
        db.session.commit()
        return True
    else:
        return False

def add_material(course_id, title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    try:
        sql = text("INSERT INTO course_materials (course_id, title, content) VALUES (:course_id, :title, :content)")
        db.session.execute(sql, {"course_id":course_id, "title":title, "content":content})
        db.session.commit()
        return True
    except:
        return False

def get_materials(course_id):
    try:
        sql = text("SELECT id, title, content FROM course_materials WHERE course_id=:course_id")
        res = db.session.execute(sql, {"course_id":course_id})
        materials = res.fetchall()
        if materials is None:
            return []
        else:
            return materials
    except:
        return False
    
def check_multiple_choice(multiple_choice_id, course_id, choice_id):
    try:
        user_id = users.user_id()
        if user_id == 0:
            return False
        
        sql_check = text("SELECT COUNT(*) FROM user_correct_choices WHERE user_id=:user_id AND multiple_choice_id=:multiple_choice_id AND course_id=:course_id")
        res_check = db.session.execute(sql_check, {"user_id": user_id, "multiple_choice_id": multiple_choice_id, "course_id": course_id})
        existing_count = res_check.fetchone()[0]
        
        sql = text("SELECT correct_answer FROM multiple_choices WHERE id=:multiple_choice_id")
        res = db.session.execute(sql, {"multiple_choice_id":multiple_choice_id})
        correct = res.fetchone()[0]

        sql2 = text("SELECT choice FROM choices WHERE id = :choice_id")
        res2 = db.session.execute(sql2, {"choice_id":choice_id})
        answer = res2.fetchone()[0]

        if str(answer) != str(correct):
            return False
        
        if existing_count == 0:
            sql = text("INSERT INTO user_correct_choices (user_id, multiple_choice_id, course_id) VALUES (:user_id, :multiple_choice_id, :course_id)")
            db.session.execute(sql, {"user_id":user_id, "multiple_choice_id":multiple_choice_id, "course_id":course_id})
            db.session.commit()
            return True
        else:
            return True
    
    except:
        db.session.rollback()        
        return False


def check_text_assignment(text_assignment_id, course_id, answer):
    try:
        user_id = users.user_id()
        if user_id == 0:
            return False
        
        sql_check = text("SELECT COUNT(*) FROM user_correct_answers WHERE user_id=:user_id AND text_assignment_id=:text_assignment_id AND course_id=:course_id")
        res_check = db.session.execute(sql_check, {"user_id":user_id, "text_assignment_id":text_assignment_id, "course_id":course_id})
        existing_count = res_check.fetchone()[0]

        sql = text("SELECT correct_answer FROM text_assignments WHERE id=:text_assignment_id")
        res = db.session.execute(sql, {"text_assignment_id": text_assignment_id})
        correct = res.fetchone()[0]

        if str(answer) != str(correct):
            return False
        
        if existing_count == 0:
            sql_insert = text("INSERT INTO user_correct_answers (user_id, text_assignment_id, course_id) VALUES (:user_id, :text_assignment_id, :course_id)")
            db.session.execute(sql_insert, {"user_id":user_id, "text_assignment_id":text_assignment_id, "course_id":course_id})
            db.session.commit()
            return True
        else:
            return True
    
    except:
        db.session.rollback()
        return False


def total_completed_assignments(course_id, user_id):
    sql = text("SELECT COUNT(*) FROM user_correct_choices WHERE course_id=:course_id AND user_id=:user_id")
    res = db.session.execute(sql, {"course_id": course_id, "user_id": user_id})
    multi_choices = res.fetchone()[0]
    
    sql2 = text("SELECT COUNT(*) FROM user_correct_answers WHERE course_id=:course_id AND user_id=:user_id")
    res2 = db.session.execute(sql2, {"course_id": course_id, "user_id": user_id})
    text_assignments = res2.fetchone()[0]

    total = int(multi_choices) + int(text_assignments)
    return total
    

def get_students(course_id):
    sql = text("SELECT u.id, u.username FROM users u JOIN enrollments e ON u.id = e.user_id JOIN courses c ON c.id = e.course_id WHERE c.id = :course_id")
    res = db.session.execute(sql, {"course_id": course_id})
    students = res.fetchall()

    students_with_assignments = []
    for student_id, username in students:
        total_assignments = total_completed_assignments(course_id, student_id)
        students_with_assignments.append((student_id, username, total_assignments))

    return students_with_assignments