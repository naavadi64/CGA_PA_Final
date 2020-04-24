import pyglet
from enum import Enum


class Color:
    '''
    Class color. Perlu dijelasin? RGB.
    '''
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Vector:
    '''
        Vector bisa dijadikan point ataupun velocity
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y


def ANDColor(color1, color2):
    '''
    Bitwise operation antara dua warna tiap channel warnanya (RGB)
    :param color1: color 1 sesuai class GameObject.Color
    :param color2: color 2 yang ingin di bitwise sesuai class GameObject.Color
    :return: satu color yang udah di bitwise AND
    '''
    clr = Color(0,0,0)
    clr.r = color1.r & color2.r
    clr.g = color1.g & color2.g
    clr.b = color1.b & color2.b
    return clr


def ANDwPixelByte(pxlb_1, pxlb_2):
    '''
    Bitwise operation antara dua data pixel (bisa dibilang warna) dalam bentuk bytes. Data bisa lebih dari satu pixel
    yang dicompare. Contoh: satu string bytes yang mempresentasikan sebuah gambar atau garis, di bitwise dengan pixel
    byte lainnya tergantung size siapa yang lebih kecil.
    :param pxlb_1: data bytes pixel RBB order. Bisa lebih dari satu.
    :param pxlb_2: data bytes pixel RGB order yang ingin di bitwise. Bisa lebih dari satu.
    :return: satu data pixel (3 bytes) jika kedua param cuma satu pixel juga. > 3 bytes jika banyak.
    '''
    pxlb = bytes()
    if len(pxlb_1) <= len(pxlb_2):
        for i in range(len(pxlb_1)):
            pxlb += bytes([pxlb_1[i] & pxlb_2[i]])
    else:
        for i in range(len(pxlb_2)):
            pxlb += bytes([pxlb_2[i] & pxlb_1[i]])
    return pxlb


def ORColor(color1, color2):
    '''
    Bitwise operation antara dua warna tiap channel warnanya (RGB)
    :param color1: color 1 sesuai class GameObject.Color
    :param color2: color 2 yang ingin di bitwise sesuai class GameObject.Color
    :return: satu color yang udah di bitwise OR
    '''
    clr = Color(0,0,0)
    clr.r = color1.r | color2.r
    clr.g = color1.g | color2.g
    clr.b = color1.b | color2.b
    return clr


def ORwPixelByte(pxlb_1, pxlb_2):
    '''
    Bitwise operation antara dua data pixel (bisa dibilang warna) dalam bentuk bytes. Data bisa lebih dari satu pixel
    yang dicompare. Contoh: satu string bytes yang mempresentasikan sebuah gambar atau garis, di bitwise dengan pixel
    byte lainnya tergantung size siapa yang lebih kecil.
    :param pxlb_1: data bytes pixel RBB order. Bisa lebih dari satu.
    :param pxlb_2: data bytes pixel RGB order yang ingin di bitwise. Bisa lebih dari satu.
    :return: satu data pixel (3 bytes) jika kedua param cuma satu pixel juga. > 3 bytes jika banyak.
    '''
    pxlb = bytes()
    if len(pxlb_1) <= len(pxlb_2):
        for i in range(len(pxlb_1)):
            pxlb += bytes([pxlb_1[i] | pxlb_2[i]])
    else:
        for i in range(len(pxlb_2)):
            pxlb += bytes([pxlb_2[i] | pxlb_1[i]])
    return pxlb


class CharState(Enum):
    '''
    State buat karakter biasa atau pun dummy
    '''
    idle = 0
    walk = 1
    leapBegin = 10
    leap = 11
    leapEnd = 12


class DummyState(Enum):
    '''
    State untuk dummy
    '''
    pass


class SpongeState(Enum):
    '''
    State khusus untuk Wire Sponge
    '''
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


class Facing(Enum):
    '''
    Arah pandangan karakter, kanan atau kiri
    '''
    left = 5
    right = 6


class ImageObject:
    '''
    Sebuah raw image yang dibuat untuk load background, spritesheet, dsb. Koordinat raw image dimulai dari TOP-LEFT yang
    berbeda dengan koordinat screen pyglet BOTTOM-LEFT. Don't get confused in practice.
    '''
    def __init__(self, path):
        '''
        Constructor untuk initialize raw image baru dengan path dan filename yang tersedia.
        :param path: Filename in current directory or full path with filename
        '''
        self.path = path
        try:
            img = pyglet.image.load(filename=path).get_image_data()
            self.width = img.width
            self.height = img.height
            self.pitch = -self.width * len('RGB')  # Number of bytes per row
            self.data = img.get_data(fmt='RGB', pitch=self.pitch)  # Pixels bytes data
        except FileNotFoundError:
            print("File not succesfully loaded")
            exit()

    def get_color(self, x, y, width=0, height=0):
        '''
        Ambil color dengan koordinat image yang ditentukan. Kalau ingin mengambil dalam satu area kotak/garis, width dan
        height harus ditentukan
        :param x: koordinat x dari LEFT
        :param y: koordinat y dari TOP
        :param width: panjang area jika perlu satu Kotak (Rectangle)
        :param height: lebar area jika perlu satu Kotak (Rectangle)
        :return: satu color jika width dan height tidak di specified. Array of color jika di specified.
        '''
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
        '''
        Ambil color dalam bentuk bytes of pixels dengan koordinat image yang ditentukan. Kalau ingin mengambil dalam
        satu area kotak/garis, width dan height harus ditentukan
        :param x: koordinat x dari LEFT
        :param y: koordinat y dari TOP
        :param width: panjang area jika perlu satu Kotak (Rectangle)
        :param height: lebar area jika perlu satu Kotak (Rectangle)
        :return: string bytes of pixel (size-nya kelipatan 3, RGB)
        '''
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
        '''
        Taruh warna di koordinat yang ditentukan. Bisa mengubah satu area yang ditentukan width dan height nya
        :param x: koordinat x dari LEFT
        :param y: koordinat y dari TOP
        :param color: warna yang ingin ditaruh sesuai class GameObject.Color
        :param width: panjang area jika perlu satu area Kotak (Rectangle)
        :param height: lebar area jika perlu satu area Kotak (Rectangle)
        :return: tidak ada, void
        '''
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


class Frame:
    '''
    Frame bertindak seperti grid yang memotong dan memisahkan pada bagian image untuk sprite yang akan di apply.
    '''
    def __init__(self, xLeft, xRight, yTop, yBottom, anchor, time_framing):
        '''

        :param xLeft:
        :param xRight:
        :param yTop:
        :param yBottom:
        :param anchor:
        :param time_framing:
        '''
        self.xLeft = xLeft
        self.xRight = xRight
        self.yTop = yTop
        self.yBottom = yBottom
        self.anchor = anchor
        self.id = None
        self.time_framing = time_framing


class FrameCollection:
    '''
    Bertindak sebagai penampung Frames. Dipakai sebagai set frame karena akan dianimasikan sesuai state karakternya
    '''
    def __init__(self):
        self.frames = []
        self.num_frame = len(self.frames)

    def insert(self, frame):
        '''
        memasukkan frame baru tanpa menghapus yang ada.
        :param frame: frame, sesuai class GameObject.Frame
        :return: tidak ada, void
        '''
        self.frames.append(frame)
        self.num_frame = len(self.frames)


class Character:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(0,0)
        self.curState = CharState.idle
        self.frameId = 0
        self.curFrame = 0
        self.sprites = []       # Frame collection
        self.spritesId = 0
        self.facing = Facing.right

    def setState(self, state, sprId):
        self.curState = state
        self.spritesId = sprId
        self.curFrame = 0
        self.frameId = 0

    def nextFrame(self):
        self.curFrame += 1
        if self.curFrame == self.sprites[self.spritesId].frames[self.frameId].framing_time:
            self.frameId += 1
            if self.frameId == self.sprites[self.spritesId].num_frame:
                self.frameId = 0
            self.curFrame = 0

    def update(self):
        pass  # ini untuk karakter biasa/dummy/whatever, disini buat skema nya sesuai finite machine (FSM) karakternya


class WireSponge(Character):
    def __init__(self, position):
        super().__init__(position)
        self.curState = SpongeState.idle

    def update(self):
        pass # disini buat sesuai FSM karakter si sponge nya

