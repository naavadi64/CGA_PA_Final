import imgui
import imgui.core
from imgui.integrations.pyglet import PygletRenderer

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
        pyglet.clock.schedule_interval(self.update, 1/60)
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
        pass

    def on_key_release(self, symbol, modifiers):
        pass


app = Application()
pyglet.app.run()
