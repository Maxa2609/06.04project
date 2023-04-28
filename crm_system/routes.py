from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from crm_system import app, login_manager
from crm_system.models import student
from crm_system.models.database import session
from crm_system.models.group import Group
from crm_system.models.student import Student
from crm_system.models.user import User


@app.route("/")
@app.route("/group_management", methods=["POST"])
@login_required
def group_management():
    all_data = session.query(Group).all()
    all_data = [i.group_name for i in all_data]

    if request.method == "POST":
        group_name = request.form['gr_name']
        group = Group(group_name=group_name)
        session.add(group)
        session.commit()

        session.close()
        return redirect("group_management")
    return render_template('group_management.html',group_names=all_data)

@app.route("/student_management/<g_name>", methods=["GET","POST"])
@login_required
def group_list(g_name):
    gr_id = session.query(Group).where(Group.group_name == g_name).first().id
    group = session.query(Student).where(Student.group == gr_id).all()
    if request.method == "POST":
        surname = request.form["surname"]
        name = request.form["name"]
        age = request.form["age"]
        address = request.form["address"]
        student = Student(surname=surname, name=name, age=age, address=address, group=gr_id)
        session.add(student)
        session.commit()
        session.close()
        return redirect(f"/student_management/{g_name}")
    return render_template("student_management.html", group=group)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = session.query(User).where(User.username == username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again')
            return redirect(url_for("login"))
        login_user(user,remember=remember)
        return redirect(url_for("group_management"))
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')

        user = session.query(User).where(User.username == username).first()

        if user:
            flash('This user already exists')
            return redirect(url_for('signup'))

        new_user = User (username=username, password=generate_password_hash(password, method='sha256'))
        session.add(new_user)
        session.commit()
        session.close()

        return redirect("login")
    return render_template("signup.html")

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('group_management'))

@app.route("/group_management")
def user_group():
    all_data = session.query(Group).all()
    all_data = [i.group_name for i in all_data]
    return render_template("group_management.html", group_names=all_data)