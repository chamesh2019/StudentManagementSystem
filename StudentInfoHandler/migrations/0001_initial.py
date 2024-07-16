# Generated by Django 4.1.7 on 2023-04-27 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StudentInfo",
            fields=[
                (
                    "index_number",
                    models.CharField(
                        max_length=8, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("full_name", models.CharField(max_length=255)),
                ("name_with_initials", models.CharField(max_length=255)),
                ("date_of_birth", models.CharField(max_length=20)),
                ("gender", models.CharField(max_length=1)),
                ("enrolled_date", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("special_notes", models.TextField()),
                ("buckets", models.CharField(default="", max_length=20)),
                ("RFID_key", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ParentInfo",
            fields=[
                (
                    "student_index_number",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="StudentInfoHandler.studentinfo",
                    ),
                ),
                ("mother_name", models.CharField(max_length=255)),
                ("mother_nic", models.CharField(max_length=255)),
                ("mother_dob", models.CharField(max_length=255)),
                ("mother_job", models.CharField(max_length=255)),
                ("mother_status", models.CharField(max_length=10)),
                ("mother_special_notes", models.TextField()),
                ("father_name", models.CharField(max_length=255)),
                ("father_job", models.CharField(max_length=255)),
                ("father_dob", models.CharField(max_length=255)),
                ("father_nic", models.CharField(max_length=255)),
                ("father_status", models.CharField(max_length=10)),
                ("father_special_notes", models.TextField()),
            ],
        ),
    ]