from flask import Flask, render_template, request, redirect
from models import db, Employee, SalaryStructure
from models import Product , Attendance, Payroll
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from flask import send_file
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch




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

        new_employee = Employee(

            employee_code=request.form["employee_code"],

            first_name=request.form["first_name"],

            last_name=request.form["last_name"],

            father_name=request.form["father_name"],

            gender=request.form["gender"],

            dob=datetime.strptime(
                request.form["dob"],
                "%Y-%m-%d"
            ).date() if request.form["dob"] else None,

            phone=request.form["phone"],

            email=request.form["email"],

            address=request.form["address"],

            city=request.form["city"],

            state=request.form["state"],

            pincode=request.form["pincode"],

            aadhaar=request.form["aadhaar"],

            pan=request.form["pan"],

            bank_name=request.form["bank_name"],

            account_number=request.form["account_number"],

            ifsc=request.form["ifsc"],

            department=request.form["department"],

            designation=request.form["designation"],

            joining_date=datetime.strptime(
                request.form["joining_date"],
                "%Y-%m-%d"
            ).date() if request.form["joining_date"] else None,

            status=request.form["status"]
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


@app.route("/employee/<int:id>")
def employee_profile(id):

    employee = Employee.query.get_or_404(id)

    return render_template(
        "employee_profile.html",
        employee=employee
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

@app.route("/salary")
def salary():

    salaries = SalaryStructure.query.all()

    return render_template(
        "salary.html",
        salaries=salaries
    )

@app.route("/add_salary", methods=["GET", "POST"])
def add_salary():

    employees = Employee.query.all()

    if request.method == "POST":

        salary = SalaryStructure(

            employee_id=request.form["employee_id"],

            basic=request.form["basic"],

            hra=request.form["hra"],

            fuel_allowance=request.form["fuel_allowance"],

            medical_allowance=request.form["medical_allowance"],

            travel_allowance=request.form["travel_allowance"],

            overtime=request.form["overtime"],

            bonus=request.form["bonus"],

            other_allowance=request.form["other_allowance"]

        )

        db.session.add(salary)

        db.session.commit()

        return redirect("/salary")

    return render_template(
        "add_salary.html",
        employees=employees
    )

@app.route("/payroll")
def payroll():

    payrolls = Payroll.query.all()

    return render_template(
        "payroll.html",
        payrolls=payrolls
    )


@app.route("/generate_payroll", methods=["GET", "POST"])
def generate_payroll():

    employees = Employee.query.all()

    if request.method == "POST":
        employee_id = request.form["employee_id"]
        month = request.form["month"]
        year = int(request.form["year"])
        advance = float(request.form["advance"])
        pf = float(request.form["pf"])
        esi = float(request.form["esi"])
        professional_tax = float(request.form["professional_tax"])
        other_deduction = float(request.form["other_deduction"])
        salary = SalaryStructure.query.filter_by(
            employee_id=employee_id
        ).first()

        if salary is None:

            return "Salary Structure not found for this employee."

        gross_salary = (
            salary.basic
            + salary.hra
            + salary.fuel_allowance
            + salary.medical_allowance
            + salary.travel_allowance
            + salary.overtime
            + salary.bonus
            + salary.other_allowance
        )

        total_deduction = (
            advance
            + pf
            + esi
            + professional_tax
            + other_deduction
        )

        net_salary = gross_salary - total_deduction

        payroll = Payroll(
            employee_id=employee_id,
            month=month,
            year=year,
            present_days=30,
            leave_days=0,
            gross_salary=gross_salary,
            advance=advance,
            pf=pf,
            esi=esi,
            professional_tax=professional_tax,
            other_deduction=other_deduction,
            total_deduction=total_deduction,
            net_salary=net_salary,
            payment_status="Pending"
        )

        db.session.add(payroll)
        db.session.commit()
        return redirect("/payroll")

    return render_template(
        "generate_payroll.html",
        employees=employees
    )

@app.route("/payslip/<int:id>")
def payslip(id):

    payroll = Payroll.query.get_or_404(id)

    salary = SalaryStructure.query.filter_by(
        employee_id=payroll.employee_id
    ).first()

    return render_template(
        "payslip.html",
        payroll=payroll,
        salary=salary
    )


@app.route("/download_payslip/<int:id>")
def download_payslip(id):

    payroll = Payroll.query.get_or_404(id)

    salary = SalaryStructure.query.filter_by(
        employee_id=payroll.employee_id
    ).first()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    # ---------------------------
    # Title
    # ---------------------------

    elements.append(
        Paragraph(
            "<b><font size='20'>WORKSPHERE ERP</font></b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "<b>Employee Payslip</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    # ---------------------------
    # Employee Details
    # ---------------------------

    employee_table = Table([

        ["Employee",
         payroll.employee.first_name + " " + payroll.employee.last_name],

        ["Employee Code",
         payroll.employee.employee_code],

        ["Department",
         payroll.employee.department],

        ["Designation",
         payroll.employee.designation],

        ["Month",
         payroll.month],

        ["Year",
         str(payroll.year)]

    ], colWidths=[2.3*inch, 4*inch])

    employee_table.setStyle(TableStyle([

        ('GRID',(0,0),(-1,-1),1,colors.grey),

        ('BACKGROUND',(0,0),(0,-1),colors.HexColor("#EAF4FF")),

        ('FONTNAME',(0,0),(-1,-1),"Helvetica"),

        ('BOTTOMPADDING',(0,0),(-1,-1),8)

    ]))

    elements.append(employee_table)

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    # ---------------------------
    # Earnings
    # ---------------------------

    gross = payroll.gross_salary

    earnings = [

        ["Earnings","Amount"],

        ["Basic Salary", salary.basic],

        ["HRA", salary.hra],

        ["Fuel Allowance", salary.fuel_allowance],

        ["Medical Allowance", salary.medical_allowance],

        ["Travel Allowance", salary.travel_allowance],

        ["Overtime", salary.overtime],

        ["Bonus", salary.bonus],

        ["Other Allowance", salary.other_allowance],

        ["Gross Salary", gross]

    ]

    earnings_table = Table(earnings)

    earnings_table.setStyle(TableStyle([

        ('GRID',(0,0),(-1,-1),1,colors.black),

        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#198754")),

        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('BACKGROUND',(0,-1),(-1,-1),colors.HexColor("#D1F7D6")),

        ('FONTNAME',(0,0),(-1,-1),"Helvetica-Bold")

    ]))

    elements.append(earnings_table)

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    # ---------------------------
    # Deductions
    # ---------------------------

    deductions = [

        ["Deductions","Amount"],

        ["Advance", payroll.advance],

        ["PF", payroll.pf],

        ["ESI", payroll.esi],

        ["Professional Tax", payroll.professional_tax],

        ["Other Deduction", payroll.other_deduction],

        ["Total Deduction", payroll.total_deduction],

        ["Net Salary", payroll.net_salary]

    ]

    deduction_table = Table(deductions)

    deduction_table.setStyle(TableStyle([

        ('GRID',(0,0),(-1,-1),1,colors.black),

        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#DC3545")),

        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('BACKGROUND',(0,-1),(-1,-1),colors.HexColor("#FFF3CD")),

        ('FONTNAME',(0,0),(-1,-1),"Helvetica-Bold")

    ]))

    elements.append(deduction_table)

    doc.build(elements)

    buffer.seek(0)

    filename = f"Payslip_{payroll.employee.employee_code}_{payroll.month}_{payroll.year}.pdf"

    return send_file(

        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"

    )


if __name__ == "__main__":
    app.run(debug=True)











