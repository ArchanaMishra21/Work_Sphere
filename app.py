from flask import Flask, render_template, request, redirect
from models import db, Employee

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345@localhost/worksphere"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name = request.form["employee_name"]
        department = request.form["department"]
        salary = request.form["salary"]
        email = request.form["email"]

        new_employee = Employee(
            name=name,
            department=department,
            salary=salary,
            email=email
        )

        db.session.add(new_employee)
        db.session.commit()

        return redirect("/employees")

    return render_template("add_employee.html")


@app.route("/employees")
def employees():

    employees = Employee.query.all()

    return render_template(
        "employee.html",
        employees=employees
    )

@app.route("/delete_employee/<int:id>")
def delete_employee(id):

    employee = Employee.query.get(id)

    if employee:

        db.session.delete(employee)

        db.session.commit()

    return redirect("/employees")


@app.route("/edit_employee/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    employee = Employee.query.get(id)

    if request.method == "POST":

        employee.name = request.form["employee_name"]
        employee.department = request.form["department"]
        employee.salary = request.form["salary"]
        employee.email = request.form["email"]

        db.session.commit()

        return redirect("/employees")

    return render_template(
        "edit_employee.html",
        employee=employee
)


app.run(debug=True)











