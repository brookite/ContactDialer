from typing import Dict, List, Union
import pyvcard
from .utils import get_filename
from .settings import JSONSettings
from .contact import Contact


def get_vcard_name(owner):
    if not owner:
        return "UNNAMED CONTACT"

    if len(owner.name.values):
        return repr(owner.name.value)
    else:
        return "UNNAMED CONTACT"

class ContactFile:
    _vcards: List["pyvcard.vCard"]
    _path: str
    _container: List[Contact]

    def __init__(self, path: str):
        self._path = path
        self._vcard = None
        self._vcards = []
        self._container = []

    def loaded(self):
        return self._vcard is not None
    
    def load(self, indexer: pyvcard.vCardIndexer):
        if not self.loaded():
            self._vcard = pyvcard.openfile(self._path, encoding="utf-8", indexer=indexer)
            self._vcards = list(self._vcard.vcards())
            self._container = list(map(Contact, self._vcards))

    @property
    def container(self):
        return self._container
    
    @property
    def path(self):
        return self._path

    @property
    def vcards(self):
        return self._vcards

    def get_contact_by_vcard(self, vcard: "pyvcard.vCard"):
        if vcard in self._vcards:
            i = self._vcards.index(vcard)
            return i, self._container[i]
        else:
            return None, None

    def __eq__(self, other: "ContactFile"):
        if isinstance(other, str):
            return self._path == other
        else:
            return super().__eq__(other)

    def __ne__(self, other: "ContactFile"):
        return not self.__eq__(other)

    def __str__(self):
        return get_filename(self._path)


class AppCore:
    _indexer: pyvcard.vCardIndexer
    _vcards: List[ContactFile]
    settings: JSONSettings

    def __init__(self):
        self._indexer = pyvcard.vCardIndexer()
        self._vcards = []

        self.settings = JSONSettings(nobuffer=True)
        self.settings.create("opened", [])

    def load_vcardinfo(self, path: str) -> ContactFile:
        file = ContactFile(path)
        self._vcards.append(file)
        return file

    def fetch_vcard(self, file: ContactFile):
        if isinstance(file, str):
            if file not in self._vcards:
                file = self.load_vcardinfo(file)
                file.load(self._indexer)
            else:
                file = self._vcards[self._vcards.index(file)]
                file.load(self._indexer)
        else:
            file.load(self._indexer)
        self.settings.add_to_list("opened", file.path, unique=True)

    def get(self, file: Union[str, int]) -> ContactFile:
        if isinstance(file, int):
            return self._vcards[file]
        elif isinstance(file, str):
            return self._vcards[self._vcards.index(file)] 
    
    def get_index(self, file: ContactFile) -> int:
        return self._vcards.index(file)

    def vcard_tree(self, files: List=[]) -> Dict:
        if isinstance(files, str):
            files = [files]

        tree = {}
        for file in self._vcards:
            tree[str(file)] = file.container
        return tree   

    def route(self, file: int, index: int) -> List[Contact]:
        file = self.get(file)
        return file.container[index]
