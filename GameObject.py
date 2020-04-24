import pyglet


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ImageObject:
    def __init__(self, path):
        self.path = path
        try:
            img = pyglet.image.load(filename=path).get_image_data()
            self.width = img.width
            self.height = img.height
            self.pitch = -self.width * len('RGB')
            self.data = img.get_data(fmt='RGB', pitch=self.pitch)

        except FileNotFoundError:
            print("File not succesfully loaded")
            exit()

    def get_color(self, x, y, width=None, height=None):
        if x >= self.width:
            x = self.width - 1
        if y >= self.height:
            y = self.height - 1
        idx = y * self.width + x
        idx *= 3
        if width is None and height is None:
            return Color(self.data[idx], self.data[idx + 1], self.data[idx + 2])
        clr = []
        for j in range(height):
            for i in range(width):
                try:
                    clr.append(Color(self.data[idx], self.data[idx + 1], self.data[idx + 2]))
                except IndexError:
                    return clr
                idx += 3
        return clr

    def set_color(self, x, y, color, width=None, height=None):
        if x >= self.width:
            x = self.width - 1
        if y >= self.height:
            y = self.height - 1
        idx = y * self.width + x
        idx *= 3
        if width is None and height is None:
            self.data[idx] = color.r
            self.data[idx + 1] = color.g
            self.data[idx + 2] = color.b
            return
        for j in range(height):
            for i in range(width):
                try:
                    self.data[idx] = color.r
                    self.data[idx + 1] = color.g
                    self.data[idx + 2] = color.b
                except IndexError:
                    return
                idx += 3


class Sprite:
    def __init__(self, xLeft, xRight, yTop, yBottom, anchor, time_framing):
        self.xLeft = xLeft
        self.xRight = xRight
        self.yTop = yTop
        self.yBottom = yBottom
        self.anchor = anchor
        self.time_framing = time_framing


class SpriteCollection:
    def __init__(self):
        self.sprites = []
        self.num_frame = len(self.sprites)

    def insert(self, sprite):
        self.sprites.append(sprite)
        self.num_frame = len(self.sprites)
