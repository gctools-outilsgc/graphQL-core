# Generated by Django 2.0.2 on 2018-03-01 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GCprofile', '0002_auto_20180228_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=150)),
                ('name_fr', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='orgtier',
            name='ownerID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.ProtectedError, to='GCprofile.Profile'),
        ),
        migrations.AddField(
            model_name='orgtier',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GCprofile.Department'),
        ),
    ]
