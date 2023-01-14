from django.urls import path
from . import views

app_name = 'Manager'

urlpatterns = [
    path('user/', views.userDashboard, name="userDashboard"),
    path('admin/', views.adminDashboard, name="adminDashboard"),
    path('createInvoice/', views.createInvoice, name="createInvoice"),
    path('pay/<invoiceID>', views.payInvoice, name='payInvoice'),
    path('statementList/', views.statementList, name="statementList"),
    path('statement/<customer>', views.statement, name="statement"),
    path('deleteInvoice/<invoiceId>', views.deleteInvoice, name="deleteInvoice"),
]
