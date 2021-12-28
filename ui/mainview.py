# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainview.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftBox = QtWidgets.QVBoxLayout()
        self.leftBox.setObjectName("leftBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.searchField = QtWidgets.QLineEdit(self.centralwidget)
        self.searchField.setObjectName("searchField")
        self.horizontalLayout_2.addWidget(self.searchField)
        self.searchSettings = QtWidgets.QToolButton(self.centralwidget)
        self.searchSettings.setObjectName("searchSettings")
        self.horizontalLayout_2.addWidget(self.searchSettings)
        self.leftBox.addLayout(self.horizontalLayout_2)
        self.openVcards = QtWidgets.QTreeView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openVcards.sizePolicy().hasHeightForWidth())
        self.openVcards.setSizePolicy(sizePolicy)
        self.openVcards.setObjectName("openVcards")
        self.leftBox.addWidget(self.openVcards)
        self.horizontalLayout.addLayout(self.leftBox)
        self.content = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.content.sizePolicy().hasHeightForWidth())
        self.content.setSizePolicy(sizePolicy)
        self.content.setObjectName("content")
        self.horizontalLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.file = QtWidgets.QMenu(self.menubar)
        self.file.setObjectName("file")
        self.about = QtWidgets.QMenu(self.menubar)
        self.about.setObjectName("about")
        MainWindow.setMenuBar(self.menubar)
        self.open_file = QtWidgets.QAction(MainWindow)
        self.open_file.setObjectName("open_file")
        self.aboutapp = QtWidgets.QAction(MainWindow)
        self.aboutapp.setObjectName("aboutapp")
        self.file.addAction(self.open_file)
        self.about.addAction(self.aboutapp)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.about.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.searchSettings.setText(_translate("MainWindow", "..."))
        self.file.setTitle(_translate("MainWindow", "File"))
        self.about.setTitle(_translate("MainWindow", "?"))
        self.open_file.setText(_translate("MainWindow", "Open File"))
        self.aboutapp.setText(_translate("MainWindow", "About"))