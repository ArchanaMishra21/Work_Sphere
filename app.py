from flask import Flask, render_template, request

app = Flask(__name__)

employees = ["archana","rahul", "priya"]

@app.route("/", methods=["GET","POST"])
def home():
    
    if request.method=="POST":
        new_employee= request.form["employee_name"]
        employees.append(new_employee)
    return render_template("index.html", employees=employees)

app.run(debug=True)

