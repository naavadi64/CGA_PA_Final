import imgui
import imgui.core
from copy import copy
from imgui.integrations.pyglet import PygletRenderer
from pyglet.window import key, mouse
from GameObject import *

bg = ImageObject("resource/spongy_wired.jpg")
sprsht = ImageObject("resource/spritesheet.png")
sprmask = ImageObject("resource/spritesheet_mask.png")
#dummy_sprsht = ImageObject("resource/dummy_spritesheet.bmp")
#dummy_sprmask = ImageObject("resource/dummy_spritesheet_mask.bmp")
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
    # ----Wire Sponge----
    # Idle
    SpongeIdle = FrameCollection(SpongeState.idle)
    SpongeIdle.insert(Frame(82, 137, 26, 85, Vector(108, 60), 1))

    # Intro
    SpongeIntroChainFall = FrameCollection(SpongeState.introChainFall)
    ChainIntroFall = FrameCollection(ChainState.fallIntro)
    ChainIntroRelease = FrameCollection(ChainState.releaseIntro)
    SpongeIntroChainWait = FrameCollection(SpongeState.introChainWait)
    SpongeIntroChainFallEnd = FrameCollection(SpongeState.introChainFallEnd)
    SpongeIntroSpin = FrameCollection(SpongeState.introSpin)
    SpongeIntroCharge = FrameCollection(SpongeState.introCharge)

    SpongeIntroChainFall.insert(Frame(218, 268, 100, 169, Vector(250, 133), 1, fist_position=Vector(259, 103)))
    ChainIntroFall.insert(Frame(986, 1002, 4, 22, Vector(994, 13), 1))
    ChainIntroRelease.insert(Frame(986, 1002, 4, 556, Vector(994, 280), 1))
    SpongeIntroChainWait.insert(Frame(4, 63, 23, 86, Vector(41, 57), 1, fist_position=Vector(48, 29)))
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

    # Chain Throw/Attack - States Unfinished
    SpongeChainHrzBegin = FrameCollection(SpongeState.throwHrzBegin)
    ChainThrowHrz = FrameCollection(ChainState.thrownH)
    SpongeChainHrz = FrameCollection(SpongeState.throwHrz)
    SpongeChainHrzPullStay = FrameCollection(SpongeState.throwHrzPullStay)
    ChainHrzPullStay = FrameCollection(ChainState.pullStayH)
    ChainHrzPullGo = FrameCollection(ChainState.pullGoH)
    SpongeChainHrzPullGo = FrameCollection(SpongeState.throwHrzPullGo)
    SpongeChainHrzEnd = FrameCollection(SpongeState.throwHrzEnd)
    #SpongeChainVrtBegin = FrameCollection(SpongeState)
    #SpongeChainVrt = FrameCollection()
    #SpongeChainVrtEnd = FrameCollection()

    SpongeChainHrzBegin.insert(Frame(420, 473, 112, 164, Vector(445, 142), 4))
    SpongeChainHrzBegin.insert(Frame(480, 537, 101, 166, Vector(493, 146), 2))
    SpongeChainHrzBegin.insert(Frame(550, 605, 102, 169, Vector(563, 147), 2))
    SpongeChainHrzBegin.insert(Frame(480, 537, 101, 166, Vector(493, 146), 1))
    SpongeChainHrzBegin.insert(Frame(626, 666, 112, 168, Vector(641, 143), 4))
    SpongeChainHrzBegin.insert(Frame(679, 724, 113, 167, Vector(699, 143), 2, fist_position=Vector(682, 137)))
    SpongeChainHrzBegin.insert(Frame(742, 787, 113, 169, Vector(762, 144), 2, fist_position=Vector(744, 137)))
    SpongeChainHrzBegin.insert(Frame(679, 724, 113, 167, Vector(699, 143), 2, fist_position=Vector(682, 137)))
    ChainThrowHrz.insert(Frame(312, 330, 504, 518, Vector(321, 511), 1))
    SpongeChainHrz.insert(Frame(679, 724, 113, 167, Vector(699, 143), 2, fist_position=Vector(682, 137)))
    SpongeChainHrzPullStay.insert(Frame(679, 724, 113, 167, Vector(699, 143), 2, fist_position=Vector(682, 137)))
    ChainHrzPullStay.insert(Frame(312, 330, 504, 518, Vector(321, 511), 1))
    ChainHrzPullGo.insert(Frame(312, 330, 504, 518, Vector(321, 511), 1))
    #SpongeChainVrt.insert(Frame(987, 1000, 4, 554, Vector(), 1))

    # Initializing the sprites
        # Idle
    wire_sponge.insert(SpongeIdle)
        # Intro
    wire_sponge.insert(SpongeIntroChainFall)
    wire_sponge.chain.insert(ChainIntroFall)
    wire_sponge.chain.insert(ChainIntroRelease)
    wire_sponge.insert(SpongeIntroChainWait)
    wire_sponge.insert(SpongeIntroChainFallEnd)
    wire_sponge.insert(SpongeIntroSpin)
    wire_sponge.insert(SpongeIntroCharge)
        # Leap
    wire_sponge.insert(SpongeLeapBegin)
    wire_sponge.insert(SpongeLeapUp)
    wire_sponge.insert(SpongeLeapDown)
    wire_sponge.insert(SpongeLeapEnd)
        # Spin
    wire_sponge.insert(SpongeSpin)
        # Throw chain Horizontal
    wire_sponge.insert(SpongeChainHrzBegin)
    wire_sponge.insert(SpongeChainHrz)
    wire_sponge.chain.insert(ChainThrowHrz)
    wire_sponge.insert(SpongeChainHrzPullStay)
    wire_sponge.chain.insert(ChainHrzPullStay)
    wire_sponge.chain.insert(ChainHrzPullGo)

    # Setting initial state
    wire_sponge.setState(SpongeState.introChainFall)
    wire_sponge.chain.setState(ChainState.fallIntro)

    # ----Dummy---- Class and State Unfinished(?)
    '''
    # Idle
    DummyIdle = FrameCollection(DummyState.idle)
    DummyIdle.insert(Frame(208, 239, 14, 49, Vector(224, 32), 1))

    # Intro/Spawn - States Undefined, frame timing Unfinished
    DummySpawnLine = FrameCollection(DummyState.SpawnLine)
    DummySpawnBlob = FrameCollection(DummyState.SpawnBlob)
    DummySpawnTp = FrameCollection(DummyState.SpawnTp)

    DummySpawnLine.insert(Frame(0, 9, 0, 49, Vector(4, 25), 1))
    DummySpawnBlob.insert(Frame(12, 35, 19, 49, Vector(), 1))
    DummySpawnTp.insert(Frame(38, 69, 6, 49, Vector(), 1))
    DummySpawnTp.insert(Frame(72, 103, 9, 49, Vector(), 1))
    DummySpawnTp.insert(Frame(140, 169, 14, 49, Vector(), 1))
    DummySpawnTp.insert(Frame(174, 205, 16, 49, Vector(), 1))
    DummySpawnTp.insert(Frame(208, 239, 14, 49, Vector(224, 32), 1))
    '''


