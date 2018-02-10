# Root PlaylistNode UUID is caps
#   Folder PlaylistNode UUID is lowercase
#       array-children
#           array[RVPlaylistNode] - lowercase UUID | actual playlist
#               array-children
#                   array[RVDocumentCue] - uppercase UUID ### This UUID doesn't relate to anything; The file is loaded by filepath and arrangementID
#               array-events
#       array-events

from collections import OrderedDict

import xmltodict
from uuid import uuid4
from .xml import File as XML
from datetime import datetime
import propresenter.utils

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
            self.data = {
                "RVPlaylistDocument":  {
                    "@versionNumber": 600,
                    "@os": 1,
                    "@buildNumber": 6016,
                    "RVPlaylistNode": [{
                        "@displayName": "root",
                        "@UUID": uuid(),
                        "@smartDirectoryURL": "",
                        "@modifiedDate": getDateString(),
                        "@type": 0, ######################
                        "@isExpanded": 0, #################
                        "@hotFolderType": 2, ################
                        "@rvXMLIvarName": "rootNode",
                        "array": [
                            OrderedDict({
                                "@rvXMLIvarName": "children",
                                "RVDocumentCue": []
                            }),OrderedDict({

                                "@rvXMLIvarName": "events"
                            })
                        ]
                    }],
                    "array": {
                        "@rvXMLIvarName": "deletions"
                    }
                }
            }

        class Element():
            def __new__(cls, arg):
                cls.data = arg
                return cls.data


        class Children(list):
            def __init__(self, arg: OrderedDict):
                self.data = arg
                # Hardcode the types of elements, not like they'll change?
                a= (self.data.get("RVDocumentCue", []) + self.data.get("RVPlaylistNode", []) + self.data.get("RVHeaderCue", []) + self.data.get("RVMediaCue", []) + self.data.get("RVAudioCue", []))
                list.__init__(self, sorted(a,key=lambda o: o["@__order__"]))

            def __getitem__(self, item):
                if type(item) == int:
                    #return Element(list.__getitem__(self, item))
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
        print("A",self.data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0])
        print("B",self.children)
        if self.children:
            print("C", self.children[0]["@displayName"])
            self.children[0]["@displayName"]="HAHA"
            print("D", self.children[0]["@displayName"])
            print("E", self.data["RVPlaylistDocument"]["RVPlaylistNode"][0]["array"][0])
            #f = Element(self.children[0])
            #print("F", f)









        class Folder:
            def __init__(self, *args, ):
                pass

        class Document:
            def __init__(self):
                pass

        class Header:
            def __init__(self):
                pass

        class Media:
            # Contains RVVideoElement, RVImageElement
            def __init__(self):
                pass
        class Audio:
            def __init__(self):
                pass



        xmltodict.unparse(self.data)


        print("LOADED")
