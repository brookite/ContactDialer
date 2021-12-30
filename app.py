from PyQt5 import QtWidgets, QtGui
import sys
from ui.mainview import Ui_MainWindow as MainViewUI
from ui.contactview import Ui_Form as ContactViewUI
from ui.finddialog import Ui_Form as FindDialogUI
from core import AppCore
from core.search import SearchEngine


class ContactView(QtWidgets.QWidget):
    def __init__(self, contact):
        super().__init__()
        self._ui = ContactViewUI()
        self._ui.setupUi(self)
        self._contact = contact
        self.setting_contact()
    
    def setting_contact(self):
        self._ui.name.setText("Name:" + str(self._contact.name.value))
        self._ui.tel.setText("Tel. Number:" + ";".join(map(str, self._contact.tel.values)))
        self._ui.email.setText("Email:" + ";".join(map(str, self._contact.email.values)))


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
        self._ui.find.clicked.connect(self.find)
        self._ui.applySettings.clicked.connect(self.apply_settings)
        self._ui.clearSearch.clicked.connect(self.clear)

    def app_representation(self, text):
        return self.APP_CMP[text]

    def view_representation(self, text):
        return self.VIEW_CMP[text]

    def restore(self):
        self._ui.searchtype.setCurrentText(self.view_representation(self._searcher.settings["type"]))
        self._ui.casechk.setChecked(self._searcher.settings["case"])
        self._ui.phonemethod.setCurrentText(self.view_representation(self._searcher.settings["phone_constraints"]))
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
            type=self.app_representation(self._ui.searchtype.currentText()),
            case=self._ui.casechk.isChecked(),
            phone_constraints=self.app_representation(self._ui.phonemethod.currentText()),
            fuzzy_k=self._ui.fuzzy_k.value()
        )
    
    def find(self):
        self.apply_settings()
        self._mainview.find(self._ui.mainSearch.text())

class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__main_tree_loaded = True
        self._core = AppCore()
        self._ui = MainViewUI()
        self._ui.setupUi(self)
        self._ui.open_file.triggered.connect(self.open_filedialog)
        self._ui.openVcards.clicked.connect(self.open_contact)
        self._ui.actionFind.triggered.connect(self.open_search)
        self._ui.actionOpen_all_cards.triggered.connect(self.openAll)
        self._contentLayout = QtWidgets.QVBoxLayout(self._ui.content)
        self._view = None
        self.fd = None
        self._searcher = SearchEngine(self._core._vcards, self._core._indexer)
        self._model = QtGui.QStandardItemModel()
        self._ui.openVcards.setModel(self._model)
        self._ui.openVcards.doubleClicked.connect(self.checkUnopened)
        self._ui.searchSettings.clicked.connect(self.open_search)
        self.openInitialVcards()
        self._ui.searchField.editingFinished.connect(self.search_field_signal)
        self.setWindowTitle("ContactDialer")

    def openInitialVcards(self):
        for path in self._core.settings["opened"]:
            self._core.load_vcardinfo(path)
        self.refresh_tree(self._core.vcard_tree())

    def search_field_signal(self):
        self.find(self._ui.searchField.text())

    def open_search(self):
        if not self.fd:
            self.fd = FindDialog(self, self._searcher)
        self.fd.show()

    def find(self, query):
        if query.strip():
            self._core.revert_tree()
            results = self._searcher.query(query)
            tree = self._searcher.classified_tree(results, self._core._tree)
            self._core.set_temp_tree(tree)
            self.refresh_tree(tree)
            self.__main_tree_loaded = False
            self._ui.openVcards.expandAll()
        else:
            self.__main_tree_loaded = True
            self._core.revert_tree()
            self.refresh_tree(self._core._tree)

    def openAll(self):
        for i in range(self._model.rowCount()):
            path = self._model.item(i)
            if self._core.is_unloaded(path.text()):
                self._core.fetch_vcard(self._core._vcards[path.text()][1])
                self.refresh_tree(self._core.vcard_tree(path.text()))

    def checkUnopened(self, i):
        path = self._model.item(i.row())
        if path:
            if self._core.is_unloaded(path.text()):
                self._core.fetch_vcard(self._core._vcards[path.text()][1])
                self.refresh_tree(self._core.vcard_tree(path.text()))
            path = self._model.item(i.row())
            if not self._ui.openVcards.isExpanded(path.index()):
                self._ui.openVcards.setExpanded(path.index(), True)
            else:
                self._ui.openVcards.setExpanded(path.index(), False)

    def open_filedialog(self):
        # Returns ui representation of contact bundle
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        dialog.filesSelected.connect(self.add_vcards)
        dialog.show()

    def add_vcards(self, filepaths):
        for path in filepaths:
            self._core.fetch_vcard(path)
        self.refresh_tree(self._core.vcard_tree())
    
    def refresh_tree(self, tree):
        self._model.clear()
        for file in tree:
            fileitem = QtGui.QStandardItem()
            fileitem.setEditable(False)
            fileitem.setText(str(file))
            self._model.appendRow(fileitem)
            for cnt in tree[file]:
                item = QtGui.QStandardItem()
                item.setEditable(False)
                if not cnt:
                    cnt = "Unnamed"
                item.setText(repr(cnt))
                fileitem.appendRow(item)

    def open_contact(self, contact):
        filenum, cntnum = contact.parent().row(), contact.row()
        if filenum != -1:
            if self._view:
                self._contentLayout.removeWidget(self._view)
            self._view = ContactView(self._core.route(filenum, cntnum))
            self._contentLayout.addWidget(self._view)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec_())