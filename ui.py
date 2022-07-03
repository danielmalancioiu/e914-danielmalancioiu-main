from game import Game
import re
from constants import *


class UI:
    def __init__(self, game=None):
        if game is None:
            game = Game()
        self._game = game

    def start(self):
        while True:
            if self._game.lost():
                print("You have lost the game:(")
                break
            if self._game.won():
                print("You have won the game, congrats!")
                break

            print(self._game)
            cmd = input("Enter your command: ")

            if mat := re.match("fire ([A-Z][0-9])$", cmd):
                try:
                    fire_command = self._game.fire(mat.group(1))
                    if fire_command == MISS:
                        print("You missed...")
                    elif fire_command == ALIEN:
                        print("You hit an alien ship!!")
                    elif fire_command == EARTH:
                        print("You can't destroy the Earth...")

                except ValueError as ve:
                    print(ve)
            elif cmd == "cheat":
                self._game.cheat()
                print("You've turned the cheats on.")
            else:
                print("Invalid command")


UI().start()
