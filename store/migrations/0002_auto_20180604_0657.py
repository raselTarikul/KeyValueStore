# Generated by Django 2.0.6 on 2018-06-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='last_updated',
            field=models.DateField(null=True),
        ),
    ]
