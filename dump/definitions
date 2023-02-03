import json

def get_data():
    """
    :return: cache, cost, color, player, first_time
    """
    with open("dump/data.json", "r") as f:
        cache = json.load(f)
        f.close()

        player = cache["Player"]
        first_time = cache["first_time"]

    return cache, player, first_time

def save_data(cache=dict):
    """
    :param cache:
    """
    with open("dump/data.json", "w") as f:
        json.dump(cache, f)
        f.close()
