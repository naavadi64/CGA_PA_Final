import pyglet


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class ImageObject:
    def __init__(self, path):
        self.path = path
        try:
            img = pyglet.image.load(filename=path).get_image_data()
            self.width = img.width
            self.height = img.height
            self.pitch = self.width * len('RGB')
            self.data = img.get_data(fmt='RGB', pitch=self.pitch)

        except FileNotFoundError:
            print("File not succesfully loaded")
            exit()

    def get_color(self, x, y):
        idx = y * self.width + x
        return Color(self.data[idx], self.data[idx+1], self.data[idx+2])