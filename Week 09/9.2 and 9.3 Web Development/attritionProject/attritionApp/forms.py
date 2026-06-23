from django import forms
from .models import EmployeeModel

class EmployeeForm(forms.ModelForm):

    class Meta:

        model = EmployeeModel
        fields = [
            'Age',
            'DailyRate',
            'DistanceFromHome',
            'EmployeeNumber',
            'MonthlyIncome',
            'MonthlyRate',
            'TotalWorkingYears',
            'YearsAtCompany',
            'YearsInCurrentRole',
            'YearsWithCurrManager',
            'JobRole_Sales_Representative',
            'OverTime_Yes'
        ]