def put_sprite(character):
    if character.curState.value == -1:
        return
    frame = character.sprites[character.spritesId].frames[character.frameId]
    sprite_width = frame.xRight - frame.xLeft
    sprite_height = frame.yBottom - frame.yTop

    if character.facing == Facing.left:
        spriteLeft = character.position.x - frame.anchor.x + frame.xLeft
        spriteTop = character.position.y - frame.anchor.y + frame.yTop

        for i in range(sprite_width):
            for j in range(sprite_height):
                if spriteTop+j <= 0 or spriteLeft+i <= 0:
                    continue
                img_draw.set_pixel_bytearray(
                    spriteLeft+i, spriteTop+j,
                    ANDwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft+i, spriteTop+j),
                        sprmask.get_pixel_bytearray(frame.xLeft+i, frame.yTop+j)
                    )
                )

        for i in range(sprite_width):
            for j in range(sprite_height):
                if spriteTop+j <= 0 or spriteLeft+i <= 0:
                    continue
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
                if spriteTop+j <= 0 or spriteLeft+i <= 0:
                    continue
                img_draw.set_pixel_bytearray(
                    spriteLeft + i, spriteTop + j,
                    ANDwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft + i, spriteTop + j),
                        sprmask.get_pixel_bytearray(frame.xRight - i, frame.yTop + j)
                    )
                )

        for i in range(sprite_width):
            for j in range(sprite_height):
                if spriteTop+j <= 0 or spriteLeft+i <= 0:
                    continue
                img_draw.set_pixel_bytearray(
                    spriteLeft + i, spriteTop + j,
                    ORwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft + i, spriteTop + j),
                        sprsht.get_pixel_bytearray(frame.xRight - i, frame.yTop + j)
                    )
                )


