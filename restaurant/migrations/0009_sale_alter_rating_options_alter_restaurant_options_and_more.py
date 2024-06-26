# Generated by Django 5.0 on 2023-12-29 14:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0008_remove_rating_test_rating_restaurant_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterModelOptions(
            name="rating",
            options={"ordering": ["updated_at"]},
        ),
        migrations.AlterModelOptions(
            name="restaurant",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelTableComment(
            name="rating",
            table_comment="This table stores users' ratings for restaurants",
        ),
        migrations.AddField(
            model_name="rating",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="rating",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="restaurant",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="date_opened",
            field=models.DateField(
                db_comment="Date and time when the restaurant was opened"
            ),
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="name",
            field=models.CharField(
                db_column="Name", db_index=True, max_length=100, unique=True
            ),
        ),
        migrations.AddConstraint(
            model_name="rating",
            constraint=models.CheckConstraint(
                check=models.Q(("rating__lte", 5)), name="rating_lte_5"
            ),
        ),
        migrations.AlterModelTable(
            name="restaurant",
            table="restaurants",
        ),
        migrations.AddField(
            model_name="sale",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="restaurant.restaurant"
            ),
        ),
    ]
