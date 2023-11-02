from django.urls import path

from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('add_expenses/', views.add_expenses, name = 'add_expenses'),
    path('edit_expenses/<int:id>', views.edit_expenses, name = 'edit_expenses'),
    path('delete_expenses/<int:id>', views.delete_expense, name = 'delete_expense'),
    path('search/', views.search_expenses, name='search_expenses'),
    path('expense_category_summary', views.expense_category_summary,
        name="expense_category_summary"),
    path('stats', views.stats_view,
        name="stats")
]
