from tabnanny import filename_only
from typing import Dict, Optional, Tuple, List
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os

from ui.mainview import Ui_MainWindow as MainViewUI

from core import AppCore, get_vcard_name
from core.search import SearchEngine

from views.contact import ContactView
from views.find import FindDialog
from views.merge import MergeDialog

import pyvcard

VERSION = [1, 0, 0, 38]
VERSION_NAME = "1.0.0.38"
MAINTAINER = "brookite"
APP_NAME = "ContactDialer"
APPDIR = os.path.abspath(os.path.dirname(__file__))

class MainView(QtWidgets.QMainWindow):
    _proxy_tree: Dict
    _core: AppCore
    _searcher: SearchEngine
    fd: Optional[FindDialog]

    def __init__(self):
        super().__init__()
        self._proxy_tree = None

        self.qtapp = QtWidgets.QApplication.instance()
        self.qtapp.setApplicationName(APP_NAME)
        app.setApplicationVersion(VERSION_NAME)

        self._core = AppCore()
        self._searcher = SearchEngine(self._core)

        self._ui = MainViewUI()
        self._ui.setupUi(self)

        self._ui.open_file.triggered.connect(self.open_filedialog)
        self._ui.openVcards.clicked.connect(self.open_contact)
        self._ui.actionFind.triggered.connect(self.open_search)
        self._ui.actionOpen_all_cards.triggered.connect(self.openAll)
        self._ui.actionAbout_Qt.triggered.connect(self.qtapp.aboutQt)
        self._ui.actionExit.triggered.connect(self.close)
        self._ui.aboutapp.triggered.connect(self.about)
        self._ui.actionMerge.triggered.connect(self.merge_action)

        self._contentLayout = QtWidgets.QVBoxLayout(self._ui.content)
        self._view = ContactView()

        self.fd = None
        self._model = QtGui.QStandardItemModel()
        self._ui.openVcards.setModel(self._model)
        self._ui.openVcards.doubleClicked.connect(self.open)

        self._ui.openVcards.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        menu = QtWidgets.QMenu()
        exportAction = menu.addAction(self.tr("Export to CSV"))
        exportAction.triggered.connect(self.export_action)

        removeAction = menu.addAction(self.tr("Remove from list"))
        removeAction.triggered.connect(self.remove_file)

        self._ui.openVcards.customContextMenuRequested.connect(lambda pos, menu=menu: self.on_context_menu(menu))

        self._ui.searchSettings.clicked.connect(self.open_search)
        self._ui.searchField.editingFinished.connect(self.search_field_signal)

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self._contentLayout.addWidget(self._view)

        self.openInitialVcards()

    def openInitialVcards(self) -> None:
        for path in self._core.settings["opened"]:
            self._core.load_vcardinfo(path)
        self.refresh_tree()

    def search_field_signal(self) -> None:
        self.find(self._ui.searchField.text())

    def open_search(self) -> None:
        if not self.fd:
            self.fd = FindDialog(self, self._searcher)
        self.fd.show()

    def find(self, query: str) -> None:
        if query.strip():
            results = self._searcher.query(query)
            tree = self._searcher.proxy_tree(results)
            self._proxy_tree = tree
            self.refresh_tree()
            self._ui.openVcards.expandAll()
        else:
            self._proxy_tree = None
            self.refresh_tree()

    def open_file(self, file):
        if file:
            if not file.loaded():
                self._core.fetch_vcard(file)
                self.refresh_tree()

    def openAll(self) -> None:
        for i in range(self._model.rowCount()):
            file = self._core.get(i)
            self.open_file(file)

    def export_action(self):
        index = self._ui.openVcards.currentIndex().row()
        file = self._core.get(index)
        self.open_file(file)
        vset = pyvcard.vCardSet(file.vcards)
        csv = pyvcard.convert(vset).csv().permanent_result()
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, self.tr("Export"), "",
            "CSV (*.csv)"
        )[0]
        if filename:
            f = open(filename, "w", encoding="utf-8")
            f.write(csv)
            f.close()
    
    def merge_action(self):
        self.merge = MergeDialog(self, self._core)
        self.merge.show()

    def about(self):
        QtWidgets.QMessageBox.about(self, self.tr("About ContactDialer"),
		'<p><b>' + f'ContactDialer {VERSION_NAME}' +'</b></p>'
		+self.tr('Viewer for vCard files (using pyvcard)') +'<br>'
        +self.tr('Author: ') + "Brookit, 2022"
		+'<br><a href="https://github.com/brookite">GitHub</a>')
    
    def open(self, i, expand: bool=True):
        if i.parent().row() == -1:
            file = self._core.get(self.fileindex(i))
            if file:
                self.open_file(file)
                item = self._model.item(i.row())
                if expand:
                    if not self._ui.openVcards.isExpanded(item.index()):
                        self._ui.openVcards.setExpanded(item.index(), True)
                    else:
                        self._ui.openVcards.setExpanded(item.index(), False)

    def fileindex(self, i: QtCore.QModelIndex) -> int:
        index = i.row()
        if self._proxy_tree is not None:
            index = list(self._proxy_tree.keys())[index]
        return index

    def contactindex(self, i: QtCore.QModelIndex) -> Tuple[int, int]:
        filenum, cntnum = i.parent().row(), i.row()
        if filenum == -1:
            return None, None
        if self._proxy_tree is not None:
            filenum =  list(self._proxy_tree.keys())[filenum]
            cntnum = self._proxy_tree[filenum][cntnum]
        return filenum, cntnum

    def open_filedialog(self):
        # Returns ui representation of contact bundle
        filenames = QtWidgets.QFileDialog.getOpenFileNames(
            self, self.tr("Open vCard files"), "",
            "vCard (*.vcf)"
        )
        self.add_vcards(filenames[0])

    def add_vcards(self, filepaths: List[str]):
        for path in filepaths:
            self._core.fetch_vcard(path)
        self.refresh_tree()

    def refresh_tree(self) -> None:
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

    def open_contact(self, contact: QtCore.QModelIndex) -> None:
        filenum, cntnum = self.contactindex(contact)
        if filenum is not None:
            self._view.setting_contact(self._core.route(filenum, cntnum))
    
    def on_context_menu(self, menu):
        main_index = self._ui.openVcards.currentIndex().parent().row()
        if main_index == -1:
            menu.exec_(QtGui.QCursor.pos())
    
    def remove_file(self):
        index = self._ui.openVcards.currentIndex().row()
        file = self._core.get(index)
        self._core.remove_file(file)
        self.refresh_tree()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    language = QtCore.QLocale().name()
    AppTranslator = QtCore.QTranslator()
    AppTranslator.load('cntdialer_' + language,
                    os.path.join(APPDIR, 'locale'))
    QtTranslator = QtCore.QTranslator()
    translationsPath = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    QtTranslator.load("qtbase_" + language, translationsPath)
    app.installTranslator(AppTranslator)
    app.installTranslator(QtTranslator)

    window = MainView()
    window.show()
    sys.exit(app.exec_())
