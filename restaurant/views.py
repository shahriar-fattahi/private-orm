from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone

from .models import Rating, Restaurant, Sale


def index(request):
    # rates = Rating.objects.only("restaurant__name", "rating").select_related(
    #     "restaurant"
    # )
    month_ago = timezone.now() - timezone.timedelta(days=30)
    monthly_sales = Prefetch(
        lookup="sales",
        queryset=Sale.objects.filter(created_at__gte=month_ago),
    )
    restaurants = Restaurant.objects.prefetch_related(
        "ratings",
        # "sales",
        monthly_sales,
    ).filter(ratings__rating=4)
    context = {
        "restaurants": restaurants,
        # "rates": rates,
    }
    return render(request, "restaurant/index.html", context)
