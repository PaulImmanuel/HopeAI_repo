from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model once when the application starts
with open("AttritionModel.sav", "rb") as f:
    classifier = pickle.load(f)


@app.route("/")
def home():
    return render_template("create.html")


@app.route("/predict", methods=["POST"])
def predict():

    age = request.form.get("Age")
    daily_rate = request.form.get("DailyRate")
    distance = request.form.get("DistanceFromHome")
    employee_number = request.form.get("EmployeeNumber")
    income = request.form.get("MonthlyIncome")
    monthly_rate = request.form.get("MonthlyRate")
    total_years = request.form.get("TotalWorkingYears")
    company_years = request.form.get("YearsAtCompany")
    role_years = request.form.get("YearsInCurrentRole")
    manager_years = request.form.get("YearsWithCurrManager")

    sales_rep = int(request.form.get("JobRole_Sales_Representative"))
    overtime = int(request.form.get("OverTime_Yes"))

    input_df = pd.DataFrame([{
        "Age": float(age),
        "DailyRate": float(daily_rate),
        "DistanceFromHome": float(distance),
        "EmployeeNumber": float(employee_number),
        "MonthlyIncome": float(income),
        "MonthlyRate": float(monthly_rate),
        "TotalWorkingYears": float(total_years),
        "YearsAtCompany": float(company_years),
        "YearsInCurrentRole": float(role_years),
        "YearsWithCurrManager": float(manager_years),
        "JobRole_Sales Representative": sales_rep,
        "OverTime_Yes": overtime
    }])

    out = classifier.predict(input_df)

    return render_template(
        "succ_msg.html",
        age=age,
        daily_rate=daily_rate,
        distance=distance,
        employee_number=employee_number,
        income=income,
        monthly_rate=monthly_rate,
        total_years=total_years,
        company_years=company_years,
        role_years=role_years,
        manager_years=manager_years,
        sales_rep=sales_rep,
        overtime=overtime,
        out=out[0]
    )


if __name__ == "__main__":
    app.run(debug=True) 