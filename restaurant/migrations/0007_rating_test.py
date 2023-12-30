# Generated by Django 5.0 on 2023-12-29 12:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0006_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="rating",
            name="test",
            field=models.CharField(
                choices=[
                    ("Audio", [("vinyl", "Vinyl"), ("cd", "CD")]),
                    ("Video", [("vhs", "VHS Tape"), ("dvd", "DVD")]),
                    ("unknown", "Unknown"),
                ],
                default="t",
                max_length=100,
            ),
        ),
    ]
