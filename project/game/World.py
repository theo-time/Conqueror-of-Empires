import paths
import constants
import random
from project.game.City import City
from project.game.Tile import Tile

class World:
    """ holds all the map tiles, be that a Tile or City, in a 2d-array """
    def __init__(self, map_name, players):  # __init__ creates new world
        self.format = get_world(map_name)

        self.city_names = CityPicker()

        # Make Tiles
        self.tiles = []
        for row in range(len(self.format[0])):  # assumes col 0, is same len as all others.
            self.tiles.append([])

            for col in range(len(self.format)):
                if self.format[row][col] == "c":
                    name = self.city_names.get_new()
                    self.tiles[-1].append(City(name, [row, col]))
                else:
                    self.tiles[-1].append(Tile(self.format[row][col], [row, col]))

        # Set player spawns
        self.set_spawns(players)

    def get_tile(self, position):
        return self.tiles[position[0]][position[1]]

    def get_format(self):
        return self.format

    def set_spawns(self, players):  # only time world needs player knowledge, no link made.
        spawn_choices = [tile for row in self.tiles for tile in row if tile.type == "c"]
        for player in players:
            city = random.choice(spawn_choices)
            spawn_choices.remove(city)

            # There is a two way relationship, so both must know of each other.
            player.add_settlement(city)
            city.change_holder(player)


def get_world(map_name):
    # Reading in the map from a .csv file, convert to list of strings.
    with open(paths.mapPath + map_name + ".csv", "r") as file:
        grid = file.read().split("\n")
        grid = [i.replace(",", "") for i in grid]

    # Converting for referencing as [row][col] as split by "/n" gives [col][row]
    new_grid = []
    for row in range(constants.MAP_SIZE[0]):
        new_grid.append([])
        for col in grid:
            new_grid[len(new_grid) - 1].append(col[row])

    return new_grid

class CityPicker:
    """ used to randomly assign names to cities """
    def __init__(self):
        # Load Name Choices
        with open(paths.dataPath + "city_names") as file:
            self.name_choices = file.read().split("\n")

    def get_new(self):
        choice = random.choice(self.name_choices)
        self.name_choices.remove(choice)
        return choice