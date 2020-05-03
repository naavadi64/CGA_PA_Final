import pyglet
from enum import Enum


class Color:
    """
    Class color. Perlu dijelasin? RGB.
    """

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Vector:
    """
        Vector bisa dijadikan point ataupun velocity
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


def ANDColor(color1, color2):
    """
    Bitwise operation antara dua warna tiap channel warnanya (RGB)
    :param color1: color 1 sesuai class GameObject.Color
    :param color2: color 2 yang ingin di bitwise sesuai class GameObject.Color
    :return: satu color yang udah di bitwise AND
    """
    clr = Color(0, 0, 0)
    clr.r = color1.r & color2.r
    clr.g = color1.g & color2.g
    clr.b = color1.b & color2.b
    return clr


def ANDwPixelByte(pxlb_1, pxlb_2):
    """
    Bitwise operation antara dua data pixel (bisa dibilang warna) dalam bentuk bytearray. Data bisa lebih dari satu pixel
    yang dicompare. Contoh: satu string bytearray yang mempresentasikan sebuah gambar atau garis, di bitwise dengan pixel
    byte lainnya tergantung size siapa yang lebih kecil.
    :param pxlb_1: data bytearray pixel RBB order. Bisa lebih dari satu.
    :param pxlb_2: data bytearray pixel RGB order yang ingin di bitwise. Bisa lebih dari satu.
    :return: satu data pixel (3 bytearray) jika kedua param cuma satu pixel juga. > 3 bytearray jika banyak.
    """
    pxlb = bytearray()
    if len(pxlb_1) <= len(pxlb_2):
        for i in range(len(pxlb_1)):
            pxlb += bytearray([pxlb_1[i] & pxlb_2[i]])
    else:
        for i in range(len(pxlb_2)):
            pxlb += bytearray([pxlb_2[i] & pxlb_1[i]])
    return pxlb


def ORColor(color1, color2):
    """
    Bitwise operation antara dua warna tiap channel warnanya (RGB)
    :param color1: color 1 sesuai class GameObject.Color
    :param color2: color 2 yang ingin di bitwise sesuai class GameObject.Color
    :return: satu color yang udah di bitwise OR
    """
    clr = Color(0, 0, 0)
    clr.r = color1.r | color2.r
    clr.g = color1.g | color2.g
    clr.b = color1.b | color2.b
    return clr


def ORwPixelByte(pxlb_1, pxlb_2):
    """
    Bitwise operation antara dua data pixel (bisa dibilang warna) dalam bentuk bytearray. Data bisa lebih dari satu pixel
    yang dicompare. Contoh: satu string bytearray yang mempresentasikan sebuah gambar atau garis, di bitwise dengan pixel
    byte lainnya tergantung size siapa yang lebih kecil.
    :param pxlb_1: data bytearray pixel RBB order. Bisa lebih dari satu.
    :param pxlb_2: data bytearray pixel RGB order yang ingin di bitwise. Bisa lebih dari satu.
    :return: satu data pixel (3 bytearray) jika kedua param cuma satu pixel juga. > 3 bytearray jika banyak.
    """
    pxlb = bytearray()
    if len(pxlb_1) <= len(pxlb_2):
        for i in range(len(pxlb_1)):
            pxlb += bytearray([pxlb_1[i] | pxlb_2[i]])
    else:
        for i in range(len(pxlb_2)):
            pxlb += bytearray([pxlb_2[i] | pxlb_1[i]])
    return pxlb


class MortalState(Enum):
    """
    State untuk object mortal
    """
    idle = 0
    hit = 2
    destruct = 3
    NaN = -1  # Means not to be drawn


class DummyState(Enum):
    """
    State buat karakter biasa atau pun dummy
    """
    idle = 0
    walk = 1
    jumpBegin = 10
    jump = 11
    jumpEnd = 12
    NaN = -1


class ChainState(Enum):
    """
    State untuk chain Sponge
    """
    idle = 0
    thrownH = 30
    thrownV = 40
    pullGoH = 31
    pullStayH = 32
    pullGoV = 41
    pullStayV = 42
    fallIntro = 999
    releaseIntro = 998
    NaN = -1


class SpongeState(Enum):
    """
    State khusus untuk Wire Sponge
    """
    NaN = -1
    idle = 0
    introChainFall = 60
    introChainWait = 61
    introChainFallEnd = 62
    introSpin = 63
    introCharge = 64
    leapBegin = 10
    leapUp = 11
    leapDown = 12
    leapEnd = 13
    throwHrzBegin = 200
    throwHrz = 201
    throwHrzPullStay = 202
    throwHrzPullGo = 203
    throwHrzRelease = 204
    throwVrtBegin = 300
    throwVrt = 301
    throwVrtPull = 302
    throwVrtEnd = 303
    spin = 100


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
        try:
            img = pyglet.image.load(filename=path).get_image_data()
            self.width = img.width
            self.height = img.height
            self.pitch = -self.width * len('RGB')  # Number of bytes per row
            self.data = bytearray(img.get_data(fmt='RGB', pitch=self.pitch))  # Pixels bytearray data
        except FileNotFoundError:
            print("File not successfully loaded, check ../Resource/")
            exit()

    def get_bytes(self):
        return bytes(self.data)

    def get_color(self, x, y, width=0, height=0) -> Color:
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

    def get_pixel_bytearray(self, x, y, width=0, height=0) -> bytearray:
        '''
        Ambil color dalam bentuk bytearray of pixels dengan koordinat image yang ditentukan. Kalau ingin mengambil dalam
        satu area kotak/garis, width dan height harus ditentukan
        :param x: koordinat x dari LEFT
        :param y: koordinat y dari TOP
        :param width: panjang area jika perlu satu Kotak (Rectangle)
        :param height: lebar area jika perlu satu Kotak (Rectangle)
        :return: string bytearray of pixel (size-nya kelipatan 3, RGB)
        '''
        if x >= self.width:
            x = self.width - 1
        if y >= self.height:
            y = self.height - 1
        idx = y * self.width + x
        idx *= 3
        if width == 0 and height == 0:
            return bytearray([self.data[idx], self.data[idx + 1], self.data[idx + 2]])
        pxl = bytearray()
        for j in range(height):
            for i in range(width):
                try:
                    pxl += bytearray([self.data[idx], self.data[idx + 1], self.data[idx + 2]])
                except IndexError:
                    return pxl
                idx += 3
        return pxl

    def set_color(self, x, y, color: Color, width=0, height=0):
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
            self.data[idx] = bytearray([color.r])
            self.data[idx + 1] = bytearray([color.g])
            self.data[idx + 2] = bytearray([color.b])
            return
        for j in range(height):
            for i in range(width):
                try:
                    self.data[idx] = bytearray([color.r])
                    self.data[idx + 1] = bytearray([color.g])
                    self.data[idx + 2] = bytearray([color.b])
                except IndexError:
                    return
                idx += 3

    def set_pixel_bytearray(self, x, y, pixel_byte: bytearray):
        '''
        Set a single color in different way. Terdiri dari 3 byte RGB
        :param x: koordinat x dari LEFT
        :param y: koordinat y dari TOP
        :param pixel_byte: color yang berupa 3 bytearray of pixel, RGB
        :return: nai desu, tehepero
        '''
        if x >= self.width:
            x = self.width - 1
        if y >= self.height:
            y = self.height - 1
        idx = y * self.width + x
        idx *= 3
        self.data[idx:idx + 3] = pixel_byte


class Frame:
    '''
    Frame bertindak seperti grid yang memotong dan memisahkan pada bagian image untuk sprite yang akan di apply.
    '''

    def __init__(self, xLeft, xRight, yTop, yBottom, anchor: Vector, time_framing, fist_position=None):
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
        self.fist = fist_position


class FrameCollection:
    '''
    Bertindak sebagai penampung Frames. Dipakai sebagai set frame karena akan dianimasikan sesuai state karakternya
    '''

    def __init__(self, state):
        '''
        Buat set of frames bare, atau bisa dibilang sprites.
        :param state: state sesuai set of frames nya. Sesuai class state yang di enum kan
        '''
        self.frames = []
        self.num_frame = len(self.frames)
        self.state = state

    def insert(self, frame):
        '''
        memasukkan frame baru tanpa menghapus yang ada.
        :param frame: frame, sesuai class GameObject.Frame
        :return: tidak ada, void
        '''
        self.frames.append(frame)
        self.num_frame = len(self.frames)


class MortalObject:
    def __init__(self, position: Vector):
        self.position = position
        self.velocity = Vector(0, 0)
        self.curState = MortalState.idle
        self.frameId = 0
        self.on_ground = False
        self.on_equilibrium = Vector(True, False)
        self.curTimeFrame = 0
        self.sprites = []  # Frame collection
        self.spritesId = 0
        self.facing = Facing.left
        self.getIdSpr = {}

    def insert(self, sprite):
        self.getIdSpr[sprite.state] = len(self.sprites)
        self.sprites.append(sprite)

    def setState(self, state):
        self.curState = state
        self.curTimeFrame = 0
        self.frameId = 0
        if state.value == -1:
            return
        self.spritesId = self.getIdSpr[state]

    def nextFrame(self):
        self.curTimeFrame += 1
        if self.curTimeFrame >= self.sprites[self.spritesId].frames[self.frameId].time_framing:
            self.frameId += 1
            if self.frameId == self.sprites[self.spritesId].num_frame:
                self.frameId = 0
            self.curTimeFrame = 0

    def calculate_motion(self, gravity=1):  # gravity in pixel
        frame = self.sprites[self.spritesId].frames[self.frameId]
        if self.on_equilibrium.x:
            self.velocity.x = 0
        else:
            if self.position.x - frame.anchor.x + frame.xLeft < 0:  # Touch platform left
                self.position.x = frame.anchor.x - frame.xLeft
                self.on_equilibrium = Vector(True, False)
                self.velocity.x = 0
                return
            if self.position.x - frame.anchor.x + frame.xRight > 989:  # Right
                self.position.x = 989 - frame.xRight + frame.anchor.x
                self.on_equilibrium = Vector(True, False)
                self.velocity.x = 0
                return
        if self.on_equilibrium.y:
            self.velocity.y = 0
        else:
            if self.position.y + frame.yBottom - frame.anchor.y >= 482 and self.velocity.y > 0:  # Touch platform, or change the code to any
                self.position.y = 482 - frame.yBottom + frame.anchor.y
                self.on_equilibrium = Vector(True, True)
                self.velocity.x = 0
                self.velocity.y = 0
                self.on_ground = True
                return
            self.velocity.y += gravity

    def update(self):
        self.nextFrame()
        self.calculate_motion()


class WireSponge(MortalObject):
    def __init__(self, position=Vector(843, 0)):
        super().__init__(position)
        self.spin_counter = 0
        self.position = Vector(843, 0)
        self.curState = SpongeState.idle
        self.facing = Facing.left
        self.chain = ChainSponge()

    def calculate_motion(self, gravity=1):
        super().calculate_motion(gravity)
        self.chain.on_equilibrium.x = self.on_equilibrium.x
        self.chain.on_equilibrium.y = self.on_equilibrium.y

    def update(self):
        # Calculate current position and get next frame animation
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        if self.velocity.y is not None and self.velocity.x is not None:
            self.chain.velocity.y = self.velocity.y
            self.chain.velocity.x = self.velocity.x

        self.nextFrame()

        # Set fist hand position
        frame = self.sprites[self.spritesId].frames[self.frameId]
        if frame.fist is not None:
            if self.facing == Facing.left:
                self.chain.fist_pos.x = self.position.x + frame.fist.x - frame.anchor.x
            else:
                self.chain.fist_pos.x = self.position.x - frame.fist.x + frame.anchor.x
            self.chain.fist_pos.y = self.position.y + frame.fist.y - frame.anchor.y

        if self.curState == SpongeState.idle:
            pass

        # intro
        elif self.curState == SpongeState.introChainFall:
            self.velocity.y = 15
            frame = self.sprites[self.spritesId].frames[self.frameId]
            self.chain.fist_pos.x = self.position.x + frame.fist.x - frame.anchor.x  # Need to checked further, facing
            self.chain.fist_pos.y = self.position.y + frame.fist.y - frame.anchor.y
            if self.position.y + frame.yBottom - frame.anchor.y >= 482:  # Touch platform
                self.setState(SpongeState.introChainWait)
                self.chain.begin = True
                self.chain.setState(ChainState.releaseIntro)

                # adjusting chain
                frame_chain = self.chain.sprites[self.chain.spritesId].frames[self.chain.frameId]
                last_posY = self.chain.position.y + frame_chain.yBottom - frame_chain.anchor.y
                while last_posY < self.chain.fist_pos.y:
                    frame_chain.anchor.y += 10
                    self.chain.position.y += 10
                    frame_chain.yBottom += 20
                    last_posY = self.chain.position.y + frame_chain.yBottom - frame_chain.anchor.y
                diff = last_posY - self.chain.fist_pos.y
                frame_chain.anchor.y -= diff // 2
                self.chain.position.y -= diff // 2
                frame_chain.yBottom -= diff

                self.velocity.y = 0
                self.position.y = 482 - frame.yBottom + frame.anchor.y
                self.on_ground = True
                self.on_equilibrium = Vector(True, True)
        elif self.curState == SpongeState.introChainWait:
            if self.curTimeFrame == 0 and self.frameId == 0 and self.chain.curState == ChainState.NaN:
                self.setState(SpongeState.introChainFallEnd)
        elif self.curState == SpongeState.introChainFallEnd:
            if self.curTimeFrame == 0:
                self.setState(SpongeState.introSpin)
        elif self.curState == SpongeState.introSpin:
            if self.curTimeFrame == 0 and self.frameId == 0:
                self.spin_counter += 1
            if self.spin_counter == 6:
                self.spin_counter = 0
                self.setState(SpongeState.introCharge)
        elif self.curState == SpongeState.introCharge:
            if self.curTimeFrame == 0 and self.frameId == 0:
                self.setState(SpongeState.idle)

        # State by input control

        # Leap
        elif self.curState == SpongeState.leapBegin:
            self.on_equilibrium = Vector(False, False)
            self.on_ground = False
            self.velocity.y = -20
            if self.facing == Facing.left:
                self.velocity.x = -5
            else:
                self.velocity.x = 5
            if self.curTimeFrame == 0 and self.frameId == 0:
                self.setState(SpongeState.leapUp)
        elif self.curState == SpongeState.leapUp:
            if self.velocity.y >= 6:
                self.setState(SpongeState.leapDown)
        elif self.curState == SpongeState.leapDown:
            if self.on_ground:
                self.setState(SpongeState.leapEnd)
        elif self.curState == SpongeState.leapEnd:
            if self.curTimeFrame == 0 and self.frameId == 0:
                self.setState(SpongeState.idle)

        # Spin
        elif self.curState == SpongeState.spin:
            if self.curTimeFrame == 0 and self.frameId == 0:
                self.spin_counter += 1
            if self.spin_counter == 5:
                self.spin_counter = 0
                self.setState(SpongeState.idle)

        # Throw Chain Horizontally
        elif self.curState == SpongeState.throwHrzBegin:
            if self.curTimeFrame == 0 and self.frameId == 0:
                self.setState(SpongeState.throwHrz)
            if self.frameId == 5:
                self.chain.setState(ChainState.thrownH)
            # still check
            if self.chain.curState == ChainState.pullStayH:
                self.setState(SpongeState.throwHrzPullStay)
            elif self.chain.curState == ChainState.pullGoH:
                self.setState(SpongeState.throwHrzPullGo)
                self.on_equilibrium = Vector(False, True)
                if self.facing == Facing.left:
                    self.velocity.x = -10
                else:
                    self.velocity.x = 10
        elif self.curState == SpongeState.throwHrz:
            if self.chain.curState == ChainState.pullStayH:
                self.setState(SpongeState.throwHrzPullStay)
            elif self.chain.curState == ChainState.pullGoH:
                self.setState(SpongeState.throwHrzPullGo)
                self.on_equilibrium = Vector(False, True)
                if self.facing == Facing.left:
                    self.velocity.x = -10
                else:
                    self.velocity.x = 10
        elif self.curState == SpongeState.throwHrzPullStay:
            if self.chain.curState == ChainState.NaN:
                if not self.on_ground:
                    if self.velocity.y >= 6:
                        self.setState(SpongeState.leapDown)
                    else:
                        self.setState(SpongeState.leapUp)
                else:
                    self.setState(SpongeState.idle)
        elif self.curState == SpongeState.throwHrzPullGo:
            frame = self.sprites[self.spritesId].frames[self.frameId]
            if self.facing == Facing.left:
                self.chain.fist_pos.x = self.position.x + frame.fist.x - frame.anchor.x
            else:
                self.chain.fist_pos.x = self.position.x - frame.fist.x + frame.anchor.x
            if self.chain.curState == ChainState.NaN:
                self.on_equilibrium = Vector(True, True)
                self.setState(SpongeState.throwHrzRelease)
        elif self.curState == SpongeState.throwHrzRelease:
            if self.curTimeFrame == 0 and self.frameId == 0:
                self.on_equilibrium = Vector(False, False)
                if not self.on_ground:
                    if self.facing == Facing.left:
                        self.velocity.x = 10
                        self.position.x += self.velocity.x
                    else:
                        self.velocity.x = -10
                        self.position.x += self.velocity.x
                    self.setState(SpongeState.leapDown)
                else:
                    self.setState(SpongeState.leapEnd)

        # Calculate motion
        self.calculate_motion()


class ChainSponge(MortalObject):
    def __init__(self, position=Vector(None, None)):
        super().__init__(position)
        self.fist_pos = Vector(None, None)
        self.begin = True
        self.frame_buffer = Frame(None, None, None, None, Vector(None, None), None)

    def update(self):

        self.nextFrame()
        # Intro Chain
        if self.curState == ChainState.NaN:
            return
        elif self.curState == ChainState.fallIntro:
            frame = self.sprites[self.spritesId].frames[self.frameId]
            if self.begin:
                self.position.x = self.fist_pos.x
                self.position.y = frame.anchor.y - frame.yTop - 10
                self.begin = False
            last_posY = self.position.y + frame.yBottom - frame.anchor.y
            while last_posY < self.fist_pos.y:
                frame.anchor.y += 10  # This is just a way defining chain pull/throw velocity
                self.position.y += 10
                frame.yBottom += 20
                last_posY = self.position.y + frame.yBottom - frame.anchor.y
            # adjusting if frame went too far from fist that results async frame position
            diff = last_posY - self.fist_pos.y
            frame.anchor.y -= diff // 2
            self.position.y -= diff // 2
            frame.yBottom -= diff
        elif self.curState == ChainState.releaseIntro:
            frame = self.sprites[self.spritesId].frames[self.frameId]
            spike_posY = self.position.y - frame.anchor.y + frame.yTop
            if spike_posY >= self.fist_pos.y:
                self.setState(ChainState.NaN)
            frame.anchor.y -= 20
            self.position.y += 20
            frame.yBottom -= 40

        # Chain Thrown

        elif self.curState == ChainState.thrownH:
            sprId = self.spritesId
            frmId = self.frameId
            frame = self.sprites[self.spritesId].frames[self.frameId]
            if self.begin:
                self.position.y = self.fist_pos.y
                if self.facing == Facing.left:
                    self.position.x = self.fist_pos.x - frame.xRight + frame.anchor.x
                else:
                    self.position.x = self.fist_pos.x + frame.xRight - frame.anchor.x
                self.begin = False
                return
            length = frame.xRight - frame.xLeft
            if length <= 190:
                if self.facing == Facing.left:
                    frame.anchor.x += 23
                    self.position.x -= 23
                    frame.xRight += 46
                    # Check whether spike pinned
                    spike_posX = self.position.x - frame.anchor.x + frame.xLeft
                    if spike_posX <= 0:
                        self.setState(ChainState.pullGoH)
                        self.revert_frame(sprId, frmId)
                else:
                    frame.anchor.x += 23
                    self.position.x += 23
                    frame.xRight += 46
                    # Check whether spike pinned
                    spike_posX = self.position.x + frame.anchor.x - frame.xLeft
                    if spike_posX >= 989:
                        self.setState(ChainState.pullGoH)
                        self.revert_frame(sprId, frmId)
            else:
                self.setState(ChainState.pullStayH)
                self.revert_frame(sprId, frmId)
        elif self.curState == ChainState.pullStayH:
            frame = self.sprites[self.spritesId].frames[self.frameId]
            if self.facing == Facing.left:
                spike_posX = self.position.x - frame.anchor.x + frame.xLeft
                if spike_posX < self.fist_pos.x:
                    frame.anchor.x -= 23
                    self.position.x += 23
                    frame.xRight -= 46
                else:
                    self.setState(ChainState.NaN)
            else:
                spike_posX = self.position.x + frame.anchor.x - frame.xLeft
                if spike_posX > self.fist_pos.x:
                    frame.anchor.x -= 23
                    self.position.x -= 23
                    frame.xRight -= 46
                else:
                    self.setState(ChainState.NaN)
        elif self.curState == ChainState.pullGoH:
            frame = self.sprites[self.spritesId].frames[self.frameId]
            if self.facing == Facing.left:
                tail_posX = self.position.x + frame.xRight - frame.anchor.x
                diff = tail_posX - self.fist_pos.x
                if not self.on_equilibrium.x and self.on_equilibrium.y:
                    frame.xRight -= diff
                    frame.anchor.x -= diff // 2
                    self.position.x -= diff // 2
                else:
                    self.setState(ChainState.NaN)
            else:
                tail_posX = self.position.x - frame.xRight + frame.anchor.x
                diff = self.fist_pos.x - tail_posX
                if not self.on_equilibrium.x and self.on_equilibrium.y:
                    frame.xRight -= diff
                    frame.anchor.x -= diff // 2
                    self.position.x += diff // 2
                else:
                    self.setState(ChainState.NaN)

        if self.velocity.x != 0 and self.velocity.y != 0:
            self.position.x += self.velocity.x
            self.position.y += self.velocity.y

    def setState(self, state):
        if self.curState == ChainState.NaN and state != ChainState.NaN:  # Begin new throw
            self.spritesId = self.getIdSpr[state]
            self.curState = state
            self.curTimeFrame = 0
            self.frameId = 0
            frame = self.sprites[self.spritesId].frames[self.frameId]
            self.frame_buffer.xLeft = frame.xLeft
            self.frame_buffer.xRight = frame.xRight
            self.frame_buffer.yBottom = frame.yBottom
            self.frame_buffer.yTop = frame.yTop
            self.frame_buffer.anchor = frame.anchor
            self.frame_buffer.time_framing = frame.time_framing
            return
        else:
            self.curState = state
            self.curTimeFrame = 0
            self.frameId = 0
        if state == ChainState.NaN:
            return
        frame_prev = self.sprites[self.spritesId].frames[self.frameId]
        self.spritesId = self.getIdSpr[state]
        frame_cur = self.sprites[self.spritesId].frames[self.frameId]

        # adjusting
        frame_cur.yTop = frame_prev.yTop
        frame_cur.yBottom = frame_prev.yBottom
        frame_cur.xRight = frame_prev.xRight
        frame_cur.xLeft = frame_prev.xLeft
        frame_cur.anchor = Vector(frame_prev.anchor.x, frame_prev.anchor.y)

    def revert_frame(self, sprId, frmId):
        # Revert frame after being changed
        frame = self.sprites[sprId].frames[frmId]
        frame.xLeft = self.frame_buffer.xLeft
        frame.xRight = self.frame_buffer.xRight
        frame.yBottom = self.frame_buffer.yBottom
        frame.yTop = self.frame_buffer.yTop
        frame.anchor = self.frame_buffer.anchor
        frame.time_framing = self.frame_buffer.time_framing
        self.begin = True
