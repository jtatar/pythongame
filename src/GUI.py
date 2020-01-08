from panda3d.core import TextNode, Vec4
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence,Parallel
from direct.interval.FunctionInterval import Func,Wait

class GUI(object):

    """
        Handles displaying score for both teams
    """

    def __init__(self, control):

        self.control = control
        self.blueScore = 0
        self.redScore = 0
        self.gui_node = pixel2d.attach_new_node("GUI")
        self.gui_node.hide()
        self.gui_node.set_transparency(True)

        roboto_light = loader.loadFont("res/Roboto-Light.ttf")
        roboto_light.set_scale_factor(1)
        roboto_light.set_pixels_per_unit(120)

        self.text_blue = TextNode("TextBlue")
        self.text_blue.set_text("BLUE: " + str(self.blueScore))
        self.text_blue.set_align(TextNode.A_left)
        self.text_blue.set_text_color(0, 0, 1, 1)
        self.text_blue.set_font(roboto_light)
        self.text_blue_np = self.gui_node.attach_new_node(self.text_blue)
        self.text_blue_np.set_scale(50.0)
        self.text_blue_np.set_pos(60, 0, -120)

        self.text_red = TextNode("TextRed")
        self.text_red.set_text("RED: " + str(self.redScore))
        self.text_red.set_align(TextNode.A_right)
        self.text_red.set_text_color(1, 0, 0, 1)
        self.text_red.set_font(roboto_light)
        self.text_red_np = self.gui_node.attach_new_node(self.text_red)
        self.text_red_np.set_scale(50.0)
        self.text_red_np.set_pos(base.win.get_x_size() - 60, 0, -120)

        self.anim = None

    def show(self):
        """
            showing text animation
        """
        self.gui_node.show()
        if self.anim is not None:
            self.anim.finish()
        self.anim = Sequence(
            LerpColorScaleInterval(self.gui_node, 0.2, Vec4(1), Vec4(1, 1, 1, 0), blendType="easeInOut")
        )
        self.anim.start()

    def hide(self):
        """
            hiding text animation
        """
        self.gui_node.hide()
        if self.anim is not None:
            self.anim.finish()
        self.anim = Sequence(
            LerpColorScaleInterval(self.gui_node, 0.2, Vec4(1, 1, 1, 0), Vec4(1), blendType="easeInOut")
        )
        self.anim.start()


    def add_points(self, player):
        """
            updating score after game end
        """
        if player == 2:
            self.blueScore += 1
            Sequence(
                LerpColorScaleInterval(self.text_blue_np, 0.4, Vec4(0, 0, 1, 0), Vec4(1), blendType="easeInOut"),
                Func(lambda *args: self.text_blue.set_text("BLUE: " + str(self.blueScore))),
                LerpColorScaleInterval(self.text_blue_np, 0.4, Vec4(1), Vec4(0, 0, 1, 0), blendType="easeInOut"),
            ).start()
        elif player == 1:
            self.redScore += 1
            Sequence(
                LerpColorScaleInterval(self.text_red_np, 0.4, Vec4(1, 0, 0, 0), Vec4(1), blendType="easeInOut"),
                Func(lambda *args: self.text_red.set_text("RED: " + str(self.redScore))),
                LerpColorScaleInterval(self.text_red_np, 0.4, Vec4(1), Vec4(1, 0, 0, 0), blendType="easeInOut"),
            ).start()