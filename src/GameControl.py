import os
import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file_data
from .Cube import Cube
from .Menu import Menu
from .LevelLoader import Level
from .CamControl import CamControl
from .GUI import GUI
from .Movement import Movement


class GameControl(ShowBase):
    def __init__(self):
        load_prc_file_data("", "win-size 1600 900")
        load_prc_file_data("", "window-title :)")
        # Later maybe icon/sound

        # -------RENDER PIPELINE--------

        pipeline_path = "../../"
        if not os.path.isfile(os.path.join(pipeline_path, "setup.py")):
            pipeline_path = "../../RenderPipeline/"

        sys.path.insert(0, pipeline_path)
        # Use the utility script to import the render pipeline classes
        from rpcore import RenderPipeline

        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # -------END OF PIPELINE -------

        # time of day
        self.render_pipeline.daytime_mgr.time = 0.812

        self.menu = Menu(self)
        self.level = Level(self)
        self.cube = Cube(self.level,"./models/player1.egg",1)
        self.cube1 = Cube(self.level, "./models/player2.egg", 2)
        self.movement = Movement(self.cube, self.cube1)
        self.cube.setMovement(self.movement)
        self.cube1.setMovement(self.movement)
        self.camControl = CamControl(self.cube)
        self.gui = GUI(self)
        self.menu.showMenu()
        base.accept("i", self.camControl.zoomIn)
        base.accept("o", self.camControl.zoomOut)

    def startGame(self):
        self.menu.hideMenu()
        self.level.loadLevel()
        self.cube.resetCube()
        self.cube.enableGameControl()
        self.cube1.resetCube()
        self.cube1.enableGameControl()
        base.accept("escape", self.pauseGame)

    def pauseGame(self):
        self.cube.disableGameControl()
        self.cube1.disableGameControl()
        self.menu.showMenu()
        self.menu.showResume()
        base.accept("escape", self.resumeGame )

    def resumeGame(self):
        self.menu.hideMenu()
        self.menu.hideResume()
        self.cube.enableGameControl()
        self.cube1.enableGameControl()
        base.accept("escape", self.pauseGame)

    def levelEnd(self):
        self.cube.disableGameControl()
        self.cube1.disableGameControl()
        self.menu.showMenu()
