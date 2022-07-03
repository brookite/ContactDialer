from PyQt5 import QtWidgets, QtGui, QtCore
from ui.mergedialog import Ui_MergeFiles as MergeDialogUI
import pyvcard

from core import AppCore

class MergeDialog(QtWidgets.QWidget):
    def __init__(self, mainview: "app.MainView", core: AppCore):
        super().__init__()
        self._core = core
        self._mainview = mainview
        self._ui = MergeDialogUI()
        self._ui.setupUi(self)
        self.selected = []
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        files = map(str, self._core._vcards)
        self._ui.listWidget.addItems(files)

        for i in range(self._ui.listWidget.count()):
            item = self._ui.listWidget.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

        self._ui.listWidget.itemChanged.connect(self.selection)
        self._ui.cancelButton.clicked.connect(self.close)
        self._ui.mergeButton.clicked.connect(self.merge)
    
    def merge(self):
        vset = pyvcard.vCardSet()
        for i in self.selected:
            self._mainview.open_file(self._core.get(i))
            vset.update(self._core._vcards[i].vcards)
        vcard = vset.repr_vcard()
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, self.tr("Merge"), "",
            "vCard (*.vcf)"
        )[0]
        if filename:
            f = open(filename, "w", encoding="utf-8")
            f.write(vcard)
            f.close()
        self.close()

    def selection(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.selected.append(self._ui.listWidget.row(item))
        else:
            self.selected.remove(self._ui.listWidget.row(item))


