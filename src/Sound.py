class Sounds(object):
    def __init__(self):
        self.soundlist = [
            ["rotate.wav" ,1],
            ["finish.wav" ,1],
            ["nyon.wav" ,1],
        ]
        self.soundDict ={}

        for sound in self.soundlist:
            self.soundDict[sound[0]] = loader.loadSfx("./sounds/" +sound[0])
            self.soundDict[sound[0]].setVolume(sound[1])

    def playSound(self ,soundname):
        if soundname in self.soundDict:
            self.soundDict[soundname].play()
        else:
            print("sound not found" ,soundname)
