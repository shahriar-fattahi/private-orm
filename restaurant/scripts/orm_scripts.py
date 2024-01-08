from django.contrib.auth import get_user_model
from django.db import connection

from ..models import Rating, Restaurant

User = get_user_model()


def run():
    restaurants = Restaurant.objects.all()
    print(connection.queries)
    """
    >>> []: because Restaurant.objects.all(), `never actualy evaluated.
    That is because Django query sets are lazy evaluated.
    so, when you never use the restaurant variable, the query never runs.
    """
    print(restaurants)
    print(connection.queries)
    """
    >>> [{'sql':'SELECT
                    "restaurants"."id",
                    "restaurants"."Name",
                    "restaurants"."website",
                    "restaurants"."date_opened",
                    "restaurants"."latitude",
                    "restaurants"."longitude",
                    "restaurants"."restaurant_type"
                FROM "restaurants"
                ORDER BY "restaurants"."Name" ASC LIMIT 21'
        , 'time': '0.000'}]
    In this case, you can see a query that is run to fetch data from the database.
    """

    obj1 = Restaurant.objects.first()
    obj2 = Restaurant.objects.all()[0]
    """
    The query of obj1 equals the query of obj2.
    """

    # rating = obj1.rating_set.all()
    """
    If you don't specify a name for backward related (related_name),
    Django will automatically set [fieldname_set] for that.
    """

    user = User.objects.first()
    restaurant = restaurants.first()

    rating, created = Rating.objects.get_or_create(
        restaurant=restaurant,
        user=user,
        rating=4,
    )
    print(rating, created)

    """
    Update only one field
    """
    # restaurant.name = "TANJE"
    # restaurant.website = "PORNHUB.COM"
    # restaurant.save(update_fields=["name"])

    """
    if you want to ordering query by insensetiv case:
    """
    from django.db.models.functions import Lower

    restaurant = Restaurant.objects.all().order_by(Lower("name"))

    """
    get earliest and latest data
    """
    restaurant = Restaurant.objects.earliest("date_opened")
    restaurant = Restaurant.objects.latest("date_opened")

    """
    Get 3 last restaurants in dictionary include just name(Upper case)
    """
    from django.db.models.functions import Upper

    restaurants = Restaurant.objects.values(upper_name=Upper("name"))[:3]
    print(restaurants)

    """
    aggregation
    """
    from django.db.models import Avg, Count, Sum

    count = Restaurant.objects.aggregate(number_of_ids=Count("id"))
    count_sum = Restaurant.objects.aggregate(
        number_of_ids=Count("id"),
        sum_of_latitude=Sum(
            "latitude",
        ),
    )
    ave = Rating.objects.filter(restaurant__name__istartswith="t").aggregate(
        Avg("rating")
    )
    print(count, count_sum)
    print(ave)

    """
    annotation
    """
    from django.db.models.functions import Length

    restaurants = Restaurant.objects.annotate(len_name=Length("name")).filter(
        len_name__gte=10
    )
    print(restaurants.values("name", "len_name"))

    """
    Null
    """
    from django.db.models import F, Sum
    from django.db.models.functions import Coalesce

    restaurants = Restaurant.objects.filter(capacity__isnull=True)
    restaurants = Restaurant.objects.order_by(F("capacity").desc(nulls_last=True))
    sum_capacity = Restaurant.objects.aggregate(
        total_capacity=Coalesce(Sum("capacity"), 0)
    )
    print(sum_capacity)
    # 1
    avg_rate = Rating.objects.filter(rating__lt=0).aggregate(
        avg_t=Coalesce(Avg("rating"), 0.0)
    )
    # 2
    avg_rate = Rating.objects.filter(rating__lt=0).aggregate(Avg("rating", default=0.0))
    print(avg_rate)

    """
    When, Case
    """
    from django.db.models import Case, When

    restaurants = Restaurant.objects.annotate(
        is_italian=Case(
            When(restaurant_type="IT", then=True),
            default=False,
        )
    )
    print(restaurants.values("name", "is_italian"))

    restaurants = Restaurant.objects.annotate(sales_number=Count("sales"))
    restaurants = restaurants.annotate(
        is_popular=Case(
            When(sales_number__gte=8, then=True),
            default=False,
        )
    )

    """
    Subquery, outref
    """
    from django.db.models import OuterRef, Subquery

    from ..models import Sale

    restaurants = Restaurant.objects.filter(restaurant_type__in=["IT", "CH"])
    sales = Sale.objects.filter(restaurant__in=Subquery(restaurants.values("pk")))

    # annotate each restaurant with the last income
    sales = Sale.objects.filter(restaurant=OuterRef("pk")).order_by("-created_at")
    restaurants = Restaurant.objects.all()
    restaurants = restaurants.annotate(
        last_sale_income=Subquery(sales.values("income")[:1])
    )
    for r in restaurants:
        print(r.name, r.last_sale_income)

    """
    Exists
    """
    # filter to restaurants that any sales with income > 85
    from django.db.models import Exists

    restaurants = Restaurant.objects.filter(
        Exists(Sale.objects.filter(restaurant=OuterRef("pk"), income__gt=85))
    )
