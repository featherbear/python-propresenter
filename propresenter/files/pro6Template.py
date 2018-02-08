from .xml import Stub
"""
Interesting things
RVTemplateDocument  versionNumber, os, buildNumber
"""
class slides(list):
    def add(self):
        """
        Create a blank slide
        :return:
        """
        pass
    def clear(self):
        """
        Delete all slides
        :return:
        """
        pass

class File():
    # Reminder that variables act as pointers instead of creating a new copy!

    def __init__(self, fileName: str, fileDirectory: str):
        self._file = Stub(fileName, fileDirectory)
        self._root = self._file.data["RVPresentationDocument"] if "RVPresentationDocument" in self._file.data else self._file.data["RVTemplateDocument"]
        print(type(self.slides))

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
    def slides(self):

        return slides(self._root["array"]["RVDisplaySlide"])
