from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="index"),
    path('add-income', views.add_income, name="add_income"),
    path('edit-income/<int:id>', views.income_edit, name="income_edit"),
    path('income-delete/<int:id>', views.delete_income, name="delete_income"),
    path('search-income', csrf_exempt(views.search_income),
         name="search_income")
]