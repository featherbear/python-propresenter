import colorsys
import re
from _datetime import datetime
from uuid import uuid4


def getDateString():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")


class UUID:
    @staticmethod
    def generateUUID():
        return str(uuid4()).upper()

    @staticmethod
    def validUUID(uuid):
        return re.match("^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$", uuid,
                        re.IGNORECASE) is not None


class HSLa_Handler:
    HSLa_Store = None

    @staticmethod
    def _parseTuple(colorTuple: tuple):

        if 3 <= len(colorTuple) <= 4:
            alpha = colorTuple[3] if len(colorTuple) == 4 else 255
            if colorUtil.checks.between0_255(alpha):
                alpha /= 255
            if not colorUtil.checks.between0_1(alpha):
                raise ValueError("Invalid alpha value")
            return colorTuple[0], colorTuple[1], colorTuple[2], alpha
        return None

    @property
    def colorHSL(self):
        return tuple(map(float, self.HSLa_Store.split(" ")))

    @colorHSL.setter
    def colorHSL(self, HSLtuple: tuple):
        v1, v2, v3, v4 = self._parseTuple(HSLtuple)
        if not all(map(colorUtil.checks.between0_1, (v1, v2, v3))):
            raise ValueError("Invalid HSL combination")
        self.HSLa_Store = " ".join(map(str, (v1, v2, v3, v4)))

    @property
    def colorRGB(self):
        h, s, l, a = self.colorHSL
        return (*colorUtil.conversion.hsl_to_rgb(h, s, l), a)

    @colorRGB.setter
    def colorRGB(self, RGBtuple: tuple):
        v1, v2, v3, v4 = self._parseTuple(RGBtuple)
        if not all(map(colorUtil.checks.between0_255, (v1, v2, v3))):
            raise ValueError("Invalid RGB combination")
        self.HSLa_Store = " ".join(map(str, (*colorUtil.conversion.rgb_to_hsl(v1, v2, v3), v4)))

    @property
    def colorHEX(self):
        h, s, l, a = self.colorHSL
        return colorUtil.conversion.hsl_to_hex(h, s, l), a

    @colorHEX.setter
    def colorHEX(self, HEXtupleOrString, alpha=255):
        if type(HEXtupleOrString) == str:
            HEXstring = HEXtupleOrString
        elif type(HEXtupleOrString) == tuple and len(HEXtupleOrString) == 2:
            HEXstring = HEXtupleOrString[0]
            alpha = HEXtupleOrString[1]
        else:
            raise TypeError("Invalid paramaters")
        if type(alpha) == int and 0 <= alpha <= 255:
            alpha /= 255
        if not (type(alpha) == float and colorUtil.checks.between0_1(alpha)):
            raise ValueError("Invalid alpha value")

        match = colorUtil.checks.hex(HEXstring)
        if not match:
            raise ValueError("Invalid HEX colour")
        self.HSLa_Store = " ".join(map(str, (*colorUtil.conversion.hex_to_hsl(match), alpha)))


class colorUtil:
    # https://www.viget.com/articles/equating-color-and-transparency/
    # target = opacity x overlay + (1-opacity) x background
    class checks:
        @staticmethod
        def between0_1(v):
            return 0 <= v <= 1

        @staticmethod
        def between0_255(v):
            return 0 <= v <= 255 and type(v) == int

        @staticmethod
        def hex(s):
            match = re.match("^#?(([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}))$", s)
            return match[0] if match else False

    class conversion:
        @staticmethod
        def hsl_to_rgb(h, s, l):
            return tuple(map(lambda z1b: round(z1b * 255), colorsys.hls_to_rgb(h, l, s)))

        @staticmethod
        def rgb_to_hsl(r, g, b):
            h, l, s = colorsys.rgb_to_hls(*map(lambda z255b: z255b / 255, (r, g, b)))
            return h * 3.6, s, l
            # hue: degree, saturation: percentage, l: luminance
            # return tuple(map(round,(h * 360, s*100, l*100)))

        @staticmethod
        def rgb_to_hex(r, g, b):
            # https://stackoverflow.com/a/3380739
            return '%02X%02X%02X' % (r, g, b)

        @staticmethod
        def hsl_to_hex(h, s, l):
            return colorUtil.conversion.rgb_to_hex(*colorUtil.conversion.hsl_to_rgb(h, s, l))

        @staticmethod
        def hex_to_rgb(hex):
            # #NewYearNewMe #NewYearsResolution_WriteReadableCode
            # hip-hip hooray for unreadable code!
            # https://stackoverflow.com/a/29643643
            return (int(("".join([c * 2 for c in hex]) if len(hex) == 3 else hex).lstrip("#")[i:i + 2], 16) for i in
                    (0, 2, 4))

        @staticmethod
        def hex_to_hsl(hex):
            return colorUtil.conversion.rgb_to_hsl(*colorUtil.conversion.hex_to_rgb(hex))
