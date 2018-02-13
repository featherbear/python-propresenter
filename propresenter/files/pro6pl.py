# Root PlaylistNode UUID is caps
#   Folder PlaylistNode UUID is lowercase
#       array-children
#           array[RVPlaylistNode] - lowercase UUID | actual playlist
#               array-children
#                   array[RVDocumentCue] - uppercase UUID ### This UUID doesn't relate to anything; The file is loaded by filepath and arrangementID
#               array-events
#       array-events

from collections import OrderedDict
from datetime import datetime
from uuid import uuid4

import propresenter.utils
from .xml import File as XML

getDateString = lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")


def uuid():
    return str(uuid4()).upper()


"""
Interesting things
RVTemplateDocument  versionNumber, os, buildNumber
"""


class File(XML):
    # Reminder that variables act as pointers instead of creating a new copy!
    # TODO self.data
    # TODO self.filePath

    def __init__(self, filePath: str = None):
        if filePath:
            print("EXISTING FILE")
            XML.__init__(self, filePath, ("array", "RVPlaylistNode", "RVDocumentCue", "RVHeaderCue"))
        else:
            print("Created new playlist file")
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
                        "@type": 0,  ######################
                        "@isExpanded": 0,  #################
                        "@hotFolderType": 2,  ################
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
                obj = super(Element, cls).__new__(cls)
                obj.data = args[0]
                return obj

            def __repr__(self):
                return self.__class__.__name__ + '("%s")' % self.name
                #return str(self.data)

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

        class Playlist(Element):
            {"displayName": ": playlist 1 :",
             "UUID": "9280e80b-352d-4ac9-9cf5-847be42bcd3f",
             "smartDirectoryURL": "",
             "modifiedDate": "2018-02-10T13:25:24+s00:00",
             "type": "3",
             "isExpanded": "true", "hotFolderType": "2"}
            pass

        class Document(Element):
            {"UUID" : "49DC84D0-95B4-4C91-803A-2A2D4A644C3E",
            "displayName" : "You Hold Me Now.pro6",
            "filePath" : "D%3A%5CUsers%5CAndrew%5CDocuments%5CProPresenter6%5CYou%20Hold%20Me%20Now.pro6",
            "selectedArrangementID" : "C703E052-A20A-4491-A598-FD9A96D3CD7E",
            "actionType" : "0",
            "enabled" : "1",
            "timeStamp" : "0",
            "delayTime" : "0"}
            pass

        class Header(Element):
            {"UUID": "69B7E786-E532-41EF-9BE4-D92D60AEE560",
             "displayName": "New Header",
             "actionType": "0",
             "enabled": "1",
             "timeStamp": "0",
             "delayTime": "0",
             "duration": "00:00:00",
             "endTime": "No Limit",
             "timerType": "0",
             "countDownToTimeFormat": "0",
             "allowOverrun": "false",
             "color": "0.498039215686275 0 1 0.235294117647059",
             "timerUUID": "00000000-0000-0000-0000-000000000000"}

            def __init__(self, *args):
                print("  INIT HEADER")

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
        print("RCHILDREN", self.data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0])
        print(" CHILDREN", self.children)
        print("LOADED")


        class add:
            @staticmethod
            def folder(folderName):

                root = self.data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0]
                data = {"@displayName": folderName, "@UUID": uuid(), "@smartDirectoryURL": "",
                 "@modifiedDate": getDateString(), "@type": "2", "@isExpanded": "true", "@hotFolderType": "2", "@__order__": self.currentOrder+1,
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
                    root.append(data)
                else:
                    root["RVPlaylistNode"] = [data]

                self.currentOrder += 3

                #self.children.append(
                print(self.children)
            @staticmethod
            def playlist(playlistName):
                pass
        self.add = add()


