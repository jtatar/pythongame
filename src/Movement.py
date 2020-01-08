class Movement:

    def __init__(self, cube, cube1):
        self.cube = cube
        self.cube1 = cube1
        self.isGameOver = False

    def checkMove(self, level, x, y, sounds=None, task=None):
        """
            checking for moves
            returns 1 for game lost
            returns 2 for wall
            returns 3 for already lost game
            returns 0 for normal move
        """

        tile = level.getTileFromPos(x,y)

        if tile == None:
            if(not self.isGameOver):
                self.isGameOver=True
                return 1
            else:
                return 3

        elif tile.getTag("Type") == "wall":
            return 2
        else:
            taskMgr.doMethodLater(2, level.destroyTile, "destroyTile", extraArgs=[x,y])
            taskMgr.doMethodLater(2, self.checkCubesOnTile, "checkCubesOnTile", extraArgs=[x, y, self.cube, self.cube1])
            return 0

    def checkCubesOnTile(self, x, y, cube, cube1, task=None):
        """
            used to check if there is any cube on the falling tile
        """
        if(not self.isGameOver):
            x1,y1 = cube.getCubeTiles()
            x2,y2 = cube1.getCubeTiles()
            if(x1==x and y1==y):
                cube.loseGame()
                self.isGameOver=True
            elif(x2==x and y2==y):
                cube1.loseGame()
                self.isGameOver=True
            else:
                return 0
    def resetCubePosition(self, move):
        """
            reset the other cube position if game is restarted
        """
        if(move == 1):
            self.cube1.resetCube()
        elif(move == 2):
            self.cube.resetCube()
        else:
            return 0

    def disableControl(self):
        """
            disable control over cubes
        """
        self.cube1.disableGameControl()
        self.cube.disableGameControl()

    def resetGame(self):
        """
            enable control over cubes
        """
        self.isGameOver=False
        self.cube.enableGameControl()
        self.cube1.enableGameControl()





