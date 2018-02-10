#import xmltodict
import Cxmltodict as xmltodict

class File():
    filePath = None

    def __init__(self, filePath: str = None, force_list: tuple = ()):
        if filePath:
            self.filePath= filePath

        with open(self.filePath, "r", encoding="utf-8") as f:
            self.data = xmltodict.parse(f.read(), force_list=force_list, ordered_mixed_children=True)

    def save(self):
        with open(self.filePath, "w") as f:
            f.write(xmltodict.unparse(self.data))
