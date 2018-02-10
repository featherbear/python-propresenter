import math
from collections import OrderedDict
from uuid import uuid4
import os

from .xml import File as XML

"""
Interesting things
RVTemplateDocument  versionNumber, os, buildNumber
"""


class File():
    # Reminder that variables act as pointers instead of creating a new copy!

    def __init__(self, fileName: str, fileDirectory: str):
        import propresenter.utils

        self._file = XML(os.path.join(fileDirectory, fileName), ("RVDisplaySlide", "RVPoint"))
        self._root = self._file.data["RVPresentationDocument"] if "RVPresentationDocument" in self._file.data else \
        self._file.data["RVTemplateDocument"]

        class Elements(list):
            def __init__(self, *args, **kwargs):
                list.__init__(self, *args, **kwargs)

            def __getitem__(self, item):
                if type(item) == int:
                    return Element(list.__getitem__(self, item))
                elif propresenter.utils.validUUID(item):
                    item = item.upper()
                    if item not in [s["@UUID"].upper() for s in self]:
                        return None
                    return Element(next(filter(lambda element: element["@UUID"].upper() == item, self)))
                else:
                    raise ValueError("Invalid UUIDv4")

            def newSlide(self):
                # add args
                slide = Slide()
                self.append(slide)
                return slide

        class Element(object):
            def __init__(self, obj: OrderedDict = OrderedDict()):
                self.obj = self._propertyGrp.obj = obj
                if not any(obj):
                    self.changeUUID(updateReferences=False)
                self.fill = self.fill()
                self.border = self.border()
                self.shadow = self.shadow()

            class _propertyGrp:
                # This is the wrong way to go about, but hey?
                pass

            @property
            def uuid(self):
                return self.obj["@UUID"]

            def changeUUID(self, uuid=None, updateReferences=True):
                # TODO check if used UUID
                if not uuid: uuid = str(uuid4())
                if not propresenter.utils.validUUID(uuid):
                    raise ValueError("Invalid UUID: " + uuid)

                if updateReferences:
                    raise NotImplementedError
                    # self.obj["@uuid"]
                    # 1 - brute force raw edit
                    # lol how to implement tho
                    # re.sub("(\W?)%s(\W?)" % self.uuid, "\g<1>%s\g<2>" % uuid())
                    # 2 - A better way would be to iterate over the arragenments, groups and whatnot
                    # ceebs tho
                    pass
                else:
                    self.obj["@UUID"] = uuid.lower()

            @property
            def fromTemplate(self):
                raise NotImplementedError

            @property
            def source(self):
                raise NotImplementedError

            @property
            def typeID(self):
                raise NotImplementedError

            @property
            def displayDelay(self):
                raise NotImplementedError

            @property
            def persistent(self):
                raise NotImplementedError

            @property
            def dimensions(self):
                raise NotImplementedError

            @property
            def scale(self):
                raise NotImplementedError

            @property
            def position(self):
                raise NotImplementedError

            @property
            def name(self):
                return self.obj["@displayName"]

            @name.setter
            def name(self, name: str):
                if len(name) > 256:
                    # ProPresenter doesn't actually have a limit, so setting our own limit here
                    raise ValueError("Value too long (Max 256 characters)")
                self.obj["@displayName"] = name

            @property
            def locked(self):
                return self.obj["@locked"].lower() == "true"

            @locked.setter
            def locked(self, state: bool):
                self.obj["@locked"] = str(state).lower()

            @property
            def opacity(self):
                return float(self.obj["@opacity"])

            @opacity.setter
            def opacity(self, opacity: float):
                if not propresenter.utils.colorUtil.checks.between0_1(opacity):
                    raise ValueError("Bad opacity (min: 0.0, max: 1.0)")
                self.obj["@opacity"] = str(float)

            @property
            def rotation(self):
                return int(self.obj["@rotation"])

            @rotation.setter
            def rotation(self, degree: int):
                self.obj["@rotation"] = str(degree % 360)

            class fill(_propertyGrp, propresenter.utils.HSLa_Handler):
                def __init__(self):
                    self.HSLa_Store = self.obj.get("@fillColor")

                @property
                def enabled(self):
                    return self.obj["@drawingFill"].lower() == "true"

                @enabled.setter
                def enabled(self, state: bool):
                    self.obj["@drawingFill"] = str(state).lower()

            class border(_propertyGrp, propresenter.utils.HSLa_Handler):
                def __init__(self):
                    self.HSLa_Store = self.obj["dictionary"]["NSColor"]

                @property
                def enabled(self):
                    return self.obj["@drawingStroke"].lower() == "true"

                @enabled.setter
                def enabled(self, state: bool):
                    self.obj["@drawingStroke"] = str(state).lower()

                @property
                def radius(self):
                    return int(self.obj["@bezelRadius"])

                @radius.setter
                def radius(self, radius: int):
                    if not 0 <= radius <= 1174:
                        raise ValueError("Bad radius (min: 0, max: 1174)")
                    self.obj["@bezelRadius"] = str(radius)

                @property
                def width(self):
                    return int(self.obj["dictionary"]["NSNumber"])

                @width.setter
                def width(self, width: int):
                    if not 0 <= width <= 100:
                        raise ValueError("Bad width (min: 0, max: 100)")
                    self.obj["dictionary"]["NSNumber"] = str(width)

            class shadow(_propertyGrp, propresenter.utils.HSLa_Handler):
                @property
                def HSLa_Store(self):
                    return self.obj["shadow"].split("|")[1]

                @HSLa_Store.setter
                def HSLa_Store(self, val):
                    r, c, a = self.obj["shadow"].split("|")
                    self.obj["shadow"] = "|".join(map(str, (r, val, a)))

                @property
                def enabled(self):
                    return self.obj["@drawingShadow"].lower() == "true"

                @enabled.setter
                def enabled(self, state: bool):
                    self.obj["@drawingShadow"] = str(state).lower()

                @property
                def radius(self):
                    return int(self.obj["shadow"].split("|")[0])

                @radius.setter
                def radius(self, radius: int):
                    if not 0 <= radius <= 100:
                        raise ValueError("Bad radius (min: 0, max: 100)")
                    r, c, a = self.obj["shadow"].split("|")
                    r = radius
                    self.obj["shadow"] = "|".join(map(str, (r, c, a)))

                @property
                def angle(self):
                    a = self.obj["shadow"].split("|")[-1]
                    x, y = map(float, a[1:-1].split(", "))
                    return int(math.degrees(math.atan2(y, x)) % 360)

                @angle.setter
                def angle(self, angle: int):
                    # UH WHY IS IT STORED AS A 2D X AND Y VALUE
                    # Circle with radius 3; but doesn't matter
                    r, c = self.obj["shadow"].split("|")[:-1]

                    # Original Method
                    # from fractions import Fraction
                    # f = Fraction(math.tan(math.radians(angle % 360))).limit_denominator()
                    # x = f.numerator * 3
                    # y = f.denominator * 3

                    # https://stackoverflow.com/a/35402676
                    radius = 3  # Don't think radius really matters...
                    angle = math.radians(angle)
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)
                    p = "{%s, %s}" % (x, y)
                    self.obj["shadow"] = "|".join(map(str, (r, c, p)))

                @property
                def width(self):
                    return int(self.obj["dictionary"]["NSNumber"])

                @width.setter
                def width(self, width: int):
                    if not 0 <= width <= 100:
                        raise ValueError("Bad width (min: 0, max: 100)")
                    self.obj["dictionary"]["NSNumber"] = str(width)
        class VideoElement(Element):
            # source
            # manufactureURL
            # manufactureName
            # format
            # audioVolume
            # playRate
            # frameRate
            # playbackBehavior | 0 for stop, 1 for repeat
            # inPoint
            # outPoint
            # endPoint
            # naturalSize
            # timeScale
            # scaleSize
            # scaleBehaviour
            # flippedHorizontally
            # flippedVertically
            # imageOffset
            pass
        class ImageElement(Element):
            # source
            # scaleSize
            # flippedVertically
            # flippedHorizontally
            # scaleBehaviour
            # manufactureURL
            # manufactureName
            # format
            # imageOffset
            pass
        class LiveViewElement(Element):
            # scaleBehaviour
            # flippedVertically
            # flippedHorizontally
            # scaleSize
            # imageOffset
            # manufactureURL
            # manufactureName
            # format
            # videoSourceModelName (blank for disable)
            # audioSourceModelName (blank for disable)
            # audioVolume (float 0-2)
            pass
        class HTMLShapeElement(Element):
            # urlString
            # requestInterval - 0 to disable
            # requiresLiveUpdates
            pass
        class TextCrawlerElement(Element):
            # rssParsingStyle
            # textCrawlerType
            # loopBehavior
            # textCrawlerSpeed
            # tetCrawlerSectionDelimeter
            # adjustHeightToFit
            # // got text stuff
            pass
        class BezierPathElement(Element):
            def __init__(self):
                self.points = self.points(self.obj["array"])
            class points(list):
                def clear(self):
                    raise NotImplementedError
                def addPoint(self):
                    raise NotImplementedError
                def removeLastPoint(self):
                    raise NotImplementedError
        class TextElement(Element):
            @property
            def adjustsHeightToFit(self):
                return self.obj["@adjustsHeightToFit"].lower() == "true"

            @adjustsHeightToFit.setter
            def adjustsHeightToFit(self, state: bool):
                self.obj["@adjustsHeightToFit"] = str(state).lower()

            @property
            def verticalAlign(self):
                return int(self.obj["@verticalAlignment"])

            class verticalAlignTypes:
                CENTER = 0
                TOP = 1,
                BOTTOM = 2

            @verticalAlign.setter
            def verticalAlign(self, align: int):
                if align not in (0, 1, 2):
                    raise ValueError("Bad vertical alignment type (0, 1 or 2)")
                self.obj["@verticalAlignment"] = str(align)

            @property
            def dataWinFont(self):
                raise NotImplementedError

            @property
            def dataWinFlow(self):
                raise NotImplementedError

            @property
            def dataRTF(self):
                raise NotImplementedError

            @property
            def plainText(self):
                raise NotImplementedError

            @property
            def reveal(self):
                return int(self.obj["@revealType"])

            class revealTypes:
                NONE = 0
                BULLET_LIST = 1,
                FILL_IN_THE_BLANK = 2

            @reveal.setter
            def reveal(self, reveal: int):
                if reveal not in (0, 1, 2):
                    raise ValueError("Bad reveal type (0, 1 or 2)")
                self.obj["@revealType"] = str(reveal)

        class Slides(list):
            def __init__(self, *args, **kwargs):
                list.__init__(self, *args, **kwargs)

            def __getitem__(self, item):
                if type(item) == int:
                    return Slide(list.__getitem__(self, item))
                elif propresenter.utils.validUUID(item):
                    item = item.upper()
                    if item not in [s["@UUID"] for s in self]:
                        return None
                    return Slide(next(filter(lambda slide: slide["@UUID"] == item, self)))
                else:
                    raise ValueError("Invalid UUIDv4")

            def newSlide(self):
                # add args
                slide = Slide()
                self.append(slide)
                return slide

        class Slide(object):
            def __init__(self, obj: OrderedDict = OrderedDict()):
                self.obj = self._propertyGrp.obj = obj
                if not any(obj):
                    self.changeUUID(updateReferences=False)
                self.background = self.background()

            class _propertyGrp:
                # This is the wrong way to go about, but hey?
                pass

            class background(_propertyGrp, propresenter.utils.HSLa_Handler):
                def __init__(self):
                    self.HSLa_Store = self.obj.get("@backgroundColor")

                @property
                def enabled(self):
                    return self.obj["@drawingBackgroundColor"].lower() == "true"

                @enabled.setter
                def enabled(self, state: bool):
                    self.obj["@drawingBackgroundColor"] = str(state).lower()

            @property
            def uuid(self):
                return self.obj["@UUID"]

            def changeUUID(self, uuid=None, updateReferences=True):
                # TODO check if used UUID
                if not uuid: uuid = str(uuid4())
                if not propresenter.utils.validUUID(uuid):
                    raise ValueError("Invalid UUID: " + uuid)

                if updateReferences:
                    raise NotImplementedError
                    # self.obj["@uuid"]
                    # 1 - brute force raw edit
                    # lol how to implement tho
                    # re.sub("(\W?)%s(\W?)" % self.uuid, "\g<1>%s\g<2>" % uuid())
                    # 2 - A better way would be to iterate over the arragenments, groups and whatnot
                    # ceebs tho
                    pass
                else:
                    self.obj["@UUID"] = uuid.upper()

            @property
            def enabled(self):
                return self.obj["@enabled"].lower() == "true"

            @enabled.setter
            def enabled(self, state: bool):
                self.obj["@enabled"] = str(state).lower()

            @property
            def cues(self):
                raise NotImplementedError

            @property
            def hotkey(self):
                raise NotImplementedError

            @property
            def enabled(self):
                return self.obj["@enabled"].lower() == "true"

            @enabled.setter
            def enabled(self, state: bool):
                self.obj["@enabled"] = str(bool).lower()

            class label(_propertyGrp, propresenter.utils.HSLa_Handler):
                def __init__(self):
                    self.HSLa_Store = self.obj["@highlightColor"]

                @property
                def name(self):
                    return self.obj["@label"]

                @name.setter
                def name(self, name: str):
                    if len(name) > 256:
                        raise ValueError("Value too long (Max 256 characters)")
                    self.obj["@label"] = name

            @property
            def notes(self):
                return self.obj["@notes"]

            @notes.setter
            def notes(self, notes: str):
                if len(notes) > 1000:
                    raise ValueError("Value too long (Max 1000 characters)")
                self.obj["@notes"] = notes

                # We can ignore chordChartPath for a template

        self.slides: Slides = Slides(self._root["array"]["RVDisplaySlide"])
        print(self.slides.newSlide())
        # Should check by array @rvXMLIvarName="slides"

    @property
    def width(self):
        return int(self._root["@width"])

    @width.setter
    def width(self, i):
        self._root["@width"] = str(i)

    @property
    def height(self):
        return int(self._root["@height"])

    @height.setter
    def height(self, i):
        self._root["@height"] = str(i)

    @property
    def dimensions(self):
        return int(self.width), int(self.height)

    @dimensions.setter
    def dimensions(self, WHtuple: tuple):
        self.width = WHtuple[0]
        self.height = WHtuple[1]
