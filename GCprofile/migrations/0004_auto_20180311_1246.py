# Generated by Django 2.0.3 on 2018-03-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GCprofile', '0003_auto_20180307_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AlterField(
            model_name='profile',
            name='gcID',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
