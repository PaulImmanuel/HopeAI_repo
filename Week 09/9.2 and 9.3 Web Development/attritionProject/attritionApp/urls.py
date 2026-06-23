from django.urls import path
from attritionApp import views

app_name = 'attritionApp'

urlpatterns = [
    path('', views.dataUploadView.as_view(), name='attrition'),
]