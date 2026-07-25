import boto3
from sagemaker import Session
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

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

# ----------- YOUR AWS CREDENTIALS ----------
aws_access_key_id = " "
aws_secret_access_key = " "
region_name = "ap-south-1"
endpoint_name = "attrition-paul-endpoint2"
# -------------------------------------------

# Create a boto3 session using credentials
boto_session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Create a SageMaker session from the boto3 session
sagemaker_session = Session(boto_session=boto_session)

# Create Predictor object
predictor = Predictor(
    endpoint_name=endpoint_name,
    sagemaker_session=sagemaker_session
)

# Predict
result = predict_attrition(
    predictor,
    age=35,
    daily_rate=1102,
    distance_from_home=5,
    employee_number=1001,
    monthly_income=6000,
    monthly_rate=15000,
    total_working_years=10,
    years_at_company=5,
    years_in_current_role=3,
    years_with_curr_manager=2,
    jobrole_sales_representative=0,
    overtime_yes=1
)

print("✅ Predicted Attrition:", result)