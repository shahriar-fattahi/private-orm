from django.contrib import admin

from .models import Rating, Restaurant, Sale


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "restaurant", "rating")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "income", "created_at")
