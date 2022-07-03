import unittest
from texttable import Texttable
import random
from constants import *
import re
from unittest import TestCase


class Game:
    def __init__(self):
        self._width = 7
        self._height = 7
        self._number_of_asteroids = 8
        self._alien_ships = 2
        self._matrix = self._place_asteroids()
        self._earth = self._place_earth()
        self._place_alien()
        self._cheated = False
        self._game_over = False

    @staticmethod
    def near(matrix, i, j, bad_neighbour, including_me=True):
        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1, 0, 1, -1, 1, -1, 0, 1]
        if including_me:
            dx.append(0)
            dy.append(0)

        def valid(pair):
            return pair[0] in range(len(matrix)) and pair[1] in range(len(matrix[0]))

        for a in range(len(dx)):
            i2 = i + dx[a]
            j2 = j + dy[a]
            if valid((i2, j2)) and matrix[i2][j2] == bad_neighbour:
                return True
        return False

    def _place_asteroids(self):
        matrix = [[EMPTY for _ in range(self._width)] for __ in range(self._height)]
        for _ in range(self._number_of_asteroids):
            i = random.randrange(self._height)
            j = random.randrange(self._width)
            while self.near(matrix, i, j, ASTEROID):
                i = random.randrange(self._height)
                j = random.randrange(self._width)
            matrix[i][j] = ASTEROID
        return matrix

    def _place_earth(self):
        i = 3
        j = 3
        self._matrix[i][j] = EARTH
        return i, j

    def _place_alien(self):
        for i in range(self._height):
            for j in range(self._width):
                if self._matrix[i][j] == ALIEN:
                    self._matrix[i][j] = EMPTY
        for _ in range(self._alien_ships):
            i = random.randrange(self._height)
            if i == 0 or i == 6:
                j = random.randrange(self._width)
            else:
                j = random.choice([0, 6])
            while self._matrix[i][j] != EMPTY:
                i = random.randrange(self._height)
                if i == 0 or i == 6:
                    j = random.randrange(self._width)
                else:
                    j = random.choice([0, 6])

            self._matrix[i][j] = ALIEN

    def string_to_pair(self, string):
        if not re.match("[A-Z][0-9]$", string):
            raise ValueError("Invalid format for the position.")
        a = ord(string[0]) - ord('A')
        b = ord(string[1]) - ord('1')
        if a not in range(self._height) or b not in range(self._width):
            raise ValueError("Location out of matrix.")
        return a, b

    def fire(self, location):
        """
        This function executes the fire command at a given location. If there is an alien ship, the number of alien
        ships is reduced by one, and the location is marked as MISSED. If both alien ships are destroyed it means that
        the game is won so it return True. After each miss, the alien ships randomly move.
        :param location: string containing the
        coordinates of the cell we want to hit
        :return: MISS if there was already an asteroid or the location was hit previously
               : ALIEN if at the location is an alien ship
               : EARTH if at the location is the Earth
               : True if all alien ships are destroyed
        """

        location = self.string_to_pair(location)
        if self._matrix[location[0]][location[1]] == ASTEROID or self._matrix[location[0]][location[1]] == MISS:
            return MISS
        elif self._matrix[location[0]][location[1]] == ALIEN:
            self._alien_ships -= 1
            self._matrix[location[0]][location[1]] = MISS
            self._place_alien()
            return ALIEN
        elif self._matrix[location[0]][location[1]] == EARTH:
            return EARTH
        elif self._matrix[location[0]][location[1]] == EMPTY:
            self._matrix[location[0]][location[1]] = MISS
            self._place_alien()
            return MISS

        if self._alien_ships == 0:
            self._game_over = True
            return True

    def cheat(self):
        self._cheated = True

    def won(self):
        return self._alien_ships == 0

    def lost(self):
        return self._game_over

    def __str__(self):
        if self._cheated:
            aux = CHEAT_DICTIONARY
        else:
            aux = NORMAL_DICTIONARY
        text = Texttable()
        row = list(range(0, self._width + 1))
        # row = list(chr(ord('A')))
        text.add_row(row)
        for i in range(self._height):
            row = [chr(ord('A') + i)]
            for j in range(self._width):
                elem = aux[self._matrix[i][j]]
                if self._matrix[i][j] == ALIEN and self.near(self._matrix, i, j, EARTH, False):
                    elem = CHEAT_DICTIONARY[self._matrix[i][j]]
                row.append(elem)
            text.add_row(row)
        return text.draw()


class TestFireCommand(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test__fire__coordinate__empty(self):
        matrix = [[EMPTY for _ in range(Game()._width)] for __ in range(Game()._height)]
        command = "A1"
        self.assertEqual(Game().fire(command), MISS)

    def test__fire__coordinate__asteroid(self):
        matrix = [[EMPTY for _ in range(Game()._width)] for __ in range(Game()._height)]
        matrix[0][0] = ASTEROID
        command = "A1"
        self.assertEqual(Game().fire(command), MISS)

    def test__fire__coordinate__miss(self):
        matrix = [[EMPTY for _ in range(Game()._width)] for __ in range(Game()._height)]
        matrix[0][0] = MISS
        command = "A1"
        self.assertEqual(Game().fire(command), MISS)

    def test__fire__coordinate__alien(self):
        matrix = [[EMPTY for _ in range(Game()._width)] for __ in range(Game()._height)]
        matrix[0][0] = ALIEN
        command = "A1"
        self.assertEqual(Game().fire(command), MISS)

    def test__fire__coordinate__earth(self):
        matrix = [[EMPTY for _ in range(Game()._width)] for __ in range(Game()._height)]
        matrix[3][3] = EARTH
        command = "D4"
        self.assertEqual(Game().fire(command), EARTH)

class TestStringToPair(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test__string_to_pair__string__True(self):
        string = "A2"
        self.assertEqual((0,1), Game().string_to_pair(string))

    def test__string_to_pair__string__False(self):
        string = "A2"
        self.assertFalse((0,0) == Game().string_to_pair(string))
