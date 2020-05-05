import imgui
import imgui.core
import math
from copy import copy
from imgui.integrations.pyglet import PygletRenderer
from pyglet.window import key, mouse
from GameObject import *

bg = ImageObject("resource/spongy_wired.jpg")
sprsht = ImageObject("resource/spritesheet.png")
sprmask = ImageObject("resource/spritesheet_mask.png")
dummy_sprsht = ImageObject("resource/dummy_spritesheet.bmp")
dummy_sprmask = ImageObject("resource/dummy_spritesheet_mask.bmp")
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
    def auto_anchor(left, right, top, bottom):  # calculates anchor as midpoints of x and y, rounded up
        x = math.ceil(((right - left) / 2) + left)
        y = math.ceil(((top - bottom) / 2) + top)
        return x, y

    # ----Wire Sponge----
    # Idle
    SpongeIdle = FrameCollection(SpongeState.idle)
    ChainIdle = FrameCollection(ChainState.idle)
    ChainIdle.insert(Frame(0, 0, 0, 0, Vector(0, 0), 1))
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
    # Horizontal
    SpongeChainHrzBegin = FrameCollection(SpongeState.throwHrzBegin)
    ChainThrowHrz = FrameCollection(ChainState.thrownH)
    SpongeChainHrz = FrameCollection(SpongeState.throwHrz)
    SpongeChainHrzPullStay = FrameCollection(SpongeState.throwHrzPullStay)
    ChainHrzPullStay = FrameCollection(ChainState.pullStayH)
    ChainHrzPullGo = FrameCollection(ChainState.pullGoH)
    SpongeChainHrzPullGo = FrameCollection(SpongeState.throwHrzPullGo)
    SpongeChainHrzRelease = FrameCollection(SpongeState.throwHrzRelease)

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
    SpongeChainHrzPullGo.insert(Frame(797, 841, 114, 169, Vector(819, 144), 1, fist_position=Vector(800, 136)))
    ChainHrzPullGo.insert(Frame(312, 330, 504, 518, Vector(321, 511), 1))
    SpongeChainHrzRelease.insert(Frame(926, 960, 113, 168, Vector(948, 143), 2, fist_position=Vector(929, 135)))
    SpongeChainHrzRelease.insert(Frame(850, 885, 116, 165, Vector(872, 146), 2, fist_position=Vector(853, 138)))
    SpongeChainHrzRelease.insert(Frame(897, 922, 117, 167, Vector(910, 148), 4, fist_position=Vector(901, 140)))
    SpongeChainHrzRelease.insert(Frame(850, 885, 116, 165, Vector(872, 146), 2, fist_position=Vector(853, 138)))
    SpongeChainHrzRelease.insert(Frame(926, 960, 113, 168, Vector(948, 143), 2, fist_position=Vector(929, 135)))

    # Vertical
    SpongeChainVrtBegin = FrameCollection(SpongeState.throwVrtBegin)
    SpongeChainVrt = FrameCollection(SpongeState.throwVrt)
    ChainThrowVrt = FrameCollection(ChainState.thrownV)
    SpongeChainVrtPull = FrameCollection(SpongeState.throwVrtPull)
    ChainVrtPull = FrameCollection(ChainState.pullV)
    SpongeChainSeedBegin = FrameCollection(SpongeState.seedBegin)
    SpongeChainSeedEnd = FrameCollection(SpongeState.seedEnd)
    Seed = FrameCollection(SeedWineState.seed)
    WineVrtLeft = FrameCollection(SeedWineState.vrtLeft)
    WineVrtRight = FrameCollection(SeedWineState.vrtRight)
    WineHrzLeft = FrameCollection(SeedWineState.hrzLeft)
    WineHrzRight = FrameCollection(SeedWineState.hrzRight)

    SpongeChainVrtBegin.insert(Frame(730, 789, 22, 80, Vector(753, 56), 4))
    SpongeChainVrtBegin.insert(Frame(798, 848, 22, 80, Vector(823, 54), 2))
    SpongeChainVrtBegin.insert(Frame(4, 63, 23, 86, Vector(41, 57), 1, fist_position=Vector(48, 29)))
    SpongeChainVrt.insert(Frame(4, 63, 23, 86, Vector(41, 57), 1, fist_position=Vector(48, 29)))
    ChainThrowVrt.insert(Frame(986, 1001, 5, 21, Vector(993, 13), 1))
    SpongeChainVrtPull.insert(Frame(218, 268, 100, 169, Vector(250, 133), 1, fist_position=Vector(259, 103)))
    ChainVrtPull.insert(Frame(986, 1001, 5, 21, Vector(993, 13), 1))
    SpongeChainSeedBegin.insert(Frame(160, 207, 101, 169, Vector(190, 135), 2, fist_position=Vector(199, 105),
                                      head_position=Vector(192, 113)))
    SpongeChainSeedBegin.insert(Frame(851, 898, 15, 83, Vector(881, 49), 2, fist_position=Vector(890, 19)))
    SpongeChainSeedBegin.insert(Frame(105, 152, 104, 172, Vector(135, 138), 2, fist_position=Vector(144, 107)))
    SpongeChainSeedBegin.insert(Frame(1, 58, 111, 168, Vector(33, 142), 4, fist_position=Vector(43, 115)))
    SpongeChainSeedBegin.insert(Frame(58, 102, 97, 170, Vector(88, 135), 1, fist_position=Vector(97, 101),
                                      head_position=Vector(90, 111)))
    SpongeChainSeedEnd.insert(Frame(58, 102, 97, 170, Vector(88, 135), 1, fist_position=Vector(97, 101),
                                    head_position=Vector(90, 111)))
    SpongeChainSeedEnd.insert(Frame(105, 152, 104, 172, Vector(135, 138), 2, fist_position=Vector(144, 107)))
    SpongeChainSeedEnd.insert(Frame(851, 898, 15, 83, Vector(881, 49), 2, fist_position=Vector(890, 19)))
    SpongeChainSeedEnd.insert(Frame(160, 207, 101, 169, Vector(190, 135), 2, fist_position=Vector(199, 105),
                                    head_position=Vector(192, 113)))
    Seed.insert(Frame(757, 766, 333, 342, Vector(761, 337), 1))
    WineHrzLeft.insert(Frame(786, 802, 328, 350, Vector(794, 339), 1))
    WineHrzRight.insert(Frame(876, 892, 331, 353, Vector(884, 342), 1))
    WineVrtLeft.insert(Frame(883, 905, 355, 371, Vector(894, 363), 1))
    WineVrtRight.insert(Frame(859, 882, 355, 371, Vector(870, 363), 1))

    # Thunder Dance - 26, 25
    SpongeDance = FrameCollection(SpongeState.dance)

    SpongeDance.insert(30, 85, 217, 271, Vector(56, 246), 1)
    SpongeDance.insert(93, 148, 220, 271, Vector(119, 246), 1)
    SpongeDance.insert(154, 207, 217, 271, Vector(180, 246), 1)
    SpongeDance.insert(220, 276, 222, 271, Vector(246, 246), 1)
    SpongeDance.insert(286, 339, 213, 271, Vector(260, 246), 1)
    SpongeDance.insert(350, 403, 203, 271, Vector(324, 246), 1)
    SpongeDance.insert(408, 461, 201, 271, Vector(382, 246), 1)
    SpongeDance.insert(473, 527, 191, 271, Vector(499, 246), 1)
    SpongeDance.insert(543, 596, 188, 271, Vector(517, 246), 1)
    SpongeDance.insert(604, 657, 187, 271, Vector(578, 246), 1)
    SpongeDance.insert(669, 722, 187, 271, Vector(643, 246), 1)
    SpongeDance.insert(734, 787, 202, 271, Vector(708, 246), 1)
    SpongeDance.insert(853, 907, 200, 271, Vector(827, 246), 1)
    SpongeDance.insert(18, 67, 288, 346, Vector(46, 321), 1)
    SpongeDance.insert(72, 142, 286, 346, Vector(98, 321), 1)
    SpongeDance.insert(147, 217, 300, 346, Vector(173, 321), 1)
    SpongeDance.insert(224, 279, 297, 346, Vector(250, 321), 1)
    SpongeDance.insert(285, 338, 293, 346, Vector(311, 321), 1)
    SpongeDance.insert(342, 395, 286, 346, Vector(368, 321), 1)
    SpongeDance.insert(405, 458, 288, 346, Vector(431, 321), 1)
    SpongeDance.insert(460, 513, 287, 346, Vector(486, 321), 1)
    SpongeDance.insert(520, 573, 287, 346, Vector(546, 321), 1)
    SpongeIdle.insert(Frame(82, 137, 26, 85, Vector(108, 60), 1))

    # Initializing the sprites
    # Idle
    wire_sponge.insert(SpongeIdle)
    wire_sponge.chain.insert(ChainIdle)
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
    wire_sponge.insert(SpongeChainHrzPullGo)
    wire_sponge.chain.insert(ChainHrzPullGo)
    wire_sponge.insert(SpongeChainHrzRelease)
    # Throw chain Vertical
    wire_sponge.insert(SpongeChainVrtBegin)
    wire_sponge.insert(SpongeChainVrt)
    wire_sponge.chain.insert(ChainThrowVrt)
    wire_sponge.insert(SpongeChainVrtPull)
    wire_sponge.chain.insert(ChainVrtPull)
    wire_sponge.insert(SpongeChainSeedBegin)
    wire_sponge.seed_wine_clone.insert(Seed)
    wire_sponge.seed_wine_clone.insert(WineVrtRight)
    wire_sponge.seed_wine_clone.insert(WineVrtLeft)
    wire_sponge.seed_wine_clone.insert(WineHrzRight)
    wire_sponge.seed_wine_clone.insert(WineHrzLeft)
    wire_sponge.insert(SpongeChainSeedEnd)
    # Setting initial state
    wire_sponge.setState(SpongeState.introChainFall)
    wire_sponge.chain.setState(ChainState.fallIntro)

    # ----Dummy---- Class, States, timing Unfinished(?)

    # Idle
    DummyIdle = FrameCollection(DummyState.idle)
    DummyIdle.insert(Frame(208, 239, 15, 49, Vector(224, 32), 1))  # 8

    # Intro/Spawn
    DummySpawn = FrameCollection(DummyState.spawn)

    DummySpawn.insert(Frame(0, 9, 0, 50, Vector(5, 32), 1))
    DummySpawn.insert(Frame(12, 35, 19, 50, Vector(24, 32), 1))
    DummySpawn.insert(Frame(38, 69, 7, 50, Vector(54, 32), 1))
    DummySpawn.insert(Frame(72, 103, 10, 50, Vector(88, 32), 1))
    DummySpawn.insert(Frame(106, 137, 13, 50, Vector(122, 32), 1))
    DummySpawn.insert(Frame(140, 169, 15, 50, Vector(156, 32), 1))
    DummySpawn.insert(Frame(174, 205, 17, 50, Vector(190, 32), 1))
    DummySpawn.insert(Frame(208, 239, 15, 50, Vector(224, 32), 1))  # 8, End on idle

    # Walk Cycle - Note: retain y values from first frame for anchor to avoid vertical position weirdness
    DummyWalk = FrameCollection(DummyState.walk)

    DummyWalk.insert(Frame(314, 345, 15, 50, Vector(330, 32), 1))  # 11
    DummyWalk.insert(Frame(345, 366, 15, 50, Vector(361, 32), 1))  # 12
    DummyWalk.insert(Frame(366, 390, 14, 50, Vector(382, 32), 1))  # 13
    DummyWalk.insert(Frame(389, 422, 15, 50, Vector(405, 32), 1))  # 14
    DummyWalk.insert(Frame(421, 456, 16, 50, Vector(437, 32), 1))  # 15
    DummyWalk.insert(Frame(455, 482, 16, 50, Vector(471, 32), 1))  # 16
    DummyWalk.insert(Frame(484, 507, 15, 50, Vector(500, 32), 1))  # 17
    DummyWalk.insert(Frame(506, 532, 14, 50, Vector(522, 32), 1))  # 18
    DummyWalk.insert(Frame(534, 565, 15, 50, Vector(550, 32), 1))  # 19
    DummyWalk.insert(Frame(565, 600, 16, 50, Vector(581, 32), 1))  # 20
    DummyWalk.insert(Frame(599, 628, 16, 50, Vector(615, 32), 1))  # 21, go back to 12
    DummyWalk.insert(Frame(345, 366, 15, 50, Vector(361, 32), 1))  # 12
    DummyWalk.insert(Frame(366, 390, 14, 50, Vector(382, 32), 1))  # 13
    DummySpawn.insert(Frame(208, 239, 14, 50, Vector(224, 32), 1))  # 8, End on idle

    # Attack (Standing) - Anchor based on idle sprite's dX (16), dY (18) from left, bottom
    DummyAttack = FrameCollection(DummyState.attack)

    DummyAttack.insert(Frame(0, 32, 163, 198, Vector(16, 181), 1))  # 1, Start
    DummyAttack.insert(Frame(36, 66, 163, 198, Vector(52, 181), 1))  # 2, Recoil
    DummyAttack.insert(Frame(0, 32, 163, 198, Vector(16, 18), 1))  # 1, Reset

    # Stagger - Anchor based on idle sprite's dX (16), dY (18) from left, bottom
    DummyStagger = FrameCollection(DummyState.stagger)

    DummyStagger.insert(Frame(4, 32, 312, 349, Vector(20, 331), 1))  # 1, Start
    DummyStagger.insert(Frame(34, 64, 314, 349, Vector(50, 331), 1))  # 2, Knockback
    DummyStagger.insert(Frame(4, 32, 312, 349, Vector(20, 331), 1))  # 1, Recover & reset

    # Electrocuted - Follow anchor of start sprite
    DummyElec = FrameCollection(DummyState.electrocuted)

    DummyElec.insert(Frame(4, 32, 312, 349, Vector(20, 331), 1))  # 1, Start
    DummyElec.insert(Frame(34, 64, 314, 349, Vector(50, 331), 1))  # 2
    DummyElec.insert(Frame(67, 97, 315, 349, Vector(91, 331), 1))  # 3
    DummyElec.insert(Frame(100, 133, 304, 353, Vector(117, 331), 1))  # 4
    DummyElec.insert(Frame(134, 164, 314, 349, Vector(150, 331), 1))  # 5
    DummyElec.insert(Frame(167, 200, 304, 353, Vector(153, 331), 1))  # 6
    DummyElec.insert(Frame(202, 232, 314, 349, Vector(218, 331), 1))  # 7
    DummyElec.insert(Frame(235, 268, 304, 353, Vector(251, 331), 1))  # 8
    DummyElec.insert(Frame(270, 302, 314, 331, Vector(286, 331), 1))  # 9
    DummyElec.insert(Frame(34, 64, 314, 349, Vector(50, 331), 1))  # 2
    DummyElec.insert(Frame(4, 32, 312, 349, Vector(20, 331), 1))  # 1

    # Explode
    DummyExplode = FrameCollection(DummyState.explode)

    DummyExplode.insert(Frame(204, 219, 437, 452, Vector(211, 434), 1))
    DummyExplode.insert(Frame(199, 224, 405, 430, Vector(211, 412), 1))
    DummyExplode.insert(Frame(204, 219, 437, 452, Vector(211, 434), 1))


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
                if spriteTop + j <= 0 or spriteLeft + i <= 0:
                    continue
                img_draw.set_pixel_bytearray(
                    spriteLeft + i, spriteTop + j,
                    ANDwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft + i, spriteTop + j),
                        sprmask.get_pixel_bytearray(frame.xLeft + i, frame.yTop + j)
                    )
                )

        for i in range(sprite_width):
            for j in range(sprite_height):
                if spriteTop + j <= 0 or spriteLeft + i <= 0:
                    continue
                img_draw.set_pixel_bytearray(
                    spriteLeft + i, spriteTop + j,
                    ORwPixelByte(
                        img_draw.get_pixel_bytearray(spriteLeft + i, spriteTop + j),
                        sprsht.get_pixel_bytearray(frame.xLeft + i, frame.yTop + j)
                    )
                )
    else:
        spriteLeft = character.position.x + frame.anchor.x - frame.xRight
        spriteTop = character.position.y - frame.anchor.y + frame.yTop
        for i in range(sprite_width):
            for j in range(sprite_height):
                if spriteTop + j <= 0 or spriteLeft + i <= 0:
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
                if spriteTop + j <= 0 or spriteLeft + i <= 0:
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
    for seed in wire_sponge.seed_wines:
        put_sprite(seed)
    img_display.set_data(
        'RGB',
        img_draw.pitch,
        img_draw.get_bytes()
    )
    img_display.blit(0, 0)


