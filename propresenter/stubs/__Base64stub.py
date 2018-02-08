import propresenter
from propresenter.utils import xml

class Stub():
    fileName = None

    def __init__(self):
        try:
            self.data = xml.read(self.fileName, propresenter.appDataLocation)
        except:
            raise

    def save(self):
        try:
            xml.write(self.data, self.fileName, propresenter.appDataLocation)
            return True
        except Exception as e:
            print(e)
            return False
