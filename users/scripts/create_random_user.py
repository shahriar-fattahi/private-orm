from ..tests.factories import UserFactory


def run(numbers=1):
    UserFactory.create_batch(int(numbers))
