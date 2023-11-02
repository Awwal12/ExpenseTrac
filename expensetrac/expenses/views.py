from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.http import JsonResponse
from expenseapp.models import UserPreference
import datetime
from django.db.models import Q
# Create your views here.


def search_expenses(request):
    query = request.GET.get('q', '')

    # Use Q objects to filter on multiple fields using OR logic
    expenses = Expense.objects.filter(
        Q(description__icontains=query) |
        Q(amount__icontains=query) |
        Q(date__icontains=query)
    )
    return render(request, 'expenses/search_expense.html', {'page_obj': expenses, 'query': query})


@login_required(login_url='expenseapp:my_login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Query UserPreference for currency
    try:
        user_preference = UserPreference.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPreference.DoesNotExist:
        # Handle the case where UserPreference is not found
        currency = 'NGN - NIGERIAN NAIRA'  # Set a default currency or handle it as needed

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'expenses': page_obj,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)


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
            messages.error(request, 'Category is required',
                           extra_tags='expense')
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, 'description is required',
                           extra_tags='expense')
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses:add_expenses')


@login_required(login_url='expenseapp:my_login')
def edit_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses:index')


@login_required(login_url='expenseapp:my_login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses:index')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')
