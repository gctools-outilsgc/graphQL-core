# Generated by Django 2.0.3 on 2018-03-07 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GCprofile', '0002_auto_20180307_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgtier',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Org_Tiers', to='GCprofile.Department'),
        ),
        migrations.AlterField(
            model_name='orgtier',
            name='ownerID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Owner_of_Org_Tiers', to='GCprofile.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Employees', to='GCprofile.Profile'),
        ),
    ]