# Generated by Django 4.2.1 on 2023-08-14 16:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_remove_userteam_is_owner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="is_staff_override",
        ),
    ]