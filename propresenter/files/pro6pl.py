import os.path
import urllib.parse
from collections import OrderedDict
from datetime import datetime
from uuid import uuid4
import mutagen

import propresenter.utils
from .xml import File as XML

getDateString = lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
uuid = lambda: str(uuid4()).upper()


class File(XML):
    # Reminder that variables act as pointers instead of creating a new copy!
    def __init__(self, filePath: str = None):
        if filePath:
            XML.__init__(self, filePath, ("array", "RVPlaylistNode", "RVDocumentCue", "RVHeaderCue"))
        else:
            self.data = {
                "RVPlaylistDocument": {
                    "@versionNumber": 600,
                    "@os": 1,
                    "@buildNumber": 6016,
                    "RVPlaylistNode": [{
                        "@displayName": "root",
                        "@UUID": uuid(),
                        "@smartDirectoryURL": "",
                        "@modifiedDate": getDateString(),
                        "@type": 0,
                        "@isExpanded": 0,
                        "@hotFolderType": 2,
                        "@rvXMLIvarName": "rootNode",
                        "array": [
                            {
                                "@rvXMLIvarName": "children",
                            }, {

                                "@rvXMLIvarName": "events"
                            }
                        ]
                    }],
                    "array": {
                        "@rvXMLIvarName": "deletions"
                    }
                }
            }

        class Element():
            def __new__(cls, *args, **kwargs):
                _obj = super(Element, cls).__new__(cls)
                _obj.data = args[0]
                return _obj

            def __repr__(self):
                return self.__class__.__name__ + '("%s")' % self.name

            @property
            def order(self):
                return self.data["@__order__"]

            @property
            def name(self):
                return self.data["@displayName"]

            @name.setter
            def name(self, name):
                self.data["@displayName"] = name

        class Folder(Element):
            @property
            def children(self):
                return Children(self.data["array"][0])

            def __init__(elem, *args):
                class add:
                    @staticmethod
                    def folder(folderName, typeNumber: int = 2):
                        root = elem.data["array"][0]
                        data = {"@displayName": folderName,
                                "@UUID": uuid(),
                                "@smartDirectoryURL": "",
                                "@modifiedDate": getDateString(),
                                "@type": typeNumber,
                                "@isExpanded": True,
                                "@hotFolderType": "2",
                                "@__order__": self.currentOrder + 1,
                                "array": [
                                    {
                                        "@rvXMLIvarName": "children",
                                        "@__order__": self.currentOrder + 2
                                    }, {

                                        "@rvXMLIvarName": "events",
                                        "@__order__": self.currentOrder + 3
                                    }
                                ]}
                        if "RVPlaylistNode" in root:
                            root["RVPlaylistNode"].append(data)
                        else:
                            root["RVPlaylistNode"] = [data]

                        self.currentOrder += 3
                        return Folder(root["RVPlaylistNode"][-1])

                    @staticmethod
                    def playlist(playlistName):
                        # format is exactly the same, except that playlists have a type number of 3
                        self.add.folder(playlistName, 3)

                elem.add = add()

        class Playlist(Element):
            @property
            def children(self):
                return Children(self.data["array"][0])

            def __init__(elem, *args):
                class add:
                    @staticmethod
                    def audio(audioPath):
                        __mediaObject = mutagen.File(audioPath)
                        if __mediaObject is None:
                            raise Exception("Bad media file")
                        __mediaObjectDuration = int(__mediaObject.info.length * 600)

                        root = elem.data["array"][0]
                        data = {
                            "@UUID": uuid(),
                            "@displayName": os.path.basename(audioPath),  # doesn't matter
                            "@actionType": 0,
                            "@enabled": 1,
                            "@timeStamp": 0,
                            "@delayTime": 0,
                            "@tags": "",
                            "@nextCueUUID": "00000000-0000-0000-0000-000000000000",
                            "behavior": "1",
                            "alignment": "4",
                            "dateAdded": "",
                            "@__order__": self.currentOrder + 1,
                            "RVAudioElement": [{
                                "@rvXMLIvarName": "element",
                                "@volume": 1,
                                "@playRate": 1,
                                "@loopBehaviour": 0,
                                "@audioType": 0,
                                "@inPoint": 0,
                                "@outPoint": 0,
                                "@displayName": os.path.basename(audioPath),  # doesn't matter
                                "@source": urllib.parse.quote(audioPath),
                                "array": [{
                                    "@rvXMLIvarName": "effects",
                                }],
                            }]
                        }
                        if "RVAudioCue" in root:
                            root["RVAudioCue"].append(data)
                        else:
                            root["RVAudioCue"] = [data]

                        # an existing file might need the order of all the proceeding elements shifted
                        self.currentOrder += 1
                        # no return

                    @staticmethod
                    def video(videoPath):
                        __mediaObject = mutagen.File(videoPath)
                        if __mediaObject is None:
                            raise Exception("Bad media file")
                        __mediaObjectDuration = int(__mediaObject.info.length * 600) # timeScale = 600

                        root = elem.data["array"][0]
                        data = {
                            "@UUID": uuid(),
                            "@displayName": os.path.basename(videoPath),  # doesn't matter
                            "@actionType": 0,
                            "@enabled": 1,
                            "@timeStamp": 0,
                            "@delayTime": 0,
                            "@tags": "",
                            "@nextCueUUID": "00000000-0000-0000-0000-000000000000",
                            "@behavior": 2,
                            "@alignment": 4,
                            "@dateAdded": "",
                            "@__order__": self.currentOrder + 1,
                            "RVVideoElement": [{
                                "@UUID": None,
                                "@rvXMLIvarName": "element",
                                "@displayName": os.path.basename(videoPath),  # doesn't matter
                                # "@displayDelay": 0,
                                # "@locked": 0,
                                # "@persistent": 0,
                                # "@typeID": 0,
                                # "@fromTemplate": 0,
                                # "@bezelRadius": 0,
                                # "@drawingFill": 0,
                                # "@drawingShadow": 0,
                                # "@drawingStroke": 0,
                                # "@fillColor": "1 1 1 1",
                                # "@rotation": 0,
                                "@source": urllib.parse.quote(videoPath),

                                "@scaleBehavior": 0,
                                    # 0 - Scale to Fit
                                    # 1 - Scale to Fill
                                    # 2 - Stretch to Fit
                                #"@manufactureURL": "",
                                #"@manufactureName": "",
                                #"@format": "",
                                #"@scaleSize": "{1.0, 1.0}",
                                #"@imageOffset": "{0.0, 0.0}",

                                #"@frameRate": "23.9760246276855", #???????????/




                                "@flippedHorizontally": "false",
                                "@flippedVertically": "false",

                                "@audioVolume": "1",
                                "@playRate": "1",
                                "@playbackBehavior": "0", # STOP on finish

                                "@timeScale": "600", # WHY THOUGH???
                                "@inPoint": "0",  #
                                "@outPoint": __mediaObjectDuration,  #
                                "@endPoint": __mediaObjectDuration,  #

                                #"@naturalSize": "{1920, 1080}",  #
                                "@fieldType": "0",
                                "RVRect3D": [{
                                    "@rvXMLIvarName": "position",
                                    "#text": "{0 0 0 0 0}",
                                }],
                                "shadow": [{
                                    "@rvXMLIvarName": "shadow",
                                    "#text": "0 | 0 0 0 0 | {0, 0}"
                                }],
                                "dictionary": [{
                                    "@rvXMLIvarName": "stroke",
                                    "NSColor": [{
                                        "@rvXMLDictionaryKey": "RVShapeElementStrokeColorKey",
                                        "#text": "0 0 0 1"
                                    }],
                                    "NSNumber": [{
                                        "@rvXMLDictionaryKey": "RVShapeElementStrokeWidthKey",
                                        "@hint": "float",
                                        "#text": "1.0"
                                    }]
                                }],
                                "array": [{
                                    "@rvXMLIvarName": "effects"
                                }]
                            }]
                        }
                        data["RVVideoElement"][0]["@UUID"] = data["@UUID"].lower()
                        if "RVMediaCue" in root:
                            root["RVMediaCue"].append(data)
                        else:
                            root["RVMediaCue"] = [data]

                        # an existing file might need the order of all the proceeding elements shifted
                        self.currentOrder += 1
                        # return

                    @staticmethod
                    def image(imagePath):
                        root = elem.data["array"][0]
                        data = {
                            "@UUID": uuid(),
                            "@displayName": os.path.basename(imagePath),  # doesn't matter
                                # on the playlist view, the extension is stripped away
                                #   # "aaaaa." -> "aaaaa"
                                # Full name shows up on the contiguous view
                            "@actionType": 0,
                            "@enabled": 1,
                            "@timeStamp": 0,
                            "@delayTime": 0,
                            "@tags": "",
                            "@nextCueUUID": "00000000-0000-0000-0000-000000000000",
                            "@behavior": 2,
                            "@alignment": 4,
                            "@dateAdded": "",
                            "@__order__": self.currentOrder + 1,
                            "RVImageElement": [{
                                "@UUID": None,
                                "@rvXMLIvarName": "element",
                                "@displayName": os.path.basename(imagePath),  # doesn't matter
                                "@displayDelay": 0,
                                "@locked": 0,
                                "@persistent": 0,
                                "@typeID": 0,
                                "@fromTemplate": 0,
                                "@bezelRadius": 0,
                                "@drawingFill": 0,
                                "@drawingShadow": 0,
                                "@drawingStroke": 0,
                                "@fillColor": "1 1 1 1",
                                "@rotation": 0,
                                "@source": urllib.parse.quote(imagePath),
                                "@flippedHorizontally": "false",
                                "@flippedVertically": "false",
                                "@scaleBehavior": 0,
                                "@manufactureName": "",
                                "@format": "",
                                "@scaleSize": "{1.0, 1.0}",
                                "@imageOffset": "{0.0, 0.0}",
                                "RVRect3D": [{
                                    "@rvXMLIvarName": "position",
                                    "#text": "{0 0 0 0 0}",
                                }],
                                "shadow": [{
                                    "@rvXMLIvarName": "shadow",
                                    "#text": "0 | 0 0 0 0 | {0, 0}"
                                }],
                                "dictionary": [{
                                    "@rvXMLIvarName": "stroke",
                                    "NSColor": [{
                                        "@rvXMLDictionaryKey": "RVShapeElementStrokeColorKey",
                                        "#text": "0 0 0 1"
                                    }],
                                    "NSNumber": [{
                                        "@rvXMLDictionaryKey": "RVShapeElementStrokeWidthKey",
                                        "@hint": "float",
                                        "#text": "1.0"
                                    }]
                                }],
                                "array": [{
                                    "@rvXMLIvarName": "effects"
                                }]
                            }]
                        }
                        data["RVImageElement"][0]["@UUID"] = data["@UUID"].lower()

                        if "RVMediaCue" in root:
                            root["RVMediaCue"].append(data)
                        else:
                            root["RVMediaCue"] = [data]

                        # an existing file might need the order of all the proceeding elements shifted
                        self.currentOrder += 1
                        # return

                    @staticmethod
                    def document(documentPath):
                        root = elem.data["array"][0]
                        data = {
                            "@UUID": uuid(),
                            "@displayName": os.path.basename(documentPath),  # doesn't matter
                            "@filePath": urllib.parse.quote(documentPath),
                            "@selectedArrangementID": "",
                            "@actionType": 0,
                            "@enabled": 1,
                            "@timeStamp": 0,
                            "@delayTime": 0,
                            "@__order__": self.currentOrder + 1,
                        }
                        if "RVDocumentCue" in root:
                            root["RVDocumentCue"].append(data)
                        else:
                            root["RVDocumentCue"] = [data]

                        # an existing file might need the order of all the proceeding elements shifted
                        self.currentOrder += 1
                        # no return

                    @staticmethod
                    def header(headerName, *args, headerColour=None):
                        if headerColour:
                            if propresenter.utils.colorUtil.checks.hex(headerColour):
                                headerColour = " ".join(
                                    (propresenter.utils.colorUtil.conversion.hex_to_hsl(headerColour) + ("1",))[:4])
                            elif type(headerColour) == tuple:
                                if all(map(propresenter.utils.colorUtil.checks.between0_255, headerColour)):
                                    headerColour = " ".join((propresenter.utils.colorUtil.conversion.rgb_to_hsl(
                                        headerColour[:3]) + headerColour[3:] + (1,))[:4])
                                elif all(map(propresenter.utils.colorUtil.checks.between0_1, headerColour)):
                                    headerColour = " ".join((headerColour + (1,))[:4])
                        if not headerColour:
                            headerColour = "0.894117647058824 0.894117647058824 0.894117647058824 1"

                        root = elem.data["array"][0]
                        data = {"@displayName": headerName,
                                "@UUID": uuid(),
                                "@actionType": 0,
                                "@enabled": 1,
                                "@timeStamp": 0,
                                "@delayTime": 0,
                                "@timerType": 0,
                                "@countDownToTimeFormat": 0,
                                "@allowOverrun": "false",
                                "@timerUUID": "00000000-0000-0000-0000-000000000000",
                                "@endTime": "No Limit",
                                "@duration": "00:00:00",
                                "@color": headerColour,
                                "@__order__": self.currentOrder + 1,
                                }
                        if "RVHeaderCue" in root:
                            root["RVHeaderCue"].append(data)
                        else:
                            root["RVHeaderCue"] = [data]

                        # an existing file might need the order of all the proceeding elements shifted
                        self.currentOrder += 1
                        return Header(root["RVHeaderCue"][-1])

                elem.add = add()

        class Document(Element):
            pass

        class Header(Element, propresenter.utils.HSLa_Handler):
            def __init__(self, *args):
                HSLa_Store = self.data["@color"]

        class Media(Element):
            # Contains RVVideoElement, RVImageElement
            def __init__(self, *args):
                print("  INIT MEDIA")

            pass

        class Audio(Element):
            def __init__(self, *args):
                print("  INIT AUDIO")

        class Children(list):
            def __init__(self, arg: OrderedDict):
                self.data = arg
                # Hardcode the types of elements, not like they'll change?
                _documents = list(map(Document, self.data.get("RVDocumentCue", [])))
                __RVPlaylistNode = self.data.get("RVPlaylistNode", [])
                _playlists = list(map(Playlist, filter(lambda e: e["@type"] == "2", __RVPlaylistNode)))
                _folders = list(map(Folder, filter(lambda e: e["@type"] == "3", __RVPlaylistNode)))
                _headers = list(map(Header, self.data.get("RVHeaderCue", [])))
                _media = list(map(Media, self.data.get("RVMediaCue", [])))
                _audio = list(map(Audio, self.data.get("RVAudioCue", [])))
                list.__init__(self, sorted(_documents + _playlists + _folders + _headers + _media + _audio,
                                           key=lambda o: o.order))

            def __getitem__(self, item):
                if type(item) == int:
                    # return Element(list.__getitem__(self, item))
                    return list.__getitem__(self, item)
                elif propresenter.utils.validUUID(item):
                    item = item.upper()
                    if item not in [s["@UUID"].upper() for s in self]:
                        return None
                    return Element(next(filter(lambda element: element["@UUID"].upper() == item, self)))
                else:
                    raise ValueError("Invalid UUIDv4")



                    # def __init__(self, obj: OrderedDict = OrderedDict()):
                    #     self.obj = self._propertyGrp.obj = obj
                    #     if not any(obj):
                    #         self.changeUUID(updateReferences=False)
                    #     self.fill = self.fill()
                    #     self.border = self.border()
                    #     self.shadow = self.shadow()
                    #
                    # class _propertyGrp:
                    #     # This is the wrong way to go about, but hey?
                    #     pass

        self.children = Children(self.data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0])
        # print("RCHILDREN", self.data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0])
        # print(" CHILDREN", self.children)
        print("LOADED")

        class add:
            @staticmethod
            def folder(folderName, **kwargs):
                typeNumber = kwargs.get("typeNumber", 2)  # hide the typeNumber from autocompletes of development IDEs

                root = self.data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0]
                data = {"@displayName": folderName, "@UUID": uuid(), "@smartDirectoryURL": "",
                        "@modifiedDate": getDateString(), "@type": typeNumber, "@isExpanded": "true",
                        "@hotFolderType": "2", "@__order__": self.currentOrder + 1,
                        "array": [
                            {
                                "@rvXMLIvarName": "children",
                                "@__order__": self.currentOrder + 2
                            }, {

                                "@rvXMLIvarName": "events",
                                "@__order__": self.currentOrder + 3
                            }
                        ]}
                if "RVPlaylistNode" in root:
                    root["RVPlaylistNode"].append(data)
                else:
                    root["RVPlaylistNode"] = [data]

                # an existing file might need the order of all the proceeding elements shifted
                self.currentOrder += 3
                return Folder(root["RVPlaylistNode"][-1])

            @staticmethod
            def playlist(playlistName):
                # format is exactly the same, except that playlists have a type number of 3
                return Playlist(self.add.folder(playlistName, typeNumber=3).data)

        self.add = add()
