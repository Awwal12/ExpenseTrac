from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
     path('', views.index, name="index"),
     path('add-income', views.add_income, name="add_income"),
     path('edit-income/<int:id>', views.income_edit, name="income_edit"),
     path('income-delete/<int:id>', views.delete_income, name="delete_income"),
     path('search/', views.search_income, name='search_income'),
     path('income_source_summary', views.income_source_summary,
          name="income_source_summary"),
     path('stats', views.stats_view,
          name="stats"),
     path('export_csv', views.export_csv, name="export-csv"),
     path('export_excel', views.export_excel, name="export-excel"),
     path('export_pdf', views.export_pdf, name="export-pdf"),
]