class Interface:  # --UI and Controls--
    def __init__(self, window):
        imgui.create_context()
        self.impl = PygletRenderer(window)
        imgui.new_frame()  # Required since on call, imgui needs to render once
        imgui.end_frame()

        # --Imgui Window Variables--
        # --Format: Window Boolean followed by its variables, separate each window with one end line.
        self.showPlayerControls = True  #

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
            imgui.text("Current State:")
            imgui.text(wire_sponge.curState.name)
            imgui.new_line()

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
                if wire_sponge.chain.curState == ChainState.NaN \
                        and wire_sponge.curState != SpongeState.throwHrz \
                        and wire_sponge.curState != SpongeState.throwHrzRelease \
                        and wire_sponge.curState != SpongeState.throwHrzPullGo:
                    wire_sponge.setState(SpongeState.throwHrzBegin)
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
            imgui.text("Z:          Thunder Dance")
            imgui.text("X:          Spin Chain")
            imgui.text("C:          Attack")
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
        pyglet.clock.schedule_interval(self.update, 1 / 30)
        self.interface = Interface(self)  # UI class call, check Controls class

    def on_draw(self):
        pass

    def update(self, dt):
        self.clear()
        wire_sponge.update()
        wire_sponge.chain.update()
        for seed in wire_sponge.seed_wines:
            seed.update()
        display_img()
        self.interface.render()

    '''
    Controls:
    Arrow key left:     Turn/Move Left
    Arrow key right:    Turn/Move Right
    Arrow key up:       Look up (Contextual) 
    Arrow key down:     Look down (Contextual) 
    Space:              Jump/Leap
    Z:                  Thunder Dance
    X:                  Spin Chain
    C:                  Attack with chain (Left/Right)
    V:                  Attack with chain (Up)
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

        elif symbol == key.Z:
            pass

        elif symbol == key.X and wire_sponge.on_ground and wire_sponge.curState != SpongeState.spin:
            wire_sponge.setState(SpongeState.spin)

        elif symbol == key.C and wire_sponge.chain.curState == ChainState.NaN and not wire_sponge.using_chain:
            wire_sponge.setState(SpongeState.throwHrzBegin)

        elif symbol == key.V and wire_sponge.chain.curState == ChainState.NaN and not wire_sponge.using_chain \
                and wire_sponge.on_ground:
            wire_sponge.setState(SpongeState.throwVrtBegin)

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
