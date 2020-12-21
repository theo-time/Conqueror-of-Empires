class Player:
    """ Each player of the game, which holds their units, key values and links to settlements etc"""
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.camera_focus = [None, None]  # TODO: system to auto-scroll to spawn
        self.show_minimap = False

        self.units = []
        self.settlements = []

        self.turn = 0
        self.ap = 3  # initial ap, not per turn. (first turn ap = self.ap + self.get_turn_ap()
        self.dead = False
        self.max_score = self.ap

        # self.wood = 0
        # self.stone = 0
        # self.metal = 0

    # def add_wood(self, amount):
    #     self.wood += amount
    #
    # def add_stone(self, amount):
    #     self.stone += amount
    #
    # def add_metal(self, amount):
    #     self.metal += amount

    def get_name(self):
        return self.name

    def is_dead(self):
        return self.dead

    def kill(self):
        self.dead = True

    def get_colour(self):
        return self.colour

    def get_turn(self):
        return self.turn

    def get_score(self):
        # score workout =  Each city's score +  turn*5 +  each unit's health.
        score = 0
        score += self.turn * 5
        for city in self.settlements:
            score += city.get_score()

        for unit in self.units:
            score += unit.health

        if score > self.max_score:
            self.max_score = score
        return score

    def get_max_score(self):
        return self.max_score

    def get_ap(self):
        return self.ap

    def get_turn_ap(self):
        ap = 0
        for city in self.settlements:
            ap += city.get_ap_value()  # changed from generate_ap
        return ap

    def take_ap(self, amount):
        self.ap -= amount

    def start_turn(self):
        self.ap += self.get_turn_ap()

        # Resetting all units for new turn
        for unit in self.units:
            unit.reset()

    def end_turn(self):
        self.turn += 1

    def add_settlement(self, reference):
        self.settlements.append(reference)

    def remove_settlement(self, reference):
        self.settlements.remove(reference)

    def add_unit(self, unit):
        self.units.append(unit)

    def delete_unit(self, unit):
        self.units.remove(unit)

    def get_camera_focus(self):
        return self.camera_focus

    def set_camera_focus(self, camera_focus):
        self.camera_focus = camera_focus

    def get_minimap_status(self):
        return self.show_minimap

    def set_minimap_status(self, show):
        self.show_minimap = show


