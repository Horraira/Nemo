from .models import *
from django import forms
from django.forms import ModelForm, NumberInput, Select


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['user', 'initialPayableAmount']
        widgets = {
            'user': Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
            'initialPayableAmount': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Payable amount'
            })
        }


class StatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = '__all__'
