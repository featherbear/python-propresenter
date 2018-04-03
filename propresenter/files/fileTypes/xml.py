# import xmltodict
from propresenter.files import Cxmltodict as xmltodict


class File():
    filePath = None
    _currentOrder = 0

    def __init__(self, filePath: str = None, force_list: tuple = ()):
        if filePath:
            self.filePath = filePath

        with open(self.filePath, "r", encoding="utf-8") as f:
            self._data, self._currentOrder = xmltodict.parse(f.read(), force_list=force_list, ordered_mixed_children=True)

    def save(self, filePath: str = None):
        filePath = filePath if filePath else self.filePath
        if not filePath:
            raise ValueError("No file path set!")
        with open(filePath, "w") as f:
            f.write(xmltodict.unparse(self._data, pretty=True, ordered_mixed_children=True))
            print("SAVED TO", f.name)
