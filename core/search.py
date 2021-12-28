import pyvcard
from fuzzywuzzy import fuzz



class SearchEngine:
    def __init__(self, vcards, indexer: pyvcard.vCardIndexer):
        self._vcards = vcards
        self.indexer = indexer
        self._settings = {
            "case": False,
            "objects": ["phone", "email", "name"],
            "type": "contain",  # contain, equal, fuzzy
            "fuzzy_k": 80,
            "phone_constraints": "default"  # default, start, end, all
        }

    def set_parameters(self, **kwargs):
        for key in kwargs:
            self._settings[key] = kwargs[key]

    @property
    def settings(self):
        return self._settings

    def classified_tree(self, results, contact_tree):
        result_tree = {}
        for vcard in results:
            for key in self._vcards:
                if vcard in self._vcards[key]:
                    i = self._vcards[key].index(vcard)
                    if key not in result_tree:
                        result_tree[key] = []
                    result_tree[key].append(contact_tree[key][i])
        return result_tree

    def query(self, query: str):
        resultset = set()
        if self.settings["type"] != "fuzzy":
            if "name" in self.settings["objects"]:
                s = self.indexer.find_by_name(query, self.settings["case"], self.settings["type"] == "equal")
                resultset.update(s)
            if "phone" in self.settings["objects"]:
                phone_nums = set()
                if self.settings["phone_constraints"] in ["default", "all"]:
                    s = self.indexer.find_by_phone(query, self.settings["type"] == "equal", True)
                    phone_nums.update(s)
                if self.settings["phone_constraints"] in ["start", "all"]:
                    s = self.indexer.find_by_phone_startswith(query, True)
                    phone_nums.update(s)
                if self.settings["phone_constraints"] in ["end", "all"]:
                    s = self.indexer.find_by_phone_endswith(query, True)
                    phone_nums.update(s)
                resultset.update(phone_nums)
            if "email" in self.settings["objects"]:
                s = self.indexer.find_by_property("EMAIL", query, self.settings["type"] == "equal")
                resultset.update(s)
        else:
            f = fuzz.WRatio
            if "name" in self.settings["objects"]:
                s = self.indexer.difference_search("name", query, f, self.settings["fuzzy_k"])
                resultset.update(s)
            if "phone" in self.settings["objects"]:
                s = self.indexer.difference_search("phone", query, f, self.settings["fuzzy_k"])
                resultset.update(s)
            if "email" in self.settings["objects"]:
                s = self.indexer.difference_search("param", query, f, self.settings["fuzzy_k"], use_param="EMAIL")
                resultset.update(s)
        return resultset
