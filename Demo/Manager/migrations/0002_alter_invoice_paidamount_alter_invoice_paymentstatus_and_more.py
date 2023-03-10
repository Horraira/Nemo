# Generated by Django 4.1.5 on 2023-01-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='paidAmount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paymentStatus',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='updatedPayableAmount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
