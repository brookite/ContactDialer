from PyQt5 import QtWidgets, QtGui
import sys
from ui.mainview import Ui_MainWindow as MainViewUI
from ui.contactview import Ui_Form as ContactViewUI
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


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__main_tree_loaded = True
        self._core = AppCore()
        self._ui = MainViewUI()
        self._ui.setupUi(self)
        self._ui.open_file.triggered.connect(self.open_filedialog)
        self._ui.openVcards.clicked.connect(self.open_contact)
        self._contentLayout = QtWidgets.QVBoxLayout(self._ui.content)
        self._view = None
        self._searcher = SearchEngine(self._core._vcards, self._core._indexer)
        self._model = QtGui.QStandardItemModel()
        self._ui.openVcards.setModel(self._model)
        self._ui.openVcards.doubleClicked.connect(self.checkUnopened)
        self.openInitialVcards()
        self._ui.searchField.editingFinished.connect(self.search_field_signal)
        self.setWindowTitle("ContactDialer")

    def openInitialVcards(self):
        for path in self._core.settings["opened"]:
            self._core.load_vcardinfo(path)
        self.refresh_tree(self._core.vcard_tree())

    def search_field_signal(self):
        self.find(self._ui.searchField.text())

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

    def checkUnopened(self, i):
        path = self._model.item(i.row())
        if path:
            path = path.text()
            if self._core.is_unloaded(path):
                self._core.fetch_vcard(self._core._vcards[path][1])
                self.refresh_tree(self._core.vcard_tree(path))

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