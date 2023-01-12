from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
from Login.models import AppUser
from .forms import *
from .models import *


# Create your views here.


def userDashboard(request):
    return render(request, 'Manager_App/user_dashboard.html')


def calculateBalance():
    pass


def calculateCredit():
    pass


def calculateDebit():
    pass


def adminDashboard(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'Manager_App/admin_dashboard.html', context)


def createInvoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        statementForm = StatementForm(request.POST)

        if form.is_valid() and statementForm.is_valid():
            invoiceObj = form.save()
            statement = statementForm.save(commit=False)
            statement.invoice = invoiceObj
            statement.debit = invoiceObj.updatedPayableAmount
            statement.save()
            return HttpResponseRedirect(reverse('Manager:adminDashboard'))
        else:
            messages.info(request, 'Something went wrong')
    else:
        form = InvoiceForm(request.POST)

    context = {'form': form}
    return render(request, 'Manager_App/invoice.html', context)


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
        statementForm = StatementForm(request.POST)
        statement = statementForm.save(commit=False)
        statement.invoice = invoice
        statement.debit = initialPayableAmount - paidAmount
        statement.credit = paidAmount
        statement.balance = paidAmount

        statement.save()
        invoice.save()
        return HttpResponseRedirect(reverse('Manager:adminDashboard'))


def statementList(request):
    customers = AppUser.objects.all()
    context = {'customers': customers}
    return render(request, 'Manager_App/statementList.html', context)


def statement(request, customer):
    statements = Statement.objects.filter(invoice__user__user=customer)
    context = {'statements': statements}
    return render(request, 'Manager_App/statement.html', context)
