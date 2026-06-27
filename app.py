from flask import Flask, render_template, request, redirect
from models import db, Employee
from models import Product , Attendance

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345@localhost/worksphere"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():

    employee_count = Employee.query.count()
    product_count = Product.query.count()

    low_stock_products = Product.query.filter(
        Product.quantity <= 10
    ).all()

    low_stock_count = len(low_stock_products)

    return render_template(
        "home.html",
        employee_count=employee_count,
        product_count=product_count,
        low_stock_products=low_stock_products,
        low_stock_count=low_stock_count
    )


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

    search = request.args.get("search", "")

    if search:
        employees = Employee.query.filter(
            Employee.name.contains(search)
        ).all()
    else:
        employees = Employee.query.all()

    return render_template(
        "employee.html",
        employees=employees,
        search=search
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



@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        supplier = request.form["supplier"]

        new_product = Product(
            name=product_name,
            category=category,
            quantity=quantity,
            price=price,
            supplier=supplier
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect("/products")

    return render_template("add_product.html")


@app.route("/products")
def products():

    search = request.args.get("search", "")

    if search:
        products = Product.query.filter(
            Product.name.contains(search)
        ).all()
    else:
        products = Product.query.all()

    return render_template(
        "products.html",
        products=products,
        search=search
    )

@app.route("/delete_product/<int:id>")
def delete_product(id):

    product = Product.query.get(id)

    db.session.delete(product)

    db.session.commit()

    return redirect("/products")


@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    product = Product.query.get(id)

    if request.method == "POST":

        product.name = request.form["product_name"]
        product.category = request.form["category"]
        product.quantity = request.form["quantity"]
        product.price = request.form["price"]
        product.supplier = request.form["supplier"]

        db.session.commit()

        return redirect("/products")

    return render_template(
        "edit_product.html",
        product=product
    )


@app.route("/attendance")
def attendance():

    attendance_records = Attendance.query.all()
    employees = Employee.query.all()

    return render_template(
        "attendance.html",
        attendance_records=attendance_records,
        employees=employees
    )

@app.route("/add_attendance", methods=["GET", "POST"])
def add_attendance():

    employees = Employee.query.all()

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        date = request.form["date"]
        status = request.form["status"]

        new_attendance = Attendance(
            employee_id=employee_id,
            date=date,
            status=status
        )

        db.session.add(new_attendance)
        db.session.commit()

        return redirect("/attendance")

    return render_template(
        "add_attendance.html",
        employees=employees
    )

@app.route("/delete_attendance/<int:id>")
def delete_attendance(id):

    record = Attendance.query.get(id)

    if record:

        db.session.delete(record)
        db.session.commit()

    return redirect("/attendance")

@app.route("/edit_attendance/<int:id>", methods=["GET", "POST"])
def edit_attendance(id):

    record = Attendance.query.get(id)

    employees = Employee.query.all()

    if request.method == "POST":

        record.employee_id = request.form["employee_id"]
        record.date = request.form["date"]
        record.status = request.form["status"]

        db.session.commit()

        return redirect("/attendance")

    return render_template(
        "edit_attendance.html",
        record=record,
        employees=employees
    )


if __name__ == "__main__":
    app.run(debug=True)











