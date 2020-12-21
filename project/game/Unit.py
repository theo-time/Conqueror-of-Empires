class Unit:
    def __init__(self, unit_type, position, owner):
        self.type = unit_type
        self.position = position

        # Unit Specs
        self.max_health = constants.UNIT_SPECS[unit_type]["max_health"]
        self.health = self.max_health
        self.attack = constants.UNIT_SPECS[unit_type]["attack"]
        self.defence = constants.UNIT_SPECS[unit_type]["defence"]
        self.movement = constants.UNIT_SPECS[unit_type]["movement"]
        self.reach = constants.UNIT_SPECS[unit_type]["reach"]

        self.allowed_moves = constants.UNIT_SPECS[unit_type]["moves"]

        #  all set to True, so unit cannot act when it is spawned, must wait till next go (EFFECTIVELY BLOCKS SPAWN)
        self.moved = True
        self.attacked = True

        self.owner = owner  # TODO: getters for attributes?

    def move(self, position):
        self.position = position
        self.moved = True

    def has_moved(self):
        return self.moved

    def has_attacked(self):
        return self.attacked

    def set_attacked(self):
        self.attacked = True

    def make_inactive(self):
        self.set_attacked()
        self.moved = True

    def reset(self):
        self.moved = False
        self.attacked = False
