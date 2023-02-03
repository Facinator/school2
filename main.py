from dump.classes import Player, Window
from dump.definitions import get_data, save_data

cache, player, first_time = get_data()

if first_time:
    player["name"] = input("Player Name?")
    cache["first_time"] = False

player = Player(player["name"], player["level"], player["cost"], player["color"], player["speed"])

w = Window(player)
w.mainloop()

cache["Player"] = player.__end__()
save_data(cache)
