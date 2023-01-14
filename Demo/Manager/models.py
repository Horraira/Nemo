from django.db import models
from django.contrib.auth.models import User
from Login.models import AppUser
from datetime import timedelta
from django.utils import timezone


def in_seven_days():
    return timezone.now() + timedelta(days=7)


# Create your models here.


class Invoice(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    paymentStatus = models.CharField(max_length=15, blank=True, null=True)
    initialPayableAmount = models.IntegerField(default=0)
    updatedPayableAmount = models.IntegerField(default=0, blank=True, null=True)
    paidAmount = models.IntegerField(default=0, blank=True, null=True)
    dueDate = models.DateTimeField(default=in_seven_days)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.updatedPayableAmount = self.initialPayableAmount
        super().save(*args, **kwargs)


class Statement(models.Model):
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)
    statementStatus = models.CharField(max_length=15, blank=True, null=True)
    debit = models.IntegerField(default=0, blank=True, null=True)
    credit = models.IntegerField(default=0, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    # totalBalance = models.IntegerField(default=0, blank=True, null=True)
    # updateBalance = models.IntegerField(default=0, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
