from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'expenses/index.html')


@login_required(login_url='expenseapp:my_login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request, 'Amount is required', extra_tags='expense')
            return render(request, 'expenses/add_expenses.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST.get('category')

        if not date:
            messages.error(request, 'Date is required', extra_tags='expense')
            return render(request, 'expenses/add_expenses.html', context)

        if not category:
            messages.error(request, 'Category is required', extra_tags='expense')
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, 'description is required', extra_tags='expense')
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses:add_expenses')

