import os.path
import urllib.parse
from collections import OrderedDict

import mutagen

from .xml import File as XML
from .. import utils


class File(XML):
    def __init__(self, filePath: str = None):
        if filePath:
            XML.__init__(self, filePath, ("array", "RVPlaylistNode", "RVDocumentCue", "RVHeaderCue"))
        else:
            self._data = {
                "RVPlaylistDocument": {
                    "@versionNumber": 600,
                    "@os": 1,
                    "@buildNumber": 6016,
                    "RVPlaylistNode": [{
                        "@displayName": "root",
                        "@UUID": utils.UUID.generateUUID(),
                        "@smartDirectoryURL": "",
                        "@modifiedDate": utils.getDateString(),
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
                _obj._data = args[0]
                return _obj

            def __repr__(self):
                return self.__class__.__name__ + '("%s")' % self.name

            @property
            def order(self):
                return self._data["@__order__"]

            @property
            def name(self):
                return self._data["@displayName"]

            @name.setter
            def name(self, name):
                self._data["@displayName"] = name

        class Folder(Element):
            @property
            def children(self):
                return Children(self._data["array"][0])

            def __init__(elem, *args):
                class add:
                    @staticmethod
                    def _generateFolderOrHeader(name, typeNumber):
                        # typeNumber = 2 | FOLDER
                        # typeNumber = 3 | PLAYLIST
                        root = elem._data["array"][0]
                        data = {"@displayName": name,
                                "@UUID": utils.UUID.generateUUID(),
                                "@smartDirectoryURL": "",
                                "@modifiedDate": utils.getDateString(),
                                "@type": typeNumber,
                                "@isExpanded": True,
                                "@hotFolderType": "2",
                                "@__order__": self._currentOrder + 1,
                                "array": [
                                    {
                                        "@rvXMLIvarName": "children",
                                        "@__order__": self._currentOrder + 2
                                    }, {

                                        "@rvXMLIvarName": "events",
                                        "@__order__": self._currentOrder + 3
                                    }
                                ]}
                        if "RVPlaylistNode" in root:
                            root["RVPlaylistNode"].append(data)
                        else:
                            root["RVPlaylistNode"] = [data]

                        self._currentOrder += 3
                        return root["RVPlaylistNode"][-1]





                    @staticmethod
                    def folder(folderName):
                        return Folder(add._generateFolderOrHeader(folderName,2))

                    @staticmethod
                    def playlist(playlistName):
                        return Playlist(add._generateFolderOrHeader(playlistName, 3))


                elem.add = add()

        class Playlist(Element):
            @property
            def children(self):
                return Children(self._data["array"][0])

            def __init__(elem, *args):
                class add:
                    @staticmethod
                    def audio(audioPath, name=None):
                        __mediaObject = mutagen.File(audioPath)
                        if __mediaObject is None:
                            raise Exception("Bad media file")
                        __mediaObjectDuration = int(__mediaObject.info.length * 600)
                        __displayName = (name + ".") if name else os.path.basename(audioPath)

                        root = elem._data["array"][0]
                        data = {
                            "@UUID": utils.UUID.generateUUID(),
                            "@displayName": __displayName,
                            "@actionType": 0,  # ???
                            "@enabled": 1,  # ???
                            "@timeStamp": 0,  # ???
                            "@delayTime": 0,  # ???
                            "@tags": "",  # ???
                            "@nextCueUUID": "00000000-0000-0000-0000-000000000000",  # ???
                            "behavior": "1",  # ???
                            "alignment": "4",  # ???
                            "dateAdded": "",  # ???
                            "@__order__": self._currentOrder + 1,
                            "RVAudioElement": [{
                                "@rvXMLIvarName": "element",
                                "@volume": 1,
                                "@playRate": 1,
                                "@loopBehaviour": 0,
                                "@audioType": 0,  # ???
                                "@inPoint": 0,
                                "@outPoint": __mediaObjectDuration,
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
                        self._currentOrder += 1
                        # no return

                    @staticmethod
                    def video(videoPath, name=None):
                        __mediaObject = mutagen.File(videoPath)
                        if __mediaObject is None:
                            raise Exception("Bad media file")
                        __mediaObjectDuration = int(__mediaObject.info.length * 600)  # timeScale = 600
                        __displayName = (name + ".") if name else os.path.basename(videoPath)

                        root = elem._data["array"][0]
                        data = {
                            "@UUID": utils.UUID.generateUUID(),
                            "@displayName": __displayName,
                            "@actionType": 0,
                            "@enabled": 1,
                            "@timeStamp": 0,
                            "@delayTime": 0,
                            "@tags": "",
                            "@nextCueUUID": "00000000-0000-0000-0000-000000000000",
                            "@behavior": 2,
                            "@alignment": 4,
                            "@dateAdded": "",
                            "@__order__": self._currentOrder + 1,
                            "RVVideoElement": [{
                                "@rvXMLIvarName": "element",
                                "@UUID": None,

                                "@displayName": os.path.basename(videoPath),
                                "@source": urllib.parse.quote(videoPath),

                                "@scaleBehavior": 0,
                                # 0 - Scale to Fit
                                # 1 - Scale to Fill
                                # 2 - Stretch to Fit

                                "@flippedHorizontally": "false",
                                "@flippedVertically": "false",

                                "@audioVolume": "1",
                                "@playRate": "1",
                                "@playbackBehavior": "0",

                                "@timeScale": "600",  # WHY THOUGH???
                                "@inPoint": "0",  #
                                "@outPoint": __mediaObjectDuration,  #
                                "@endPoint": __mediaObjectDuration,  #

                                "@fieldType": "0",

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
                                # "@manufactureURL": "",
                                # "@manufactureName": "",
                                # "@format": "",
                                # "@scaleSize": "{1.0, 1.0}",
                                # "@imageOffset": "{0.0, 0.0}",
                                # "@frameRate": "23.9760246276855"
                                # "@naturalSize": "{1920, 1080}",

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

                        self._currentOrder += 1

                    @staticmethod
                    def image(imagePath, name=None):
                        __displayName = (name + ".") if name else os.path.basename(imagePath)

                        root = elem._data["array"][0]
                        data = {
                            "@UUID": utils.UUID.generateUUID(),
                            "@displayName": __displayName,
                            "@actionType": 0,  # ???
                            "@enabled": 1,
                            "@timeStamp": 0,  # ???
                            "@delayTime": 0,  # ???
                            "@tags": "",
                            "@nextCueUUID": "00000000-0000-0000-0000-000000000000",
                            "@behavior": 2,  # ???
                            "@alignment": 4,
                            # 0 1 2
                            # 3 4 5
                            # 6 7 8
                            "@dateAdded": "",  # ???
                            "@__order__": self._currentOrder + 1,
                            "RVImageElement": [{
                                "@rvXMLIvarName": "element",
                                "@UUID": None,
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
                                "@manufactureURL": "",
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
                        self._currentOrder += 1
                        # return

                    @staticmethod
                    def document(documentPath):
                        root = elem._data["array"][0]
                        data = {
                            "@UUID": utils.UUID.generateUUID(),
                            "@displayName": os.path.basename(documentPath),  # doesn't matter
                            "@filePath": urllib.parse.quote(documentPath),
                            "@selectedArrangementID": "",
                            "@actionType": 0,  # ???
                            "@enabled": 1,
                            "@timeStamp": 0,  # ???
                            "@delayTime": 0,  # ???
                            "@__order__": self._currentOrder + 1,
                        }
                        if "RVDocumentCue" in root:
                            root["RVDocumentCue"].append(data)
                        else:
                            root["RVDocumentCue"] = [data]

                        # an existing file might need the order of all the proceeding elements shifted
                        self._currentOrder += 1
                        # no return

                    @staticmethod
                    def header(headerName, *args, headerColour=None):
                        if headerColour:
                            if utils.colorUtil.checks.hex(headerColour):
                                headerColour = " ".join(
                                    (utils.colorUtil.conversion.hex_to_hsl(headerColour) + ("1",))[:4])
                            elif type(headerColour) == tuple:
                                if all(map(utils.colorUtil.checks.between0_255, headerColour)):
                                    headerColour = " ".join((utils.colorUtil.conversion.rgb_to_hsl(
                                        headerColour[:3]) + headerColour[3:] + (1,))[:4])
                                elif all(map(utils.colorUtil.checks.between0_1, headerColour)):
                                    headerColour = " ".join((headerColour + (1,))[:4])
                        if not headerColour:
                            headerColour = "0.894117647058824 0.894117647058824 0.894117647058824 1"

                        root = elem._data["array"][0]
                        data = {"@displayName": headerName,
                                "@UUID": utils.UUID.generateUUID(),
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
                                "@__order__": self._currentOrder + 1,
                                }
                        if "RVHeaderCue" in root:
                            root["RVHeaderCue"].append(data)
                        else:
                            root["RVHeaderCue"] = [data]

                        # an existing file might need the order of all the proceeding elements shifted
                        self._currentOrder += 1
                        return Header(root["RVHeaderCue"][-1])

                elem.add = add()

        class Document(Element):
            pass

        class Header(Element, utils.HSLa_Handler):
            def __init__(self, *args):
                self.HSLa_Store = self._data["@color"]

        class Media(Element):
            # Contains RVVideoElement, RVImageElement
            def __init__(self, *args):
                print("  INIT MEDIA")

                '''
                # Transitions

                CUT
                transitionType: 10

                DISSOLVE
                transitionType: 0
                transitionDuration: 0.0-5.0

                FADE BLACK
                transitionType: 7
                transitionDuration: 0.0-5.0

                FLIP
                transitionType: 2            
                transitionDuration: 0.0-5.0

                SWAP
                transitionType: 4
                transitionDuration: 0.0-5.0

                CUBE
                transitionType: 1
                transitionDuration: 0.0-5.0

                DOOR
                transitionType: 3
                transitionDuration: 0.0-5.0

                IRIS
                transitionType: 8
                transitionDuration: 0.0-5.0

                RIPPLE
                transitionType: 6
                transitionDuration: 0.0-5.0

                PUSH
                transitionType: UP 133, RIGHT 130, DOWN 132, LEFT 131
                transitionDuration: 0.0-5.0

                WIPE
                transitionType: LEFT 114, RIGHT 113, DOWN 111, UP 116, TOPRIGHT 115, BOTTOMRIGHT 110, BOTTOMLEFT 112, TOPLEFT 117
                transitionDuration: 0.0-5.0

                COVER
                transitionType: LEFT 124, RIGHT 123, DOWN 121, UP 126, TOPRIGHT 125, BOTTOMRIGHT 120, BOTTOMLEFT 122, TOPLEFT, 127
                transitionDuration: 0.0-5.0

                REVEAL
                transitionType: LEFT 144, RIGHT 143, DOWN 141, UP 146, TOPRIGHT 145, BOTTOMRIGHT 140, BOTTOMLEFT 142, TOPLEFT, 147
                transitionDuration: 0.0-5.0

                FLY IN
                transitionType: LEFT 96, RIGHT 94, DOWN 92, UP 98, TOPRIGHT 97, BOTTOMRIGHT 91, BOTTOMLEFT 93, TOPLEFT 99, CENTER 95
                transitionDuration: 0.0-5.0
                motionEnabled: true/false
                motionSpeed: 10-[speed] => 0.0-10

                ZOOM IN
                transitionType: LEFT 106, RIGHT 104, DOWN 102, UP 108, TOPRIGHT 107, BOTTOMRIGHT 101, BOTTOMLEFT 103, TOPLEFT 109, CENTER 105
                transitionDuration: 0.0-5.0
                motionEnabled: true/false
                motionSpeed: 10-[speed] => 0.0-10
                '''  # Transition #

                class effects(list):
                    pass

                '''
                # Effects

                #Adjust Color
                {
                "@UUID": "D4C199A9-64D7-4CCB-8C26-443E7A9C5C03",
                    "@displayName": "Adjust Color",
                    "array": [{
                        "@rvXMLIvarName": "effectVariables",
                      "RVEffectFloatVariable": [{
                      "@name": "hue"    ,
                          "@type" : "1",
                "@min" : "-3.14159274",
                "@max": "3.14159274",
                "@defValue": "0",
                "@value": "0"
                      },{
                          "@name": "saturation","@type":"1","@min":"0","@max":"2","@defValue":"1","@value":"1"

                      },
                          {"@name":"brightness","@type":"1","@min":"-1","@max":"1","@defValue":"0","@value":"0"},
                          {"@name":"contrast","@type":"1","@min":"0","@max":"2","@defValue":"1","@value":"1"}]
                    }]
                }

                #Blur
                {
                "@UUID":"D84CE4A3-D1C3-4F7C-AA75-4C645A3621F2","@displayName":"Blur",
                    "array": [{
                "@rvXMLIvarName":"effectVariables",
                        "RVEffectFloatVariable": [{
                "@name":"blurAmount","@type":"1","@min":"0","@max":"1","@defValue":"0.5","@value":"0.5"
                        }]
                    }]
                }

                #Color Filter
                {
                "@UUID":"85A535EF-4EFC-4105-B8C7-C65C53376B87","@displayName":"Color Filter",
                    "array": [{
                "@rvXMLIvarName":"effectVariables",
                        "RVEffectFloatVariable": [{
                "@name":"pickedColor","@type":"2","@value":"1 1 1 1"
                        }]
                    }]
                }

                #Color Invert
                {
                "@UUID":"EDF55F11-1A1E-4BF3-9718-FA2D3731626D","@displayName":"Color Invert",
                    "array": [{
                "@rvXMLIvarName":"effectVariables"
                    }]
                }

                #Edge Blur
                {
                "@UUID":"AF83B133-D6A1-487C-BD9E-8579FA49B4E0","@displayName":"Edge Blur",
                    "array": [{
                        "@rvXMLIvarName": "effectVariables",
                        "RVEffectFloatVariable": [{
                            "@name": "blurAmount", "@type": "1", "@min": "0", "@max": "1", "@defValue": "0.5", "@value": "0.5"
                        },{
                "@name":"blurRadius","@type":"1","@min":"0","@max":"1","@defValue":"0.5","@value":"0.25"
                        }]
                    }]
                }

                #Gray Invert
                {
                "@UUID":"4FDA3849-C39D-4269-AADA-B963944900B7","@displayName":"Gray Invert",
                    "array": [{
                "@rvXMLIvarName":"effectVariables"
                    }]
                }

                #Halftone
                {
                "@UUID":"ADF80D5E-FD27-47BD-AFA6-8D4167364567","@displayName":"Halftone",
                    "array": [{
                        "@rvXMLIvarName": "effectVariables",
                        "RVEffectFloatVariable": [{
                            "@name":"sharpnessValue","@type":"1","@min":"0","@max":"1","@defValue":"0.5","@value":"0.5"
                        },{
                "@name":"gcrValue","@type":"1","@min":"0","@max":"2","@defValue":"1","@value":"1"
                        },{
                "@name":"ucrValue","@type":"1","@min":"0","@max":"1","@defValue":"0.5","@value":"0.5"
                        }]
                    }]
                }

                #Heat Signature
                {
                "@UUID":"F3F254AF-BF83-412D-B802-51E42A25FDF9","@displayName":"Heat Signature",
                    "array": [{
                "@rvXMLIvarName":"effectVariables"
                    }]
                }


                #Old Film
                {
                "@UUID":"1E5BAD9B-205C-404D-869B-2B38C33FD28F","@displayName":"Old Film",
                    "array": [{
                        "@rvXMLIvarName": "effectVariables",
                        "RVEffectFloatVariable": [{
                            "@name": "sharpnessValue", "@type": "1", "@min": "0", "@max": "1", "@defValue": "0.5", "@value": "0.5"
                        },{
                "@name":"gcrValue","@type":"1","@min":"0","@max":"2","@defValue":"1","@value":"1"
                        },{
                "@name":"ucrValue","@type":"1","@min":"0","@max":"1","@defValue":"0.5","@value":"0.5"
                        }]
                    }]
                }

                #Sepia
                {
                "@UUID":"06157C8E-D971-4F06-9ECA-2663664E22A6","@displayName":"Sepia",
                    "array": [{
                "@rvXMLIvarName":"effectVariables"
                    }]
                }

                #Vignette
                {
                "@UUID":"42E83016-41DC-43AB-8061-9A93256DDA46","@displayName":"Vignette",
                    "array": [{
                "@rvXMLIvarName":"effectVariables",
                        "RVEffectFloatVariable": [{
                "@name":"radius","@type":"1","@min":"0","@max":"100","@defValue":"50","@value":"50"
                        }]
                    }]
                }
                '''  # Effects

                self.effects = effects()

            pass

        class Audio(Element):
            def __init__(self, *args):
                print("  INIT AUDIO")

        class Children(list):
            def __init__(self, arg: OrderedDict):
                self._data = arg
                # Hardcode the types of elements, not like they'll change?
                _documents = list(map(Document, self._data.get("RVDocumentCue", [])))
                __RVPlaylistNode = self._data.get("RVPlaylistNode", [])
                _playlists = list(map(Playlist, filter(lambda e: e["@type"] == "2", __RVPlaylistNode)))
                _folders = list(map(Folder, filter(lambda e: e["@type"] == "3", __RVPlaylistNode)))
                _headers = list(map(Header, self._data.get("RVHeaderCue", [])))
                _media = list(map(Media, self._data.get("RVMediaCue", [])))
                _audio = list(map(Audio, self._data.get("RVAudioCue", [])))
                list.__init__(self, sorted(_documents + _playlists + _folders + _headers + _media + _audio,
                                           key=lambda o: o.order))

            def __getitem__(self, item):
                if type(item) == int:
                    # return Element(list.__getitem__(self, item))
                    return list.__getitem__(self, item)
                elif utils.UUID.validUUID(item):
                    item = item.upper()
                    if item not in [s["@UUID"].upper() for s in self]:
                        return None
                    return Element(next(filter(lambda element: element["@UUID"].upper() == item, self)))
                else:
                    res = list(filter(lambda s: s.name == item, self))
                    if res: return res.pop()
                    raise ValueError("Invalid UUIDv4, or Item or Folder does not exist")

            def __contains__(self, item):
                if type(item) == int:
                    # return Element(list.__getitem__(self, item))
                    try:
                        list.__getitem__(self, item)
                        return True
                    except:
                        return False

                elif utils.UUID.validUUID(item):
                    item = item.upper()
                    return False if item not in [s["@UUID"].upper() for s in self] else True
                else:
                    return len(list(filter(lambda s: s.name == item, self))) != 0

        self.children = Children(self._data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0])
        # print("RCHILDREN", self._data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0])
        # print(" CHILDREN", self.children)

        class add:
            @staticmethod
            def folder(folderName, **kwargs):
                typeNumber = kwargs.get("typeNumber", 2)  # hide the typeNumber from autocompletes of development IDEs

                root = self._data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0]
                data = {"@displayName": folderName, "@UUID": utils.UUID.generateUUID(), "@smartDirectoryURL": "",
                        "@modifiedDate": utils.getDateString(), "@type": typeNumber, "@isExpanded": "true",
                        "@hotFolderType": "2", "@__order__": self._currentOrder + 1,
                        "array": [
                            {
                                "@rvXMLIvarName": "children",
                                "@__order__": self._currentOrder + 2
                            }, {

                                "@rvXMLIvarName": "events",
                                "@__order__": self._currentOrder + 3
                            }
                        ]}
                if "RVPlaylistNode" in root:
                    root["RVPlaylistNode"].append(data)
                else:
                    root["RVPlaylistNode"] = [data]

                # an existing file might need the order of all the proceeding elements shifted
                self._currentOrder += 3
                return Folder(root["RVPlaylistNode"][-1])

            @staticmethod
            def playlist(playlistName):
                # format is exactly the same, except that playlists have a type number of 3
                return Playlist(self.add.folder(playlistName, typeNumber=3)._data)

        self.add = add()
