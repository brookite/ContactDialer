from PyQt5 import QtWidgets, QtGui
from ui.finddialog import Ui_Form as FindDialogUI

class FindDialog(QtWidgets.QWidget):
    VIEW_CMP = {
        "equal": "Equal",
        "contain": "Contain",
        "fuzzy": "Fuzzy",
        "end": "At end",
        "start": "At start",
        "all": "All",
        "default": "Default"
    }

    APP_CMP = {
        "Equal": "equal",
        "Contain": "contain",
        "Fuzzy": "fuzzy",
        "At end": "end",
        "At start": "start",
        "All": "all",
        "Default": "default"
    }

    def __init__(self, mainview, searcher):
        super().__init__()
        self._searcher = searcher
        self._mainview = mainview
        self._ui = FindDialogUI()
        self._ui.setupUi(self)
        self.restore()
        self.setWindowTitle("Search")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self._ui.find.clicked.connect(self.find)
        self._ui.applySettings.clicked.connect(self.apply_settings)
        self._ui.clearSearch.clicked.connect(self.clear)

    def app_representation(self, text):
        return self.APP_CMP[text]

    def view_representation(self, text):
        return self.VIEW_CMP[text]

    def restore(self):
        self._ui.searchtype.setCurrentText(
            self.view_representation(self._searcher.settings["type"]))
        self._ui.casechk.setChecked(self._searcher.settings["case"])
        self._ui.phonemethod.setCurrentText(self.view_representation(
            self._searcher.settings["phone_constraints"]))
        self._ui.fuzzy_k.setValue(self._searcher.settings["fuzzy_k"])
        targets = self._searcher.settings["objects"]
        if "phone" in targets:
            self._ui.phone.setChecked(True)
        if "name" in targets:
            self._ui.name.setChecked(True)
        if "email" in targets:
            self._ui.email.setChecked(True)

    def clear(self):
        self._mainview.find("")

    def apply_settings(self):
        targets = []
        if self._ui.phone.isChecked():
            targets.append("phone")
        if self._ui.name.isChecked():
            targets.append("name")
        if self._ui.email.isChecked():
            targets.append("email")
        self._searcher.set_parameters(objects=targets,
                                      type=self.app_representation(
                                          self._ui.searchtype.currentText()),
                                      case=self._ui.casechk.isChecked(),
                                      phone_constraints=self.app_representation(
                                          self._ui.phonemethod.currentText()),
                                      fuzzy_k=self._ui.fuzzy_k.value()
                                      )

    def find(self):
        self.apply_settings()
        self._mainview.find(self._ui.mainSearch.text())