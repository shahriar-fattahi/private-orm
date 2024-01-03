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

    rating = obj1.rating_set.all()
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
