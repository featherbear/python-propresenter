import xmltodict
import os

class File():
    fileName = None
    fileDirectory = None

    def __init__(self, fileName: str = None, fileDirectory: str = None):
        if fileName and fileDirectory:
            self.fileName = fileName
            self.fileDirectory = fileDirectory

        with open(os.path.join(self.fileDirectory, self.fileName), "r", encoding="utf-8") as f:
            self.data = xmltodict.parse(f.read(), force_list=("RVDisplaySlide"))

    def save(self):
        with open(os.path.join(self.fileDirectory, self.fileName), "w") as f:
            f.write(xmltodict.unparse(self.data))
