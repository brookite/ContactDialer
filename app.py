from cmath import e
from PyQt5 import QtWidgets, QtGui
import sys

from isort import file
from ui.mainview import Ui_MainWindow as MainViewUI

from core import AppCore, get_vcard_name
from core.search import SearchEngine

from views.contact import ContactView
from views.find import FindDialog

class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._proxy_tree = None

        self._core = AppCore()
        self._searcher = SearchEngine(self._core)

        self._ui = MainViewUI()
        self._ui.setupUi(self)

        self._ui.open_file.triggered.connect(self.open_filedialog)
        self._ui.openVcards.clicked.connect(self.open_contact)
        self._ui.actionFind.triggered.connect(self.open_search)
        self._ui.actionOpen_all_cards.triggered.connect(self.openAll)

        self._contentLayout = QtWidgets.QVBoxLayout(self._ui.content)
        self._view = ContactView()

        self.fd = None
        self._model = QtGui.QStandardItemModel()
        self._ui.openVcards.setModel(self._model)
        self._ui.openVcards.doubleClicked.connect(self.open)

        self._ui.searchSettings.clicked.connect(self.open_search)
        self._ui.searchField.editingFinished.connect(self.search_field_signal)

        self.setWindowTitle("ContactDialer")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self._contentLayout.addWidget(self._view)

        self.openInitialVcards()

    def openInitialVcards(self):
        for path in self._core.settings["opened"]:
            self._core.load_vcardinfo(path)
        self.refresh_tree()

    def search_field_signal(self):
        self.find(self._ui.searchField.text())

    def open_search(self):
        if not self.fd:
            self.fd = FindDialog(self, self._searcher)
        self.fd.show()

    def find(self, query):
        if query.strip():
            results = self._searcher.query(query)
            tree = self._searcher.proxy_tree(results)
            self._proxy_tree = tree
            self.refresh_tree()
            self._ui.openVcards.expandAll()
        else:
            self._proxy_tree = None
            self.refresh_tree()

    def openAll(self):
        for i in range(self._model.rowCount()):
            file = self._core.get(i)
            if file:
                if not file.loaded():
                    self._core.fetch_vcard(file)
                    self.refresh_tree()
    
    def open(self, i, expand=True):
        file = self._core.get(self.fileindex(i))
        if file:
            if not file.loaded():
                self._core.fetch_vcard(file)
                self.refresh_tree()
            item = self._model.item(i.row())
            if expand:
                if not self._ui.openVcards.isExpanded(item.index()):
                    self._ui.openVcards.setExpanded(item.index(), True)
                else:
                    self._ui.openVcards.setExpanded(item.index(), False)

    def fileindex(self, i):
        index = i.row()
        if self._proxy_tree is not None:
            index = list(self._proxy_tree.keys())[index]
        return index

    def contactindex(self, i):
        filenum, cntnum = i.parent().row(), i.row()
        if self._proxy_tree is not None:
            filenum =  list(self._proxy_tree.keys())[filenum]
            cntnum = self._proxy_tree[filenum][cntnum]
        return filenum, cntnum

    def open_filedialog(self):
        # Returns ui representation of contact bundle
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        dialog.filesSelected.connect(self.add_vcards)
        dialog.show()

    def add_vcards(self, filepaths):
        for path in filepaths:
            self._core.fetch_vcard(path)
        self.refresh_tree()

    def refresh_tree(self):
        tree = self._core.vcard_tree()
        if self._proxy_tree is not None:
            tree = {}
            for i, indexes in self._proxy_tree.items():
                filename = str(self._core._vcards[i])
                tree.setdefault(filename, [])
                for j in indexes:
                    file = self._core.route(i, j)
                    tree[filename].append(file)
        else:
            tree = self._core.vcard_tree()

        self._model.clear()
        for file in tree:
            fileitem = QtGui.QStandardItem()
            fileitem.setEditable(False)
            fileitem.setText(str(file))
            self._model.appendRow(fileitem)
            for cnt in tree[file]:
                item = QtGui.QStandardItem()
                item.setEditable(False)
                item.setText(get_vcard_name(cnt))
                fileitem.appendRow(item)

    def open_contact(self, contact):
        filenum, cntnum = self.contactindex(contact)
        if filenum != -1:
            self._view.setting_contact(self._core.route(filenum, cntnum))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec_())
