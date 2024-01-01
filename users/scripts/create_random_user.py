from ..tests.factories import UserFactory


def run(number=1):
    UserFactory.create_batch(int(number))
