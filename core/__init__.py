from core import contact
import pyvcard
from .utils import get_filename
from .settings import JSONSettings


def _get_vcard_name(owner):
    if len(owner.name.values):
        return repr(owner.name.value)
    else:
        return "UNNAMED CONTACT"


class AbstractContactBundle:
    pass


class ContactFile(AbstractContactBundle):
    def __init__(self, path):
        self._path = path

    def __str__(self):
        return utils.get_filename(self._path)


class AppCore:
    def __init__(self):
        self._indexer = pyvcard.vCardIndexer()
        self._vcards = {}  # raw vcards
        self._tree = {}  # tree with contact objects
        self._stored_tree = None
        self.settings = JSONSettings(nobuffer=True)
        self.settings.create("opened", [])
        self._bundlesinfo = {}
        contact.Contact.__repr__ = _get_vcard_name # contact representation on view

    def set_temp_tree(self, tree):
        self._stored_tree = self._tree
        self._tree = tree

    def revert_tree(self):
        if self._stored_tree:
            self._tree = self._stored_tree
            self._stored_tree = None

    def load_vcardinfo(self, path):
        file = ContactFile(path)
        self._vcards[str(file)] = ["unloaded", path]
        self._bundlesinfo[str(file)] = file

    def fetch_vcard(self, path):
        bundle = pyvcard.openfile(path, encoding="utf-8", indexer=self._indexer)
        file = ContactFile(path)
        self._vcards[str(file)] = list(bundle.vcards())
        self._bundlesinfo[str(file)] = file
        self.settings.add_to_list("opened", path, unique=True)

    def number_to_filename(self, file: int):
        return list(self._vcards.keys())[file]

    def is_unloaded(self, path):
        if len(self._vcards[path]) == 2:
            return self._vcards[path][0] == "unloaded"
        return False

    def vcard_tree(self, files=None):
        if isinstance(files, str):
            files = [files]
        elif not files:
            files = []

        if self._vcards.keys() == self._tree.keys() and not files:
            return self._tree
        else:
            keys_to_update = set(self._vcards.keys()).symmetric_difference(self._tree.keys())
            for key in list(keys_to_update) + files:
                if not self.is_unloaded(key):
                    self._tree[key] = list(map(lambda vcard: contact.Contact(vcard), self._vcards[key]))
                else:
                    self._tree[key] = []
            return self._tree

    def route(self, file, index):
        file = self.number_to_filename(file)
        return self._tree[file][index]
