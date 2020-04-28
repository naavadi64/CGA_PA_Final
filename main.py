import imgui
import imgui.core
from copy import copy
from imgui.integrations.pyglet import PygletRenderer
from pyglet.window import  key, mouse
from GameObject import *

bg = ImageObject("resource/spongy_wired.jpg")
sprsht = ImageObject("resource/spritesheet.png")
sprmask = ImageObject("resource/spritesheet_mask.png")
wire_sponge = WireSponge(Vector(800, 480))
img_draw = copy(bg)
img_display = pyglet.image.ImageData(
    img_draw.width,
    img_draw.height,
    'RGB',
    img_draw.get_bytes(),
    img_draw.pitch
)


def initialize_sprite():
    # Idle
    SpongeIdle = FrameCollection(SpongeState.idle)
    SpongeIdle.insert(Frame(82, 137, 26, 85, Vector(108, 60), 1))

    # Intro
    SpongeIntroChainFall = FrameCollection(SpongeState.introChainFall)
    SpongeIntroChainWait = FrameCollection(SpongeState.introChainWait)
    SpongeIntroChainFallEnd = FrameCollection(SpongeState.introChainFallEnd)
    SpongeIntroSpin = FrameCollection(SpongeState.introSpin)
    SpongeIntroCharge = FrameCollection(SpongeState.introCharge)

    SpongeIntroChainFall.insert(Frame(218, 268, 100, 169, Vector(250, 133), 1))
    SpongeIntroChainWait.insert(Frame(4, 63, 23, 86, Vector(38, 57), 6))
    SpongeIntroChainFallEnd.insert(Frame(82, 137, 26, 85, Vector(108, 58), 4))
    SpongeIntroSpin.insert(Frame(498, 549, 12, 80, Vector(524, 53), 1))
    SpongeIntroSpin.insert(Frame(221, 285, 19, 84, Vector(260, 57), 1))
    SpongeIntroSpin.insert(Frame(288, 354, 25, 84, Vector(329, 57), 1))
    SpongeIntroSpin.insert(Frame(149, 215, 26, 85, Vector(189, 58), 1))
    SpongeIntroSpin.insert(Frame(426, 490, 21, 80, Vector(465, 53), 1))
    SpongeIntroSpin.insert(Frame(365, 418, 23, 82, Vector(393, 55), 1))
    SpongeIntroSpin.insert(Frame(551, 603, 21, 80, Vector(578, 53), 1))
    SpongeIntroCharge.insert(Frame(602, 657, 25, 82, Vector(628, 58), 3))
    SpongeIntroCharge.insert(Frame(663, 720, 30, 81, Vector(690, 57), 40))
    SpongeIntroCharge.insert(Frame(602, 657, 25, 82, Vector(628, 58), 3))

    # Leap
    SpongeLeapBegin = FrameCollection(SpongeState.leapBegin)
    SpongeLeapUp = FrameCollection(SpongeState.leapUp)
    SpongeLeapDown = FrameCollection(SpongeState.leapDown)
    SpongeLeapEnd = FrameCollection(SpongeState.leapEnd)

    SpongeLeapBegin.insert(Frame(419, 474, 111, 165, Vector(445, 142), 4))
    SpongeLeapBegin.insert(Frame(82, 137, 26, 85, Vector(108, 60), 2))
    SpongeLeapUp.insert(Frame(283, 336, 103, 168, Vector(308, 132), 1))
    SpongeLeapDown.insert(Frame(346, 406, 105, 165, Vector(374, 138), 1))
    SpongeLeapEnd.insert(Frame(82, 137, 26, 85, Vector(108, 60), 2))
    SpongeLeapEnd.insert(Frame(419, 474, 111, 165, Vector(445, 142), 4))

    # Spin
    SpongeSpin = FrameCollection(SpongeState.spin)

    SpongeSpin.insert(Frame(498, 549, 12, 80, Vector(524, 53), 1))
    SpongeSpin.insert(Frame(221, 285, 19, 84, Vector(260, 57), 1))
    SpongeSpin.insert(Frame(288, 354, 25, 84, Vector(329, 57), 1))
    SpongeSpin.insert(Frame(149, 215, 26, 85, Vector(189, 58), 1))
    SpongeSpin.insert(Frame(426, 490, 21, 80, Vector(465, 53), 1))
    SpongeSpin.insert(Frame(365, 418, 23, 82, Vector(393, 55), 1))
    SpongeSpin.insert(Frame(551, 603, 21, 80, Vector(578, 53), 1))

    # Initializing the sprites
    wire_sponge.insert(SpongeIdle)
    wire_sponge.insert(SpongeIntroChainFall)
    wire_sponge.insert(SpongeIntroChainWait)
    wire_sponge.insert(SpongeIntroChainFallEnd)
    wire_sponge.insert(SpongeIntroSpin)
    wire_sponge.insert(SpongeIntroCharge)
    wire_sponge.insert(SpongeLeapBegin)
    wire_sponge.insert(SpongeLeapUp)
    wire_sponge.insert(SpongeLeapDown)
    wire_sponge.insert(SpongeLeapEnd)
    wire_sponge.insert(SpongeSpin)

    wire_sponge.setState(SpongeState.introChainFall)


