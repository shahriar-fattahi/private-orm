from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models


class TimeStamp(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Restaurant(models.Model):
    class Meta:
        db_table = "restaurants"
        ordering = [
            "name",
        ]

    class RestaurantType(models.TextChoices):
        PERSIAN = "PR", "Persian"
        ITALIAN = "IT", "Italian"
        CHINESE = "CH", "Chinese"

    name = models.CharField(
        max_length=100,
        unique=True,
        db_column="Name",
        db_index=True,
    )
    website = models.URLField(default="")
    date_opened = models.DateField(
        db_comment="Date when the restaurant was opened",
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    restaurant_type = models.CharField(
        max_length=2,
        choices=RestaurantType.choices,
        default=RestaurantType.PERSIAN,
    )

    def __str__(self) -> str:
        return self.name


class Rating(TimeStamp):
    class Meta:
        db_table_comment = "This table stores user ratings for restaurants"
        ordering = [
            "updated_at",
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(rating__lte=5), name="rating_lte_5"),
        ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[validators.MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user} >> {self.restaurant} >> {self.rating}"


class Sale(TimeStamp):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
    )
    income = models.DecimalField(max_digits=8, decimal_places=2)
