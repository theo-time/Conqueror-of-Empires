import constants

class City:
    def __init__(self, name, position):
        self.type = "c"
        self.name = name
        self.position = position
        self.current_holder = None
        self.level = 1  # score and ap generated from level
        self.sub_level = 0  # SUB LEVEL STARTS FROM 0
        self.max_level = len(constants.LEVELS)

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def get_holder(self):
        return self.current_holder

    def get_type(self):
        return self.type

    def get_holder_colour(self):
        if self.current_holder is not None:
            return self.current_holder.get_colour()
        return None

    def get_ap_value(self, level=None):
        if level is not None:
            return level * 2
        return self.level * 2

    def get_score(self):
        return self.level * 1000

    def get_level(self):
        return self.level

    def add_level(self):  # not to be used directly, add level via add sub_level.
        self.level += 1

    def add_sub_level(self):
        self.current_holder.take_ap(self.get_upgrade_cost())
        self.sub_level += 1
        if not self.at_max():
            if self.sub_level == len(constants.LEVELS[self.level - 1]):
                self.add_level()
                self.sub_level = 0

    def get_upgrade_cost(self):
        return constants.LEVELS[self.level - 1][self.sub_level]

    def afford_upgrade(self):
        if self.current_holder.get_ap() - self.get_upgrade_cost() >= 0:
            return True
        return False

    def at_max(self):
        return self.level == self.max_level

    def change_holder(self, new_holder):
        self.current_holder = new_holder
