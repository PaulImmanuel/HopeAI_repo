from django.db import models

class EmployeeModel(models.Model):

    Age = models.IntegerField()
    DailyRate = models.FloatField()
    DistanceFromHome = models.FloatField()
    EmployeeNumber = models.IntegerField()
    MonthlyIncome = models.FloatField()
    MonthlyRate = models.FloatField()
    TotalWorkingYears = models.FloatField()
    YearsAtCompany = models.FloatField()
    YearsInCurrentRole = models.FloatField()
    YearsWithCurrManager = models.FloatField()
    JobRole_Sales_Representative = models.BooleanField()
    OverTime_Yes = models.BooleanField()