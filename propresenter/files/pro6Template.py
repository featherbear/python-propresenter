from collections import OrderedDict
from uuid import uuid4
from .xml import File as XML

"""
Interesting things
RVTemplateDocument  versionNumber, os, buildNumber
"""


class File():
    # Reminder that variables act as pointers instead of creating a new copy!

    def __init__(self, fileName: str, fileDirectory: str):
        import propresenter.utils

        self._file = XML(fileName, fileDirectory)
        self._root = self._file.data["RVPresentationDocument"] if "RVPresentationDocument" in self._file.data else self._file.data["RVTemplateDocument"]

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
                if not uuid: uuid = str(uuid4())
                if not propresenter.utils.validUUID(uuid):
                    raise ValueError("Invalid UUID: "+ uuid)

                if updateReferences:
                    raise NotImplementedError
                    #self.obj["@uuid"]
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
            def name(self, notes: str):
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
