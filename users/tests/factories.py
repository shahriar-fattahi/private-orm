from django.contrib.auth import get_user_model
from django.utils.text import slugify
from factory import Sequence, django
from faker import Faker

fake = Faker()


class UserFactory(django.DjangoModelFactory):
    username = username = Sequence(lambda self: f"{self.first_name}-{self}")
    first_name = fake.first_name()
    last_name = fake.last_name()
    is_active = True
    is_admin = False
    is_superuser = False

    class Meta:
        model = get_user_model()
