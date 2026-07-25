from flask import Flask, render_template, request, jsonify
import boto3
import json
from botocore.exceptions import ClientError
from sagemaker import Session
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

app = Flask(__name__, template_folder='templates')


# 🔐 Fetch AWS credentials from Secrets Manager
def get_aws_secrets():
    secret_name = "myattritionappsecret"      # Change to your Secrets Manager secret
    region_name = "ap-south-1"

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret

    except ClientError as e:
        print("Error fetching AWS Secret:", e)
        raise e


# Prediction using SageMaker Endpoint
def predict_attrition(
    predictor,
    age,
    daily_rate,
    distance_from_home,
    employee_number,
    monthly_income,
    monthly_rate,
    total_working_years,
    years_at_company,
    years_in_current_role,
    years_with_curr_manager,
    jobrole_sales_representative,
    overtime_yes
):

    predictor.serializer = JSONSerializer()
    predictor.deserializer = JSONDeserializer()

    input_data = {
        "Age": [age],
        "DailyRate": [daily_rate],
        "DistanceFromHome": [distance_from_home],
        "EmployeeNumber": [employee_number],
        "MonthlyIncome": [monthly_income],
        "MonthlyRate": [monthly_rate],
        "TotalWorkingYears": [total_working_years],
        "YearsAtCompany": [years_at_company],
        "YearsInCurrentRole": [years_in_current_role],
        "YearsWithCurrManager": [years_with_curr_manager],
        "JobRole_Sales Representative": [jobrole_sales_representative],
        "OverTime_Yes": [overtime_yes]
    }

    prediction = predictor.predict(input_data)

    return prediction


@app.route("/")
def index():
    return render_template("input.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:

        age = float(request.form["age"])
        daily_rate = float(request.form["daily_rate"])
        distance_from_home = float(request.form["distance_from_home"])
        employee_number = float(request.form["employee_number"])
        monthly_income = float(request.form["monthly_income"])
        monthly_rate = float(request.form["monthly_rate"])
        total_working_years = float(request.form["total_working_years"])
        years_at_company = float(request.form["years_at_company"])
        years_in_current_role = float(request.form["years_in_current_role"])
        years_with_curr_manager = float(request.form["years_with_curr_manager"])

        jobrole_sales_representative = float(
            request.form["jobrole_sales_representative"]
        )

        overtime_yes = float(
            request.form["overtime_yes"]
        )

        # Get AWS credentials from Secrets Manager
        aws_creds = get_aws_secrets()

        aws_access_key_id = aws_creds["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = aws_creds["AWS_SECRET_ACCESS_KEY"]

        region_name = "ap-south-1"

        endpoint_name = "attrition-paul-endpoint"

        # Create boto3 session
        boto_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        # Create SageMaker Predictor
        sagemaker_session = Session(boto_session=boto_session)

        predictor = Predictor(
            endpoint_name=endpoint_name,
            sagemaker_session=sagemaker_session
        )

        result = predict_attrition(
            predictor,
            age,
            daily_rate,
            distance_from_home,
            employee_number,
            monthly_income,
            monthly_rate,
            total_working_years,
            years_at_company,
            years_in_current_role,
            years_with_curr_manager,
            jobrole_sales_representative,
            overtime_yes
        )

        return render_template("output.html", result=result)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)