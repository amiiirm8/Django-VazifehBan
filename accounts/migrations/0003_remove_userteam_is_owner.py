# Generated by Django 4.2.1 on 2023-08-14 16:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_customuser_managers_rename_users_team_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userteam",
            name="is_owner",
        ),
    ]
