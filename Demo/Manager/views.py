from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
from Login.models import AppUser
from .forms import *
from .models import *


# Create your views here.


def userDashboard(request):
    return render(request, 'Manager_App/user_dashboard.html')


def adminDashboard(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'Manager_App/admin_dashboard.html', context)


def createInvoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        statementForm = StatementForm(request.POST)

        if form.is_valid() and statementForm.is_valid():
            user = form.cleaned_data['user']
            if Invoice.objects.filter(user=user).exists():
                preBalance = Statement.objects.filter(invoice__user=user).order_by(
                    'date_created').last().balance
                invoiceObj = form.save()
                statement = statementForm.save(commit=False)
                statement.invoice = invoiceObj
                statement.debit = statement.balance = invoiceObj.updatedPayableAmount + preBalance
                statement.save()
            else:
                invoiceObj = form.save()
                statement = statementForm.save(commit=False)
                statement.invoice = invoiceObj
                statement.debit = statement.balance = invoiceObj.updatedPayableAmount
                statement.save()
            return HttpResponseRedirect(reverse('Manager:adminDashboard'))
        else:
            messages.info(request, 'Something went wrong')
    else:
        form = InvoiceForm(request.POST)

    context = {'form': form}
    return render(request, 'Manager_App/invoice.html', context)


def deleteInvoice(request, invoiceId):
    invoice = Invoice.objects.get(id=invoiceId)
    statements = Statement.objects.filter(invoice__user=invoice.user).order_by('date_created')
    preBalance = 0
    for statement in statements:
        if int(statement.invoice.id) == int(invoiceId):
            dateCreated = statement.date_created
            invoice.delete()
            break
        else:
            preBalance = statement.balance

    statements = Statement.objects.filter(invoice__user=invoice.user, date_created__gt=dateCreated).order_by(
        'date_created')
    for statement in statements:
        preBalance = statement.balance = preBalance + statement.debit - statement.credit
        statement.save()

    return HttpResponseRedirect(reverse('Manager:adminDashboard'))


def payInvoice(request, invoiceID):
    if request.method == 'POST':
        invoice = Invoice.objects.get(pk=invoiceID)

        initialPayableAmount = invoice.initialPayableAmount
        initialPaidAmount = invoice.paidAmount
        paidAmount = int(request.POST['paidAmount']) + initialPaidAmount

        if paidAmount >= initialPayableAmount:
            invoice.paymentStatus = 'PAID'
        elif paidAmount < initialPayableAmount:
            invoice.paymentStatus = 'Partial PAID'

        invoice.paidAmount = paidAmount
        invoice.updatedPayableAmount = initialPayableAmount - paidAmount

        # calculate statement
        preUpdateBalance = Statement.objects.filter(invoice__user=invoice.user).order_by(
            'date_created').last().balance
        statementForm = StatementForm(request.POST)
        statement = statementForm.save(commit=False)
        statement.invoice = invoice
        statement.debit = 0
        statement.credit = paidAmount
        statement.balance = preUpdateBalance - int(request.POST['paidAmount'])

        statement.save()
        invoice.save()
        return HttpResponseRedirect(reverse('Manager:adminDashboard'))


def statementList(request):
    customers = AppUser.objects.all()
    context = {'customers': customers}
    return render(request, 'Manager_App/statementList.html', context)


def statement(request, customer):
    statements = Statement.objects.filter(invoice__user__user=customer).order_by('date_created')
    totalBalance = 0
    for statement in statements:
        totalBalance = + statement.balance
    if not statements:
        messages.info(request, 'No statement has created.')
        return HttpResponseRedirect(reverse('Manager:statementList'))
    context = {'statements': statements, 'totalBalance': totalBalance}
    return render(request, 'Manager_App/statement.html', context)
