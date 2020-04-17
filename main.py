import pyglet


class CGA(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=512, height=512, visible=True)
        self.label = pyglet.text.Label('Hello, world',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.label.draw()


cga = CGA()
pyglet.app.run()