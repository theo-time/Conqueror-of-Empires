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