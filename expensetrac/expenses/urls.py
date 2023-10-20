from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_expenses/', views.add_expenses, name = 'add_expenses'),
    path('edit_expenses/<int:id>', views.edit_expenses, name = 'edit_expenses')
]