def display_img():
    img_draw.data = bytearray(bg.data)
    put_sprite(wire_sponge.chain)
    put_sprite(wire_sponge)
    img_display.set_data(
        'RGB',
        img_draw.pitch,
        img_draw.get_bytes()
    )
    img_display.blit(0,0)


class Interface:  # --UI and Controls--
    def __init__(self, window):
        imgui.create_context()
        self.impl = PygletRenderer(window)
        imgui.new_frame()  # Required since on call, imgui needs to render once
        imgui.end_frame()

        # --Imgui Window Variables--
        # --Format: Window Boolean followed by its variables, separate each window with one end line.
        self.showPlayerControls = False  #

        self.showDummyControls = False  #
        self.actStand = True
        self.actMove = False
        self.actAttack = False

        self.showControlHelp = False  #

        self.showAbout = False  #

        self.showTestWindow = False  #
        self.test_checkbox = False
        self.test_input_int = 0

    def render(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        imgui.new_frame()

        # --Imgui Windows--
        # --Note: Variables are defined in __init__ under Imgui Window Variables
        if self.showPlayerControls:
            imgui.begin("Player Controls")

            imgui.begin_child("movement", 320, 180, border=True)
            imgui.text("Movement")
            if imgui.button("Turn to Opposite", 300, 20):
                if wire_sponge.facing == Facing.left:
                    wire_sponge.facing == Facing.right
                else:
                    wire_sponge.facing = Facing.left
            if imgui.button("Face Left", 140, 20):
                wire_sponge.facing = Facing.left
            imgui.same_line(spacing=20)
            if imgui.button("Face Right", 140, 20):
                wire_sponge.facing = Facing.right
            if imgui.button("Walk (Toggle)", 300, 20):
                pass
            if imgui.button("Walk Left", 140, 20):
                pass
            imgui.same_line(spacing=20)
            if imgui.button("Walk Right", 140, 20):
                pass
            if imgui.button("Jump", 300, 20):
                if wire_sponge.on_ground:
                    wire_sponge.setState(SpongeState.leapBegin)
                    wire_sponge.on_ground = False
            imgui.new_line()
            imgui.end_child()

            imgui.begin_child("skills", 320, 120, border=True)
            imgui.text("Attacks and Skills")
            if imgui.button("Attack", 300, 20):
                pass
            if imgui.button("Chain Spin", 300, 20):
                if wire_sponge.on_ground and wire_sponge.curState != SpongeState.spin:
                    wire_sponge.setState(SpongeState.spin)
            if imgui.button("Thunder Dance", 300, 20):
                pass
            imgui.new_line()
            imgui.end_child()

            imgui.end()

        if self.showDummyControls:
            imgui.begin("Dummy Controls")

            imgui.begin_child("spawn", 320, 80, border=True)
            imgui.text("Spawn Controls")
            if imgui.button("Respawn", 300, 20):
                pass
            if imgui.button("Spawn", 140, 20):
                pass
            imgui.same_line(spacing=20)
            if imgui.button("Despawn", 140, 20):
                pass
            imgui.new_line()
            imgui.end_child()

            imgui.begin_child("behaviour", 320, 80, border=True)
            imgui.text("Behaviour Controls")
            changed, self.actStand = imgui.checkbox("Stand", self.actStand)
            changed, self.actMove = imgui.checkbox("Move", self.actMove)
            changed, self.actAttack = imgui.checkbox("Attack", self.actAttack)
            imgui.new_line()
            imgui.end_child()

            imgui.end()

        if self.showControlHelp:
            imgui.begin("Control Help")
            imgui.text("Arrow Keys: Move")
            imgui.text("Space:      Jump")
            imgui.text("Z:          Attack")
            imgui.text("X:          Spin Chain")
            imgui.text("C:          Thunder Dance")
            imgui.end()

        if self.showTestWindow:
            imgui.begin("Test Window")
            imgui.text("This is the test window.")
            changed, self.test_checkbox = imgui.checkbox("Test Checkbox", self.test_checkbox)
            if imgui.button("Test Button", 100, 20):
                pass
            changed, self.test_input_int = imgui.input_int("Integer Input Test", self.test_input_int)
            imgui.end()

        # --This is where the fun begins--
        if imgui.begin_main_menu_bar():

            if imgui.begin_menu("Application", True):

                selected_test, clicked_test = imgui.menu_item(
                    "Test Window", "", False, True
                )
                if clicked_test:
                    if not self.showTestWindow:
                        self.showTestWindow = True
                    else:
                        self.showTestWindow = False

                if selected_test:
                    pass

                selected_quit, clicked_quit = imgui.menu_item(
                    "Quit", "", False, True
                )
                if clicked_quit:
                    exit(0)
                if selected_quit:
                    pass

                imgui.end_menu()

            if imgui.begin_menu("Controls", True):
                selected_reset, clicked_reset = imgui.menu_item(
                    "Reset All", "", False, True
                )
                if clicked_reset:
                    pass
                if selected_reset:
                    pass

                selected_player, clicked_player = imgui.menu_item(
                    "Player", "", False, True
                )
                if clicked_player:
                    if not self.showPlayerControls:
                        self.showPlayerControls = True
                    else:
                        self.showPlayerControls = False
                if selected_player:
                    pass

                selected_dummy, clicked_dummy = imgui.menu_item(
                    "Dummy", "", False, True
                )
                if clicked_dummy:
                    if not self.showDummyControls:
                        self.showDummyControls = True
                    else:
                        self.showDummyControls = False
                if selected_dummy:
                    pass

                imgui.end_menu()

            if imgui.begin_menu("Help", True):
                selected_controls, clicked_controls = imgui.menu_item(
                    "Keyboard Controls", "", False, True
                )
                if clicked_controls:
                    if self.showControlHelp:
                        self.showControlHelp = False
                    else:
                        self.showControlHelp = True
                if selected_controls:
                    pass

                selected_about, clicked_about = imgui.menu_item(
                    "About", "", False, True
                )
                if clicked_about:
                    if self.showAbout:
                        self.showAbout = False
                    else:
                        self.showAbout = True
                if selected_about:
                    pass

                imgui.end_menu()

        imgui.end_main_menu_bar()
        imgui.end_frame()
        # --UI ends here--


# --Main Application--
class Application(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=bg.width, height=bg.height, visible=True, caption="Animator")
        initialize_sprite()
        pyglet.clock.schedule_interval(self.update, 1/30)
        self.interface = Interface(self)  # UI class call, check Controls class

    def on_draw(self):
        pass

    def update(self, dt):
        self.clear()
        wire_sponge.update()
        wire_sponge.chain.update()
        display_img()
        self.interface.render()

    '''
    Controls:
    Arrow key left:     Turn/Move Left
    Arrow key right:    Turn/Move Right
    Arrow key up:       Look up (Contextual) 
    Arrow key down:     Look down (Contextual) 
    Space:              Jump/Leap
    Z:                  Attack with chain (Left/Right)
    X:                  Spin Chain
    C:                  Thunder Dance
    Arrow key up + Z:   Attack with chain (Up)
    '''
    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT and wire_sponge.curState == SpongeState.idle and wire_sponge.on_ground:
            wire_sponge.facing = Facing.left
            wire_sponge.chain.facing = Facing.left

        elif symbol == key.RIGHT and wire_sponge.curState == SpongeState.idle and wire_sponge.on_ground:
            wire_sponge.facing = Facing.right
            wire_sponge.chain.facing = Facing.right

        elif symbol == key.UP:
            pass

        elif symbol == key.DOWN:
            pass

        elif symbol == key.SPACE and wire_sponge.on_ground and wire_sponge.curState == SpongeState.idle:
            wire_sponge.setState(SpongeState.leapBegin)
            wire_sponge.on_ground = False

        elif symbol == key.Z:
            pass

        elif symbol == key.X and wire_sponge.on_ground and wire_sponge.curState != SpongeState.spin:
            wire_sponge.setState(SpongeState.spin)

        elif symbol == key.C and wire_sponge.chain.curState == ChainState.NaN:
            wire_sponge.setState(SpongeState.throwHrzBegin)

    def on_key_release(self, symbol, modifiers):  # pass if not needed
        if symbol == key.LEFT:
            pass

        if symbol == key.RIGHT:
            pass

        if symbol == key.UP:
            pass

        if symbol == key.DOWN:
            pass

        if symbol == key.SPACE and wire_sponge.on_ground:
            pass

        if symbol == key.Z:
            pass

        if symbol == key.X:
            pass

        if symbol == key.C:
            pass


app = Application()
pyglet.app.run()
