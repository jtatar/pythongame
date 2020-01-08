from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval, LerpScaleInterval
from direct.interval.LerpInterval import LerpPosHprInterval, LerpColorScaleInterval, LerpFunc
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.FunctionInterval import Func, Wait
from panda3d.core import Vec3
from random import random
from .Sound import *


class Cube:
    def __init__(self, level, model, move):
        self.level = level
        self.move = move
        self.sounds = Sounds()
        self.cube = loader.loadModel(model)
        self.cube.setPythonTag("TilePos", [0, 0])
        self.cube.setPythonTag("Animated", False)
        self.cube.reparentTo(render)
        self.shard_node = render.attach_new_node("shards")

    def enableGameControl(self):
        """
        assigns the keyboard-events to the block's movement
        """
        if(self.move==2):
            base.accept("arrow_up", self.rotateCube, ["up"])
            base.accept("arrow_down", self.rotateCube, ["down"])
            base.accept("arrow_left", self.rotateCube, ["left"])
            base.accept("arrow_right", self.rotateCube, ["right"])
        else:
            base.accept("w", self.rotateCube, ["up"])
            base.accept("s", self.rotateCube, ["down"])
            base.accept("a", self.rotateCube, ["left"])
            base.accept("d", self.rotateCube, ["right"])

    def disableGameControl(self):
        """
        clears the keyboard-events so the keys can be used to navigate the menu or other stuff.
        """
        if(self.move==2):
            base.ignore("arrow_up")
            base.ignore("arrow_down")
            base.ignore("arrow_left")
            base.ignore("arrow_right")
        else:
            base.ignore("w")
            base.ignore("s")
            base.ignore("a")
            base.ignore("d")

    def setPos(self, x1, y1=None):
        """
        sets blocks position
        """
        if type(x1) == list or type(x1) == tuple:
            y1 = x1[1]
            x1 = x1[0]
        if self.getCubeTiles()[1]:
            self.cube.setHpr(render, 0, 0, 0)

        self.cube.setPos(render, x1, y1, 1)
        self.setCubeTiles(x1, y1)

    def getCube(self):
        """
        returns the cube's node path.
        """
        return self.cube

    def getCubePlayer(self):
        """
        returns cube.move - define which player
        """
        return self.cube.move

    def getCubeTiles(self):
        """
        returns a list with [x1,y1]
        """
        return self.cube.getPythonTag("TilePos")

    def setCubeTiles(self, x1, y1):
        """
        sets the tile coordinates for the tiles the block is on. inputs are x1,y1
        """
        self.cube.setPythonTag("TilePos", [x1, y1])

    def isAnimated(self):
        """
        returns True if the block is currently playing an animation
        """
        return self.cube.getPythonTag("Animated")

    def setAnimated(self, param):
        """
        sets and clears the "isAnimated" tag
        """
        self.cube.setPythonTag("Animated", param)

    def fadeInCube(self, duration=2.5):
        """
        spawn cube from the top to the floor
        """
        self.setAnimated(True)
        x1, y1 = self.cube.getPythonTag("TilePos")
        # animate the cube, once finished clear the animation tag
        self.cube.setZ(render, 15)
        self.cube.wrtReparentTo(render)

        print("Starting fade in sequence")
        Sequence(LerpPosInterval(self.cube, duration, (x1, y1, 0.6), blendType="easeOut"),
                 Func(self.setAnimated, False)).start()

    def animate(self, myInterval):
        """
        return seq and after it sets animation to false
        """
        seq = Sequence(myInterval, Func(self.setAnimated, False))
        return seq

    def resetCube(self, task=None):
        """
        resets the cube postion + calling fadeInCube().
        """
        print("Resetting cube")
        x, y, z = self.level.getPosFromTile(self.level.getStartTile(self.move))
        self.setPos(x, y)
        print("Move or fall..")
        taskMgr.doMethodLater(3, self.movement.checkMove,"CheckMove",extraArgs=[self.level, x, y,self.sounds])
        self.cube.setHpr(render, 0, 0, 0)
        print("Fading in cube")
        self.fadeInCube()

    def levelUp(self, task=None):
        """
        calls level to spawn new map + resetCube()
        """
        if self.level.loadLevel() == 0:  # if level loaded successfully...
            self.resetCube()
            self.movement.resetCubePosition(self.move)
            self.movement.resetGame()
            self.enableGameControl()

        self.level.main.gui.add_points(self.move)

    def rotateCube(self, direction):
        """
        rotates and moves the cube according to the direction passed as first argument. accepted values are "up" "down" "left" "right"
        """
        #wont move cube if its already being animated
        if self.isAnimated():
            print("waiting for cube to end rotating")
            return

        # cleaning up from last rotation (we cant clean those up at the end of this function cause the interval needs the dummynode for rotation)
        self.cube.wrtReparentTo(render)
        try:
            dummy.remove_node()
        except:
            pass

        self.setAnimated(True)
        duration = 0.2
        x1, y1 = self.getCubeTiles()

        dummy = render.attachNewNode("dummy")
        dummy.reparentTo(self.cube)
        dummy.setZ(render, .1)
        dummy.wrtReparentTo(render)
        dummy.setHpr(0, 0, 0)
        dest_hpr = Vec3(0)


        if direction == "right":
                dummy.setY(dummy, 0.5)
                self.cube.wrtReparentTo(dummy)
                dest_hpr = Vec3(0, -90, 0)
                y1 = y1 + 1

        if direction == "left":
                dummy.setY(dummy, -0.5)
                self.cube.wrtReparentTo(dummy)
                dest_hpr = Vec3(0, 90, 0)
                y1 = y1 - 1

        if direction == "up":
                dummy.setX(dummy, -0.5)
                self.cube.wrtReparentTo(dummy)
                dest_hpr = Vec3(0, 0, -90)
                x1 = x1 - 1

        if direction == "down":
                dummy.setX(dummy, 0.5)
                self.cube.wrtReparentTo(dummy)
                dest_hpr = Vec3(0, 0, 90)
                x1 = x1 + 1

        print("Setting rotate animation")
        anim = self.animate(LerpHprInterval(dummy, duration, dest_hpr, (0, 0, 0)))

        checkresult = self.movement.checkMove(self.level, x1, y1, self.sounds)

        if checkresult == 1:
            self.setCubeTiles(x1, y1)
            self.loseGame(direction)
            anim.start()
        elif checkresult == 0:
            self.setCubeTiles(x1, y1)
            self.sounds.playSound("rotate.wav")
            anim.start()
        elif checkresult == 2:
            self.setAnimated(False)
        elif checkresult == 3:
            anim.start()
            self.setCubeTiles(x1,y1)
            self.fallAnimation(direction)


    def animateShard(self, t, initial_pos, dest_hpr, shard, force):
        z_force = -(t ** 2) * 9.81 * 1.7
        regular_force = force * t
        dest_pos = initial_pos + regular_force + Vec3(0, 0, z_force)
        shard.set_pos(dest_pos)
        shard.set_hpr(dest_hpr * t)

    def animateCube(self, t, initial_pos, initial_hpr, dest_hpr, cube, force):
        z_force = -(t ** 2) * 9.81 * 1.7
        regular_force = force * t
        dest_pos = initial_pos + regular_force + Vec3(0, 0, z_force)
        cube.set_pos(render, dest_pos)
        cube.set_hpr(render, initial_hpr * (1 - t) + dest_hpr * t)

    def setMovement(self, movement):
        self.movement = movement

    def loseGame(self, direction="down"):
        self.fallAnimation(direction)
        taskMgr.doMethodLater(1.3, self.endGame, "endGame")

    def fallAnimation(self, direction="down"):
        self.movement.disableControl()
        side_force = 1.7
        if direction == "up":
            force = Vec3(-side_force, 0, 0)
            dest_hpr = Vec3(0, 0, -90)
        elif direction == "down":
            force = Vec3(side_force, 0, 0)
            dest_hpr = Vec3(0, 0, 90)
        elif direction == "left":
            force = Vec3(0, -side_force, 0)
            dest_hpr = Vec3(0, 90, 0)
        elif direction == "right":
            force = Vec3(0, side_force, 0)
            dest_hpr = Vec3(0, -90, 0)
        self.setAnimated(True)
        final_hpr = dest_hpr * 3.0 + Vec3(random(), random(), random()) * 360.0 * 0.0
        anim = LerpFunc(self.animateCube, fromData=0, toData=1, duration=1.3, blendType='noBlend',
                        extraArgs=[self.cube.get_pos(render), Vec3(0), final_hpr, self.cube, force])
        anim.start()

    def endGame(self, task=None):
        dummy = render.attachNewNode("dummy")
        dummy.reparentTo(self.cube)
        dummy.setZ(render, .1)
        dummy.wrtReparentTo(render)
        dummy.setHpr(0, 0, 0)

        self.level.fadeOutLevel()

        Sequence(Wait(0.3), Func(lambda *args: self.cube.hide())).start()

        taskMgr.doMethodLater( 2, self.levelUp, "lvlup")
        taskMgr.doMethodLater( 2, lambda *args: self.cube.show(), "show cube")
        taskMgr.doMethodLater( 2, lambda *args: self.shard_node.node().remove_all_children(),
                              "clear shards")

        Sequence(Wait(0.2), Func(lambda *args: self.sounds.playSound("finish.wav"))).start()

        cube_min, cube_max = Vec3(-0.5, -0.5, -1), Vec3(0.5, 0.5, 1)
        self.shard_node.set_pos(dummy.get_pos(render) + Vec3(-0.5, 0, 0))
        shard_size = (cube_max - cube_min) / 5.0

        self.shard_node.hide()
        Sequence(Wait(0.22), Func(lambda *args: self.shard_node.show())).start()

        for i in range(5):
            for j in range(5):
                for k in range(5):
                    shard = loader.loadModel("models/CubeShard.bam")
                    shard.reparent_to(self.shard_node)
                    shard.set_x(i * shard_size.x + 0.1)
                    shard.set_y(j * shard_size.y + 0.1)
                    shard.set_z(k * shard_size.z + 0.2)
                    shard.set_scale(0.8 + random())

                    force = Vec3(i - 2 - 0.15, j - 2 - 0.15, k - 2 + 2.6)
                    force.normalize()
                    force *= 12.0 * (1 + random() * 0.5)

                    d_hpr = Vec3(random(), random(), random()) * 360.0 * (3.0 + random())

                    shard_anim = Sequence(
                        Wait(0.22),
                        LerpFunc(self.animateShard, fromData=0, toData=2, duration=2.0, blendType='noBlend',
                                 extraArgs=[shard.get_pos(), d_hpr, shard, force]),
                        LerpHprInterval(shard, 1.0 + random(), d_hpr * 1.6, d_hpr, blendType='noBlend'),
                    )
                    shard_anim.start()

