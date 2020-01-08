from panda3d.core import SamplerState
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectButton import DirectButton
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Func
from direct.gui.DirectGuiBase import DGG
from sys import exit

class Menu(object):
    def __init__(self ,main):
        self.main =main
        wx = base.win.get_x_size()
        wy = base.win.get_y_size()
        kx = 1600
        ky = 900
        self.myFrame = DirectFrame(frameColor=(1 ,1 ,1 ,1),
                                   frameSize=(0, kx ,0, ky))

        menu_tex = loader.loadTexture("res/menu.png")
        menu_tex.set_minfilter(SamplerState.FT_nearest)
        menu_tex.set_magfilter(SamplerState.FT_linear)
        self.myFrame["frameTexture"] = menu_tex
        self.myFrame.reparentTo(base.pixel2d)
        self.myFrame.set_pos( (wx -kx) / 2, 0, -(wy +ky) / 2)
        self.myFrame.set_transparency(True)

        self.startButton = DirectButton(
            text = "",
            text_scale=1.0,
            text_fg=(0.2 ,0.2 ,0.2 ,1),
            frameTexture="res/start.png",
            frameColor=(1 ,1 ,1 ,1),
            frameSize=(-64, 64, -20, 20),
            command=self.main.startGame,
            relief=DGG.FLAT,
            rolloverSound=None,
            clickSound=None,
            parent=self.myFrame,
            scale=2.0,
            pos=(wx /2 , 0, wy /2 + 50)
        )
        self.startButton.setTransparency(1)

        self.exitButton = DirectButton(
            text = "",
            text_scale=1.0,
            text_fg=(0.2 ,0.2 ,0.2 ,1),
            frameTexture="res/exit.png",
            frameColor=(1 ,1 ,1 ,1),
            frameSize=(-64, 64, -20, 20),
            relief=DGG.FLAT,
            command=exit,
            rolloverSound=None,
            clickSound=None,
            parent=self.myFrame,
            scale=2.0,
            pos=(wx / 2, 0, wy / 2 - 50)
        )
        self.exitButton.setTransparency(1)

        self.resumeButton = DirectButton(
            text="",
            text_scale=1.0,
            text_fg=(0.2, 0.2, 0.2, 1),
            frameTexture="res/resume.png",
            frameColor=(1, 1, 1, 1),
            frameSize=(-64, 64, -20, 20),
            relief=DGG.FLAT,
            command=self.main.resumeGame,
            rolloverSound=None,
            clickSound=None,
            parent=self.myFrame,
            scale=2.0,
            pos=(wx / 2, 0, wy / 2 + 150)
        )

        self.resumeButton.setTransparency(1)
        self.resumeButton.hide()

    def hideMenu(self):
        self.main.gui.show()
        seq= Sequence(LerpColorScaleInterval(self.myFrame, 0.4 ,(1, 1, 1, 0)), Func(self.myFrame.hide))
        seq.start()

    def hideResume(self):
        seq = Sequence(LerpColorScaleInterval(self.resumeButton, .5, (1, 1, 1, 0)), Func(self.resumeButton.hide))
        seq.start()

    def showResume(self):
        self.resumeButton.show()
        seq = Sequence(LerpColorScaleInterval(self.resumeButton, .5, (1, 1, 1, 1)))
        seq.start()

    def showMenu(self):
        self.myFrame.show()
        self.main.gui.hide()
        seq = Sequence(LerpColorScaleInterval(self.myFrame, .5, (1, 1, 1, 1)))
        seq.start()
