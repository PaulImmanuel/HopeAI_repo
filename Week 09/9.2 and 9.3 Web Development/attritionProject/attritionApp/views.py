from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse_lazy

from .forms import EmployeeForm

import pickle
import pandas as pd
import numpy as np

np.random.seed(123)


class dataUploadView(View):

    form_class = EmployeeForm
    success_url = reverse_lazy('success')
    template_name = 'create.html'
    failure_url = reverse_lazy('fail')

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        return render(
            request,
            self.template_name,
            {'form': form}
        )

    def post(self, request, *args, **kwargs):

        form = self.form_class(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            age = request.POST.get('Age')
            daily_rate = request.POST.get('DailyRate')
            distance = request.POST.get('DistanceFromHome')
            employee_number = request.POST.get('EmployeeNumber')
            income = request.POST.get('MonthlyIncome')
            monthly_rate = request.POST.get('MonthlyRate')
            total_years = request.POST.get('TotalWorkingYears')
            company_years = request.POST.get('YearsAtCompany')
            role_years = request.POST.get('YearsInCurrentRole')
            manager_years = request.POST.get('YearsWithCurrManager')

            sales_rep = request.POST.get(
                'JobRole_Sales_Representative'
            )

            overtime = request.POST.get(
                'OverTime_Yes'
            )

            sales_rep = 1 if sales_rep else 0
            overtime = 1 if overtime else 0

            input_df = pd.DataFrame([{
                'Age': float(age),
                'DailyRate': float(daily_rate),
                'DistanceFromHome': float(distance),
                'EmployeeNumber': float(employee_number),
                'MonthlyIncome': float(income),
                'MonthlyRate': float(monthly_rate),
                'TotalWorkingYears': float(total_years),
                'YearsAtCompany': float(company_years),
                'YearsInCurrentRole': float(role_years),
                'YearsWithCurrManager': float(manager_years),
                'JobRole_Sales Representative': sales_rep,
                'OverTime_Yes': overtime
            }])

            filename = 'AttritionModel.sav'

            classifier = pickle.load(
                open(filename, 'rb')
            )

            out = classifier.predict(input_df)

            return render(
                request,
                "succ_msg.html",
                {
                    "age": age,
                    "daily_rate": daily_rate,
                    "distance": distance,
                    "employee_number": employee_number,
                    "income": income,
                    "monthly_rate": monthly_rate,
                    "total_years": total_years,
                    "company_years": company_years,
                    "role_years": role_years,
                    "manager_years": manager_years,
                    "sales_rep": sales_rep,
                    "overtime": overtime,
                    "out": out[0]
                }
            )

        else:

            return redirect(self.failure_url)