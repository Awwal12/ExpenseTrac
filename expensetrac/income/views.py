from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.http import JsonResponse
from expenseapp.models import UserPreference
import datetime

# Create your views here.


@login_required(login_url='expenseapp:my_login')
def index(request):
    categories = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='expenseapp:my_login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required', extra_tags='income')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST["income_date"]
        source = request.POST.get('source')

        if not description:
            messages.error(request, 'description is required', extra_tags='income')
            return render(request, 'income/add_income.html', context, )

        Income.objects.create(owner=request.user, amount=amount, date=date,
                                  source=source, description=description)
        messages.success(request, 'Record saved successfully')

        return redirect('income:index')



@login_required(login_url='expenseapp:my_login')
def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required', extra_tags='income')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST.get("income_date")
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required', extra_tags='income')
            return render(request, 'income/edit_income.html', context)
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income:index')



@login_required(login_url='expenseapp:my_login')
def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('income:index')



@login_required(login_url='expenseapp:my_login')
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)