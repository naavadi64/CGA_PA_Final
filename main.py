from GameObject import *

bg = ImageObject("resource/spongy_wired.jpg")
sprsht = ImageObject("resource/spritesheet.png")
sprmask = ImageObject("resource/spritesheet_mask.png")
wire_sponge = WireSponge(Vector(800, 480))
img_draw = bg
img_display = pyglet.image.ImageData(
    img_draw.width,
    img_draw.height,
    'RGB',
    img_draw.get_bytes(),
    img_draw.pitch
)


def initialize_sprite():
    SpongeIdle = FrameCollection(SpongeState.idle)
    SpongeIdle.insert(Frame(82, 137, 26, 85, Vector(108, 58), 1))

    # Intro
    SpongeIntroChainFall = FrameCollection(SpongeState.introChainFall)
    SpongeIntroChainFallEnd = FrameCollection(SpongeState.introChainFallEnd)
    SpongeIntroSpin = FrameCollection(SpongeState.introSpin)
    SpongeIntroCharge = FrameCollection(SpongeState.introCharge)

    SpongeIntroChainFall.insert(Frame(218, 268, 100, 169, Vector(250, 133), 1))
    SpongeIntroChainFallEnd.insert(Frame(4, 63, 23, 86, Vector(38, 57), 1))
    SpongeIntroChainFallEnd.insert(Frame(82, 137, 26, 85, Vector(108, 58), 1))
    SpongeIntroSpin.insert(Frame(498, 549, 12, 80, Vector(524, 53), 1))
    SpongeIntroSpin.insert(Frame(221, 285, 19, 84, Vector(260, 57), 1))
    SpongeIntroSpin.insert(Frame(288, 254, 25, 84, Vector(329, 57), 1))
    SpongeIntroSpin.insert(Frame(149, 215, 26, 85, Vector(189, 58), 1))
    SpongeIntroSpin.insert(Frame(426, 490, 21, 80, Vector(465, 53), 1))
    SpongeIntroSpin.insert(Frame(365, 418, 23, 82, Vector(393, 55), 1))
    SpongeIntroSpin.insert(Frame(551, 603, 21, 80, Vector(578, 53), 1))
    SpongeIntroCharge.insert(Frame(83, 136, 27, 84, Vector(110, 57), 1))
    SpongeIntroCharge.insert(Frame(83, 136, 27, 84, Vector(110, 57), 1))
    SpongeIntroCharge.insert(Frame(83, 136, 27, 84, Vector(110, 57), 1))

    wire_sponge.insert(SpongeIdle)
    wire_sponge.insert(SpongeIntroChainFall)
    wire_sponge.insert(SpongeIntroChainFallEnd)
    wire_sponge.insert(SpongeIntroSpin)
    wire_sponge.insert(SpongeIntroCharge)


def put_sprite(character):
    img_draw = bg
    frame = character.sprites[character.spritesId].frames[character.frameId]
    sprite_width = frame.xRight - frame.xLeft
    sprite_height = frame.yBottom - frame.yTop

    if character.facing.left:
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


def display_img():
    put_sprite(wire_sponge)
    img_display.set_data(
        'RGB',
        img_draw.pitch,
        img_draw.get_bytes()
    )
    img_display.blit(0,0)


class CGA(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=bg.width, height=bg.height, visible=True)
        initialize_sprite()
        pyglet.clock.schedule_interval(self.update, 0.5)

    def on_draw(self):
        pass

    def update(self, dt):
        self.clear()
        wire_sponge.update()
        display_img()

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass


cga = CGA()
pyglet.app.run()
