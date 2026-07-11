from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Employee(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    employee_code = db.Column(db.String(20), unique=True, nullable=False)

    photo = db.Column(db.String(200), default="default.png")

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    father_name = db.Column(db.String(100))

    gender = db.Column(db.String(20))

    dob = db.Column(db.Date)

    phone = db.Column(db.String(15), unique=True)

    email = db.Column(db.String(100), unique=True, nullable=False)

    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))

    aadhaar = db.Column(db.String(12), unique=True)

    pan = db.Column(db.String(10), unique=True)

    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(30))
    ifsc = db.Column(db.String(20))

    department = db.Column(db.String(100))
    designation = db.Column(db.String(100))

    joining_date = db.Column(db.Date)

    status = db.Column(db.String(30), default="Active")




class Attendance(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employee.id"),
        nullable=False
    )

    date = db.Column(db.Date)

    status = db.Column(db.String(20))

    employee = db.relationship("Employee")




class SalaryStructure(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employee.id"),
        nullable=False
    )

    basic = db.Column(db.Float, default=0)

    hra = db.Column(db.Float, default=0)

    fuel_allowance = db.Column(db.Float, default=0)

    medical_allowance = db.Column(db.Float, default=0)

    travel_allowance = db.Column(db.Float, default=0)

    overtime = db.Column(db.Float, default=0)

    bonus = db.Column(db.Float, default=0)

    other_allowance = db.Column(db.Float, default=0)

    employee = db.relationship("Employee")




class Payroll(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employee.id"),
        nullable=False
    )

    month = db.Column(db.String(20))

    year = db.Column(db.Integer)

    present_days = db.Column(db.Integer, default=0)

    leave_days = db.Column(db.Integer, default=0)

    gross_salary = db.Column(db.Float, default=0)

    advance = db.Column(db.Float, default=0)

    pf = db.Column(db.Float, default=0)

    esi = db.Column(db.Float, default=0)

    professional_tax = db.Column(db.Float, default=0)

    other_deduction = db.Column(db.Float, default=0)

    total_deduction = db.Column(db.Float, default=0)

    net_salary = db.Column(db.Float, default=0)

    payment_status = db.Column(
        db.String(20),
        default="Pending"
    )

    employee = db.relationship("Employee")




class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    item_code = db.Column(db.String(20), unique=True)

    name = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(100))

    brand = db.Column(db.String(100))

    unit = db.Column(db.String(20))

    quantity = db.Column(db.Integer)

    minimum_stock = db.Column(db.Integer)

    purchase_price = db.Column(db.Float)

    selling_price = db.Column(db.Float)

    gst = db.Column(db.Float)

    supplier = db.Column(db.String(100))