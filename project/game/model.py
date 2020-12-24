# Ben-Ryder 2019

import random
import paths
import constants
from project.game.Unit import Unit
from project.game.World import World


import project.game.calculations as calculations


class Model:
    """ holds all the data and interface to manipulate the game """
    def __init__(self, game_name, map_name, players):  # only when creating new game
        self.game_name = game_name
        self.map_name = map_name
        self.game_end = False

        self.players = [Player(p["name"], p["colour"]) for p in players]
        self.current_player = self.players[0]

        self.world = World(self.map_name, self.players)  # assigns settlements to players

        self.current_player.start_turn()

    def all_units(self):
        return [unit for player in self.players for unit in player.units]

    def next_turn(self):
        self.current_player.end_turn()

        # Getting new turn
        if not self.is_winner():  # if more than 1 player alive
            self.current_player = self.get_next_player()
        else:
            self.game_end = True

        self.current_player.start_turn()

    def get_next_player(self):
        valid_choice = False
        player = self.current_player
        while not valid_choice:  # wont be infinite, as to be called at least two players are left.
            if self.players.index(player) < len(self.players) - 1:
                player = self.players[self.players.index(player) + 1]
            else:
                player = self.players[0]
            valid_choice = not player.is_dead()
        return player

    def try_spawn(self, unit_type, position):
        if not self.get_unit(position):
            if self.current_player.get_ap() - constants.UNIT_SPECS[unit_type]["spawn_cost"] >= 0:
                self.current_player.add_unit(Unit(unit_type, position, self.get_current_player()))
                self.current_player.take_ap(constants.UNIT_SPECS[unit_type]["spawn_cost"])
                return True
        return False

    def make_attack(self, attacker, defender):
        attacker.set_attacked()
        killed_units = calculations.apply_attack(attacker, defender)
        for unit in killed_units:  # could be both units
            unit.owner.units.remove(unit)

    def check_conquer(self, unit):
        if (self.world.get_tile(unit.position).get_type() == "c" and
                self.world.get_tile(unit.position).get_holder() != self.get_current_player()):
            if not unit.has_moved():  # must stay in settlement for a turn cycle
                return True
        return False

    def conquer(self, position):
        settlement = self.world.get_tile(position)
        if settlement.current_holder is not None:
            settlement.current_holder.remove_settlement(settlement)

        settlement.change_holder(self.get_current_player())
        self.current_player.add_settlement(settlement)

    def handle_death(self):
        for player in self.players:
            if self.check_death(player):
                player.kill()

                if self.is_winner():  # here, as otherwise must wait for next_turn call
                    self.game_end = True

                return player.get_name()  # assuming only one player died, return first found.
        return None

    def check_death(self, player):
        return len(player.settlements) == 0 and not player.is_dead()

    def game_ended(self):
        return self.game_end

    def is_winner(self):
        return len([player for player in self.players if not player.is_dead()]) == 1

    def get_winner(self):
        return self.current_player.get_name()  # will always end on current player, as they take last city.

    def get_current_player(self):
        return self.current_player

    def unit_selected(self, position):
        for unit in self.all_units():
            if position == unit.position:
                return True
        return False

    def get_unit(self, position):
        for unit in self.all_units():
            if unit.position == position:
                return unit
        return None

    def settlement_selected(self, position):
        tile = self.world.get_tile(position)
        if tile.get_type() == "c" and tile.get_holder() == self.get_current_player():
            return True
        return False

    def get_moves(self, unit):
        moves = []
        if not unit.has_moved():
            for x in range(unit.position[0] - unit.movement, unit.position[0] + unit.movement + 1):
                for y in range(unit.position[1] - unit.movement, unit.position[1] + unit.movement + 1):
                    if ([x, y] != unit.position and
                            x in range(0, constants.MAP_SIZE[0]) and
                            y in range(0, constants.MAP_SIZE[1]) and
                            self.world.get_tile([x, y]).get_type() in unit.allowed_moves and not self.get_unit([x, y])):
                        moves.append([x, y])

        return moves

    def move_unit(self, position, unit):
        unit.move(position)

    def get_attacks(self, unit):
        attacks = []
        if not unit.has_attacked():
            for x in range(unit.position[0] - unit.reach, unit.position[0] + unit.reach + 1):
                for y in range(unit.position[1] - unit.reach, unit.position[1] + unit.reach + 1):
                    if [x, y] != unit.position and self.get_unit([x, y]):
                        if self.get_unit([x, y]).owner != self.get_current_player():
                            attacks.append([x, y])
        return attacks


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