def put_sprite(character):
    img_draw.data = bytearray(bg.data)
    frame = character.sprites[character.spritesId].frames[character.frameId]
    sprite_width = frame.xRight - frame.xLeft
    sprite_height = frame.yBottom - frame.yTop

    if character.facing == Facing.left:
        spriteLeft = character.position.x - frame.anchor.x + frame.xLeft
        spriteTop = character.position.y - frame.anchor.y + frame.yTop

        for i in range(sprite_width):
            for j in range(sprite_height):
                img_draw.set_pixel_bytearray(
                    spriteLeft+i, spriteTop+j,
                    ANDwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft+i, spriteTop+j),
                        sprmask.get_pixel_bytearray(frame.xLeft+i, frame.yTop+j)
                    )
                )

        for i in range(sprite_width):
            for j in range(sprite_height):
                img_draw.set_pixel_bytearray(
                    spriteLeft+i, spriteTop+j,
                    ORwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft+i, spriteTop+j),
                        sprsht.get_pixel_bytearray(frame.xLeft+i, frame.yTop+j)
                    )
                )
    else:
        spriteLeft = character.position.x + frame.anchor.x - frame.xRight
        spriteTop = character.position.y - frame.anchor.y + frame.yTop

        for i in range(sprite_width):
            for j in range(sprite_height):
                img_draw.set_pixel_bytearray(
                    spriteLeft + i, spriteTop + j,
                    ANDwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft + i, spriteTop + j),
                        sprmask.get_pixel_bytearray(frame.xRight - i, frame.yTop + j)
                    )
                )

        for i in range(sprite_width):
            for j in range(sprite_height):
                img_draw.set_pixel_bytearray(
                    spriteLeft + i, spriteTop + j,
                    ORwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft + i, spriteTop + j),
                        sprsht.get_pixel_bytearray(frame.xRight - i, frame.yTop + j)
                    )
                )


def display_img():
    put_sprite(wire_sponge)
    img_display.set_data(
        'RGB',
        img_draw.pitch,
        img_draw.get_bytes()
    )
    img_display.blit(0,0)


class Controls:  # --UI and Controls--
    def __init__(self, window):
        imgui.create_context()
        self.renderer = PygletRenderer(window)
        self.impl = PygletRenderer(window)
        imgui.new_frame()
        imgui.end_frame()

    def render_ui(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())

        # --This is where the fun begins--
        imgui.new_frame()
        if imgui.begin_main_menu_bar():

            if imgui.begin_menu("Application", True):
                selected_quit, clicked_quit = imgui.menu_item(
                    "Quit", "", False, True
                )
                if clicked_quit:
                    exit(1)
                if selected_quit:
                    pass

                imgui.end_menu()

        imgui.end_main_menu_bar()
        imgui.end_frame()


class Application(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=bg.width, height=bg.height, visible=True, caption="Animator")
        initialize_sprite()
        pyglet.clock.schedule_interval(self.update, 1/30)
        self.window_object = self
        self.control_ui = Controls(self.window_object)  # UI class call, check Controls section

    def on_draw(self):
        pass

    def update(self, dt):
        self.clear()
        wire_sponge.update()
        display_img()
        self.control_ui.render_ui()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE and wire_sponge.on_ground:
            wire_sponge.setState(SpongeState.leapBegin)
            wire_sponge.on_ground = False
        elif symbol == key.X and wire_sponge.on_ground and wire_sponge.curState != SpongeState.spin:
            wire_sponge.setState(SpongeState.spin)
        elif symbol == key.RIGHT:
            wire_sponge.facing = Facing.right
        elif symbol == key.LEFT:
            wire_sponge.facing = Facing.left

    def on_key_release(self, symbol, modifiers):
        pass


app = Application()
pyglet.app.run()
