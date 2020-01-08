from panda3d.core import NodePath, Vec3
from direct.interval.LerpInterval import LerpPosQuatInterval
from direct.interval.LerpInterval import LerpFunc
from random import random
from panda3d.core import RigidBodyCombiner
from random import randrange
from .Sound import *
from panda3d.core import OmniBoundingVolume


class Level:
    def __init__(self, main):
        self.main = main
        self.sounds = Sounds()
        self.loadBackground()
        self.LevelNr = 0

    def loadBackground(self, background="./models/scene/Scene.bam"):
        base.setBackgroundColor(1, 1, 1)
        self.background = loader.loadModel(background)
        self.background.reparentTo(render)
        self.background.setZ(-10)
        self.background.setScale(.3)
        self.background.setH(-90)

    def loadLevel(self):
        """
            loading random level from 0-2
        """
        i = randrange(3)
        if self.LevelNr == i:
            self.LevelNr = (self.LevelNr + 1) % 3
        else:
            self.LevelNr = i

        print("trying to load level nr:", self.LevelNr)
        # handle unloading of the map here.
        try:
            tiles = self.levelNode.findAllMatches("=Pos")
        except:
            tiles = []
            print("No tiles to remove")
        for tile in tiles:
            tile.remove_node()

        try:
            self.levelNode.remove_node()
        except:
            print("failed to remove old level node or there was none")

        print("loading level...")
        try:
            data = open("./levels/level_" + str(self.LevelNr)).read()
        except:
            print("Couldnt open level file: " + str(self.LevelNr))
            self.main.levelEnd()
            return 1

        self.levelNode = self.loadLevelData(data)
        print(self.levelNode, "returning levelNode")
        self.levelNode.reparentTo(render)
        self.fadeInLevel()
        return 0

    def loadTile(self, data):
        """
            Load tiles by types
        """
        data = data.split(",")
        tile = None
        for i in data:
            # check for the type and load tile
            if i.startswith("Type="):
                i = i.split("=")
                tile = loader.loadModel("./models/" + i[1] + ".egg")
                tile.setTag(i[0], i[1])
                break

        for i in data:
            if i.startswith("Pos=") and tile != None:
                i = i.split("=")
                tile.setTag(i[0], i[1])
                break

        if tile:
            if tile.hasTag("Pos") and tile.hasTag("Type"):
                return tile
            else:
                return None
        else:
            return None

    def loadLevelData(self, inputData):
        """
        processes the level asloaded from the file. it seperates the input data until the data for each tile is ready.
        """
        rigidNode = RigidBodyCombiner("LevelNode")
        levelNode = NodePath(rigidNode)

        #deleting whitespaces and seperating the content for each tile into a list.
        inputData = inputData.replace("\n", "").strip().replace(" ", "").lstrip("<").rstrip(">").split("><")

        for tileData in inputData:
            tile = self.loadTile(tileData)
            if tile != None:
                tile.reparentTo(levelNode)
                tile.setPos(self.getPosFromTile(tile))
                tile.setZ(tile,
                          0.00000001)  # workaround for rigid body combiner so it does not assume the (0,0) tile as static
            else:
                print("ERROR, could not load tile with data: ", tileData)
        rigidNode.collect()
        inode = rigidNode.getInternalScene().node()  # workaround for a boundingvolume issue with rigidbodycombiner
        inode.setBounds(OmniBoundingVolume())  # still workaround
        inode.setFinal(True)  # still workaround
        return levelNode

    def getTileFromPos(self, x, y):
        """
        returns the nodePath of a tile with the given tile number
        """
        if type(x) == list or type(x) == tuple:
            y = x[1]
            x = x[0]
        tile = self.levelNode.find("=Pos=" + str(x) + "_" + str(y))
        if tile.isEmpty():
            return None
        else:
            return tile

    def getPosFromTile(self, tile):
        """
        returns the tile position given a tile's nodePath, or None if the nodepath has no position tags
        """
        if tile.hasTag("Pos"):
            pos = tile.getTag("Pos").split("_")
            x, y = int(pos[0]), int(pos[1])
            return (x, y, 0)
        else:
            print("ERROR, supplied tile has no 'Pos' tag")
            return None

    def getStartTile(self, move):
        if(move==1):
            tile = self.levelNode.find("=Type=start")
        elif(move==2):
            tile = self.levelNode.find("=Type=start2")
        if tile.isEmpty() == True:
            print("Start-Tile was not found")
        return tile

    def fadeOutLevel(self, fadeTime=1):
        """
        the level-falls-apart animation.
        """
        tiles = self.levelNode.findAllMatches("=Pos")
        for tile in tiles:
            x, y, z = self.getPosFromTile(tile)
            tile.setPos(x, y, 0)
            final_hpr = Vec3(random(), random(), random()) * 360.0
            force = (Vec3(random(), random(), random()) - 0.5) * 5.0
            force.z = 0

    def fadeInLevel(self, fadeTime=1.6):
        """
        fade-in animation. the parameter it takes is the time in seconds.changing it might cause animation glitches with the cube-fade-in animation
        """
        self.sounds.playSound("nyon.wav")
        tiles = self.levelNode.findAllMatches("=Pos")
        for tile in tiles:
            x, y, z = self.getPosFromTile(tile)
            tile.setPos(x, y, -15)
            tile.setHpr(random() * 360 - 180, random() * 360 - 180, random() * 360 - 180)
            seq = LerpPosQuatInterval(tile, fadeTime + (0.3 * fadeTime * random()), (x, y, 0), (0, 0, 0),
                                      blendType='easeOut')
            tile.setPythonTag("Seq", seq)
            seq.start()

    def destroyTile(self, x, y, task=None):
        """
            fall animation of tile, sets position of tile to -99,-99
        """
        tile = self.getTileFromPos(x,y)
        if(tile!=None):
            tile.setTag('Pos','-99_-99')
            final_hpr = Vec3(random(), random(), random()) * 360.0 * 0.0
            anim = LerpFunc(self.animateTile, fromData=0, toData=1, duration=1.3, blendType='noBlend',
                            extraArgs=[tile.get_pos(render), Vec3(0), final_hpr, tile, Vec3(1.7, 0, 0)])
            tile.setPythonTag("Seq", anim)
            anim.start()

    def animateTile(self, t, initial_pos, initial_hpr, dest_hpr, tile, force):
        """
            used for fall animation
        """
        z_force = -(t ** 2) * 9.81 * 1.7
        regular_force = force * t
        dest_pos = initial_pos + regular_force + Vec3(0, 0, z_force)
        tile.set_pos(render, dest_pos)
        tile.set_hpr(render, initial_hpr * (1 - t) + dest_hpr * t)