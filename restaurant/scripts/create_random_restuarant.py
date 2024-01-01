from ..tests.factories import RestaurantFactory


def run(numbers=1):
    RestaurantFactory.create_batch(int(numbers))
