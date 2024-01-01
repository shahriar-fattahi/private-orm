import factory
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker


class UserFactory(factory.django.DjangoModelFactory):
    password = factory.django.Password("password")
    is_active = True
    is_admin = False
    is_superuser = False

    @factory.lazy_attribute
    def username(self):
        uid = Faker().random_number(digits=3)
        return slugify(f"{self.full_name} {uid}")

    @factory.lazy_attribute
    def first_name(self):
        return self.full_name.split()[0]

    @factory.lazy_attribute
    def last_name(self):
        return self.full_name.split()[1]

    class Meta:
        model = get_user_model()

    class Params:
        full_name = factory.Faker("name")
