# Generated by Django 4.2.1 on 2024-12-05 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prompt_studio_output_manager_v2", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="promptstudiooutputmanager",
            name="highlight_data",
            field=models.JSONField(
                blank=True, db_comment="Field to store highlight data", null=True
            ),
        ),
    ]