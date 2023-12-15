from app import app
from flask import render_template, request, redirect, flash, session, abort
import users
import course_data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():    
    return render_template("profile.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        role = request.form["role"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username,password1,role):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        

@app.route("/courses", methods=["GET"])
def courses():
    courses = course_data.get_list()
    user_course_ids = users.get_courses()

    return render_template("courses.html", courses=courses, user_course_ids=user_course_ids)
        
@app.route("/create_course", methods=["GET","POST"])
def create_course():
    if request.method == "GET":
        return render_template("create_course.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        course_name = request.form["course_name"]
        description = request.form["description"]
        owner = request.form["owner"]
        if course_data.create_course(course_name,description,owner):
            return redirect("/courses")
        else:
            return render_template("error.html", message="Kurssin luominen ei onnistunut")

@app.route("/enroll/<int:id>", methods=["POST"])
def enroll(id):
    if course_data.enroll(id):
        return redirect("/courses")
    else:
        return render_template("error.html", message="Kurssille liittyminen ei onnistunut")
    
@app.route("/view_course/<int:id>", methods=["GET", "POST"])
def view_course(id):
    if request.method == "GET":
        course = course_data.get_course(id)
        text_assignments = course_data.get_text_assignments(id)
        multiple_choices = course_data.get_multiple_choices(id)
        materials = course_data.get_materials(id)
        user_correct_mcs = users.get_correct_mc_list()
        user_correct_tas = users.get_correct_ta_list()
        students = course_data.get_students(id)

        return render_template("view_course.html", course=course, text_assignments=text_assignments, multiple_choices=multiple_choices, materials=materials,  user_correct_mcs=user_correct_mcs, user_correct_tas=user_correct_tas, students=students)

    
@app.route("/edit_course/<int:id>", methods=["GET", "POST"])
def edit_course(id):
    if request.method == "GET":
        course = course_data.get_course(id)
        return render_template("edit_course.html", course=course)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_name = request.form["course_name"]
        new_description = request.form["description"]

        if course_data.edit_course(id, new_name, new_description):
                return redirect("/view_course/" + str(id))        
        else:
            return render_template("error.html", message="Kurssin muokkaus ei onnistunut")   
            
@app.route("/create_text_assignment/<int:id>", methods=["GET", "POST"])
def create_text_assignment(id):
    if request.method == "GET":
        course = course_data.get_course(id)
        return render_template("create_text_assignment.html", course=course)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        question = request.form["question"]        
        answer = request.form["answer"]
        if course_data.create_text_assignment(id,question,answer):
            return redirect("/view_course/" + str(id))
        else:
            return render_template("error.html", message="Tekstivastauksellisen tehtävän luominen ei onnistunut")
        
@app.route("/create_multiple_choice/<int:course_id>", methods=["GET", "POST"])
def create_multiple_choice(course_id):
    if request.method == "GET":
        course = course_data.get_course(course_id)
        return render_template("create_multiple_choice.html", course=course)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        question = request.form["question"]
        correct_answer = request.form["correct_answer"]
        choices = request.form.getlist("choice")

        if course_data.create_multiple_choice(course_id,question,correct_answer,choices):
            return redirect("/view_course/" + str(course_id))
        else:
            return render_template("error.html", message="Monivalintatehtävän luominen luominen ei onnistunut")


@app.route("/delete_course/<int:id>", methods=["GET","POST"])  
def delete_course(id):
    if request.method == "GET":
        course = course_data.get_course(id)
        return render_template("delete_course.html", course=course)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if course_data.delete_course(id):
            return redirect("/courses")
        else:
            return render_template("error.html", message="Kurssin poistaminen ei onnistunut")

@app.route("/leave_course/<int:id>", methods=["GET","POST"])
def leave_course(id):
    enrollments = users.get_enrollments()
    course = course_data.get_course(id)
    if request.method == "GET":
        return render_template("leave_course.html", course=course)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if id in enrollments:
            if users.leave_course(id):
                return redirect("/courses")
            else:
                return render_template("error.html", message="Kurssilta poistuminen ei onnistunut")
        else:
            return render_template("error.html", message="Kurssia ei löytynyt omista kursseista")
    
@app.route("/add_material/<int:id>", methods=["GET","POST"])
def add_material(id):
    if request.method =="GET":
        course = course_data.get_course(id)
        return render_template("add_material.html", course=course)
    if request.method =="POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        title = request.form["title"]
        content = request.form["content"]
        if course_data.add_material(id,title,content):
            return redirect("/view_course/" + str(id))
        else:
            return render_template("error.html", message="Virhe kurssimateriaalia lisätessä")

@app.route("/multiple_choice/<multiple_choice_id>", methods=["GET", "POST"])
def multiple_choice(multiple_choice_id):

    assignment = course_data.get_multiple_choice(multiple_choice_id)
    choices = course_data.get_choices(multiple_choice_id)

    if request.method == "GET":
        return render_template("multiple_choice.html", assignment=assignment,choices=choices)
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        choice_id = request.form["answer"]
        course_id = request.form["course_id"]   
        if course_data.check_multiple_choice(multiple_choice_id,course_id,choice_id):
            flash("Vastaus oikein!")
            return redirect("/view_course/"+ str(course_id))
        else:
            flash("Vastaus väärin!")
            return redirect("/view_course/" + str(course_id))

@app.route("/text_assignment/<int:text_assignment_id>", methods=["GET", "POST"])
def text_assignment(text_assignment_id):

    assignment = course_data.get_text_assignment(text_assignment_id)

    if request.method == "GET":
        return render_template("text_assignment.html", assignment=assignment)
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        answer = request.form["answer"]
        course_id = request.form["course_id"]
        
        if course_data.check_text_assignment(text_assignment_id,course_id,answer):
            flash("Vastaus oikein!")
            return redirect("/view_course/" + str(course_id))
        else:
            flash("Vastaus väärin!")
            return redirect("/view_course/" + str(course_id))

