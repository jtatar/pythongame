import os
import sys

os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, os.getcwd())
from src.GameControl import GameControl

game = GameControl()
game.run()