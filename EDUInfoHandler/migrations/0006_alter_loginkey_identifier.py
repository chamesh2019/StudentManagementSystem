# Generated by Django 4.1.6 on 2023-05-11 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EDUInfoHandler', '0005_remove_examinfo_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginkey',
            name='identifier',
            field=models.CharField(max_length=25),
        ),
    ]
