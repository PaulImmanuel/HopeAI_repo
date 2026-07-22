import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def append_to_file(filename, *args):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "a") as f:
        for value in args:
            f.write(str(value) + "\n")


def train_model():

    log_file = "/opt/ml/output/public/output.txt"

    input_path = os.path.join(
        "/opt/ml/input/data/train",
        "HR-Employee-Attrition.csv"
    )

    if not os.path.exists(input_path):
        print(f"Dataset not found: {input_path}")
        return

    df = pd.read_csv(input_path)

    # Target column
    y = df["Attrition"]

    # Features
# ---------- Feature Engineering ----------

    # Create encoded columns first
    df = pd.get_dummies(df, drop_first=True)

    # Target
    y = df["Attrition_Yes"]

    # Selected features (same as Flask project)
    selected_features = [
        "Age",
        "DailyRate",
        "DistanceFromHome",
        "EmployeeNumber",
        "MonthlyIncome",
        "MonthlyRate",
        "TotalWorkingYears",
        "YearsAtCompany",
        "YearsInCurrentRole",
        "YearsWithCurrManager",
        "JobRole_Sales Representative",
        "OverTime_Yes"
    ]
    
    X = df[selected_features]

    append_to_file(log_file, "Columns after encoding:")
    append_to_file(log_file, X.columns)

    X = X.fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, pred)

    print("Accuracy:", accuracy)

    append_to_file(
        log_file,
        "Accuracy:",
        accuracy
    )

    joblib.dump(
        model,
        os.path.join(
            "/opt/ml/model",
            "model.joblib"
        )
    )


if __name__ == "__main__":
    train_model()