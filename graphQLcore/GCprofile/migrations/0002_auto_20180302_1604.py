# Generated by Django 2.0.2 on 2018-03-02 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GCprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='acronym_en',
            field=models.CharField(default='acro', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='department',
            name='acronym_fr',
            field=models.CharField(default='acro', max_length=10),
            preserve_default=False,
        ),
    ]
