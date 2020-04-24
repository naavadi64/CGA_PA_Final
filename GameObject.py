import pyglet
from enum import Enum


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def ANDColor(color1, color2):
    clr = Color(0,0,0)
    clr.r = color1.r & color2.r
    clr.g = color1.g & color2.g
    clr.b = color1.b & color2.b
    return clr


def ANDwPixelByte(pxlb_1, pxlb_2):
    pxlb = bytes()
    if len(pxlb_1) <= len(pxlb_2):
        for i in range(len(pxlb_1)):
            pxlb += bytes([pxlb_1[i] & pxlb_2[i]])
    else:
        for i in range(len(pxlb_2)):
            pxlb += bytes([pxlb_2[i] & pxlb_1[i]])
    return pxlb


def ORColor(color1, color2):
    clr = Color(0,0,0)
    clr.r = color1.r | color2.r
    clr.g = color1.g | color2.g
    clr.b = color1.b | color2.b
    return clr


def ORwPixelByte(pxlb_1, pxlb_2):
    pxlb = bytes()
    if len(pxlb_1) <= len(pxlb_2):
        for i in range(len(pxlb_1)):
            pxlb += bytes([pxlb_1[i] | pxlb_2[i]])
    else:
        for i in range(len(pxlb_2)):
            pxlb += bytes([pxlb_2[i] | pxlb_1[i]])
    return pxlb


class SpongeState(Enum):
    idle = 0
    walk = 1
    leapBegin = 10
    leap = 11
    leapEnd = 12
    throwHrzBegin = 200
    throwHrz = 201
    throwHrzEnd = 202
    spinBegin = 100
    spin = 101
    spinEnd = 102
    faceLeft = 5
    faceRight = 6


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

    def get_color(self, x, y, width=0, height=0):
        if x >= self.width:
            x = self.width - 1
        if y >= self.height:
            y = self.height - 1
        idx = y * self.width + x
        idx *= 3
        if width == 0 and height == 0:
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

    def get_pixel_bytes(self, x, y, width=0, height=0):
        if x >= self.width:
            x = self.width - 1
        if y >= self.height:
            y = self.height - 1
        idx = y * self.width + x
        idx *= 3
        if width == 0 and height == 0:
            return bytes([self.data[idx], self.data[idx + 1], self.data[idx + 2]])
        pxl = bytes()
        for j in range(height):
            for i in range(width):
                try:
                    pxl += bytes([self.data[idx], self.data[idx + 1], self.data[idx + 2]])
                except IndexError:
                    return pxl
                idx += 3
        return pxl

    def set_color(self, x, y, color, width=0, height=0):
        if x >= self.width:
            x = self.width - 1
        if y >= self.height:
            y = self.height - 1
        idx = y * self.width + x
        idx *= 3
        if width == 0 and height == 0:
            self.data[idx] = bytes([color.r])
            self.data[idx + 1] = bytes([color.g])
            self.data[idx + 2] = bytes([color.b])
            return
        for j in range(height):
            for i in range(width):
                try:
                    self.data[idx] = bytes([color.r])
                    self.data[idx + 1] = bytes([color.g])
                    self.data[idx + 2] = bytes([color.b])
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
        self.id = None
        self.time_framing = time_framing


class SpriteCollection:
    def __init__(self):
        self.sprites = []
        self.num_frame = len(self.sprites)

    def insert(self, sprite):
        self.sprites.append(sprite)
        self.num_frame = len(self.sprites)


class Character:
    def __init__(self):
