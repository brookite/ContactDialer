import json
import os

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
    
    def __getitem__(self, key):
        return self._model[key]

    def __contains__(self, key):
        return key in self._model

    def __setitem__(self, key, value):
        self._model[key] = value
        if self.nobuffer:
            self.save()

    def resolve_object(self, *keys):
        if len(keys) >= 1:
            branch = self[keys[0]]
            for k in keys[1:]:
                branch = branch[k]
            return branch

    def add_to_list(self, key, value, unique=False):
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

    def create(self, key, value):
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
            json.dump(self._model, fobj)
            