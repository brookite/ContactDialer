import json
import os
from typing import Union

class JSONSettings:
    def __init__(self, nobuffer=True):
        self.nobuffer = nobuffer
        self._path = os.path.expanduser("~/.cntdialer")
        if os.path.exists(self._path):
            with open(self._path, "r", encoding="utf-8") as fobj:
                self._model = json.load(fobj)
        else:
            self._model = {}
            self.save()

    def __getitem__(self, key: str):
        return self._model[key]

    def __contains__(self, key: str):
        return key in self._model

    def __setitem__(self, key: str, value):
        self._model[key] = value
        if self.nobuffer:
            self.save()

    def resolve_object(self, *keys):
        if len(keys) >= 2:
            branch = self[keys[0]]
            for k in keys[1:-1]:
                branch = branch[k]
            return branch
        return branch

    def add_to_list(self, key: Union[str, tuple], value, unique=False):
        if isinstance(key, tuple):
            branch = self.resolve_object(*key)
        else:
            branch = self
        if key not in branch:
            branch[key] = []
        if value not in branch[key] or (not unique):
            branch[key].append(value)
        if self.nobuffer:
            self.save()
    
    def remove_from_list(self, key: Union[str, tuple], value):
        if isinstance(key, tuple):
            branch = self.resolve_object(*key)
        else:
            branch = self
        if key not in branch:
            return
        branch[key].remove(value)
        if self.nobuffer:
            self.save()

    def create(self, key: Union[str, tuple], value):
        if isinstance(key, tuple):
            branch = self.resolve_object(*key)
        else:
            branch = self
        if key not in branch:
            branch[key] = value
        if self.nobuffer:
            self.save()

    def __iter__(self):
        return iter(self._model)

    def save(self):
        with open(self._path, "w", encoding="utf-8") as fobj:
            json.dump(self._model, fobj, ensure_ascii=False)
