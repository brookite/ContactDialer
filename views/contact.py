from PyQt5 import QtWidgets, QtGui, QtCore
from ui.contactview import Ui_Form as ContactViewUI


class ContactView(QtWidgets.QWidget):
    def __init__(self, contact=None):
        super().__init__()
        self._ui = ContactViewUI()
        self._ui.setupUi(self)
        self._contact = contact
        self.pixmap = None
        if self._contact:
            self.setting_contact()
        self.clipboard = QtGui.QGuiApplication.clipboard()
        self._ui.name.mouseDoubleClickEvent = lambda e: self.copy_text(
            self._ui.name)
        self._ui.tel.mouseDoubleClickEvent = lambda e: self.copy_text(
            self._ui.tel)
        self._ui.address.mouseDoubleClickEvent = lambda e: self.copy_text(
            self._ui.address)
        self._ui.email.mouseDoubleClickEvent = lambda e: self.copy_text(
            self._ui.email)
        self._ui.nickname.mouseDoubleClickEvent = lambda e: self.copy_text(
            self._ui.nickname)
        self._ui.org.mouseDoubleClickEvent = lambda e: self.copy_text(
            self._ui.org)
        self._ui.url.mouseDoubleClickEvent = lambda e: self.copy_text(
            self._ui.url)

    def copy_text(self, source):
        self.clipboard.setText(source.text())

    def setting_contact(self, contact=None):
        if contact:
            self._contact = contact
        self._ui.name.setText(str(self._contact.name.value))
        self._ui.tel.setText(";".join(map(str, self._contact.tel.values)))
        self._ui.email.setText(
            "Email:" + ";".join(map(str, self._contact.email.values)))
        self._ui.address.setText(
            "Address:" + ";".join(map(str, self._contact.address.values)))
        self._ui.nickname.setText(
            "Nickname:" + ";".join(map(str, self._contact.nickname.values)))
        self._ui.url.setText(
            "URL:" + ";".join(map(str, self._contact.url.values)))
        self._ui.bday.setText(
            "Birthday:" + ";".join(map(str, self._contact.birthday.values)))
        self._ui.org.setText(
            "Organization:" + ";".join(map(str, self._contact.org.values)))
        self._ui.notefield.setPlainText(
            ";".join(map(str, self._contact.note.values)))

        photo = None
        if self._contact.photo.values:
            photo = self._contact.photo.value.bytes
        elif self._contact.logo.values:
            photo = self._contact.logo.value.bytes

        if photo is not None:
            self.pixmap = QtGui.QPixmap()
            self.pixmap.loadFromData(photo)
            self._ui.image.setPixmap(self.pixmap.scaled(340, 340))
        else:
            self._ui.image.clear()