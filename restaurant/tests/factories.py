import factory
from django.utils import timezone
from faker import Faker

from ..models import Restaurant


class RestaurantFactory(factory.django.DjangoModelFactory):
    website = Faker().hostname()
    date_opened = timezone.datetime.now()
    latitude = Faker().latitude()
    longitude = Faker().longitude()
    restaurant_type = Faker().random_element(
        elements=[type[0] for type in Restaurant.RestaurantType.choices]
    )

    @factory.lazy_attribute
    def name(self):
        name = Faker().company()
        return f"{name} ({self.uid})"

    class Meta:
        model = Restaurant

    class Param:
        uid = Faker().random_number(digits=3)
