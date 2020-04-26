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
    SpongeIdle.insert(
        Frame(
            83, 136, 27, 84,
            Vector(110, 57),
            1
        )
    )
    wire_sponge.insert(SpongeIdle)


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


def update(dt):
    wire_sponge.update()
    display_img()


class CGA(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=bg.width, height=bg.height, visible=True)

    def on_draw(self):
        self.clear()
        wire_sponge.update()
        display_img()


initialize_sprite()
pyglet.clock.schedule_interval(update, 0.5)
cga = CGA()
pyglet.app.run()
