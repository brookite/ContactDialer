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
    def __init__(self, path):
        self._path = path
        self._vcard = None
        self._vcards = []
        self._container = []

    def loaded(self):
        return self._vcard is not None
    
    def load(self, indexer):
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

    def get_contact_by_vcard(self, vcard):
        if vcard in self._vcards:
            i = self._vcards.index(vcard)
            return i, self._container[i]
        else:
            return None, None

    def __eq__(self, other):
        if isinstance(other, str):
            return self._path == other
        else:
            return super().__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return get_filename(self._path)


class AppCore:
    def __init__(self):
        self._indexer = pyvcard.vCardIndexer()
        self._vcards = []

        self.settings = JSONSettings(nobuffer=True)
        self.settings.create("opened", [])

    def load_vcardinfo(self, path):
        file = ContactFile(path)
        self._vcards.append(file)
        return file

    def fetch_vcard(self, file):
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

    def get(self, file):
        if isinstance(file, int):
            return self._vcards[file]
        elif isinstance(file, str):
            return self._vcards[self._vcards.index(file)] 
    
    def get_index(self, file):
        return self._vcards.index(file)

    def vcard_tree(self, files=[]):
        if isinstance(files, str):
            files = [files]

        tree = {}
        for file in self._vcards:
            tree[str(file)] = file.container
        return tree   

    def route(self, file, index):
        file = self.get(file)
        return file.container[index]
