class Tile:
    def __init__(self, tile_type, position):
        self.type = tile_type
        self.position = position
        # self.wood, self.stone, self.metal = constants.TILE_DATA[tile_type]

    def get_type(self):
        return self.type

    def get_position(self):
        return self.position

    # def take_wood(self, amount=1): # defaults, left for future in case decide change.
    #     if self.wood > 0:
    #         self.wood = self.wood - amount
    #         if self.wood < 0:
    #             self.wood = 0  # ensures resource is fully used, but cant go negative.
    #         return True
    #     return False
    #
    # def take_stone(self, amount=1):
    #     if self.stone > 0:
    #         self.stone = self.stone - amount
    #         if self.stone < 0:
    #             self.stone = 0
    #         return True
    #     return False
    #
    # def take_metal(self, amount=1):
    #     if self.metal > 0:
    #         self.metal = self.metal - amount
    #         if self.metal < 0:
    #             self.metal = 0
    #         return True
    #     return False