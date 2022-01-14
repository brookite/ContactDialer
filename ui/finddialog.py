# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'finddialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(455, 225)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainSearch = QtWidgets.QLineEdit(Form)
        self.mainSearch.setObjectName("mainSearch")
        self.horizontalLayout.addWidget(self.mainSearch)
        self.find = QtWidgets.QPushButton(Form)
        self.find.setObjectName("find")
        self.horizontalLayout.addWidget(self.find)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.casechk = QtWidgets.QCheckBox(Form)
        self.casechk.setObjectName("casechk")
        self.verticalLayout.addWidget(self.casechk)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.phone = QtWidgets.QCheckBox(Form)
        self.phone.setObjectName("phone")
        self.horizontalLayout_2.addWidget(self.phone)
        self.name = QtWidgets.QCheckBox(Form)
        self.name.setObjectName("name")
        self.horizontalLayout_2.addWidget(self.name)
        self.email = QtWidgets.QCheckBox(Form)
        self.email.setObjectName("email")
        self.horizontalLayout_2.addWidget(self.email)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.searchtype = QtWidgets.QComboBox(Form)
        self.searchtype.setObjectName("searchtype")
        self.searchtype.addItem("")
        self.searchtype.addItem("")
        self.searchtype.addItem("")
        self.horizontalLayout_3.addWidget(self.searchtype)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.phonemethod = QtWidgets.QComboBox(Form)
        self.phonemethod.setObjectName("phonemethod")
        self.phonemethod.addItem("")
        self.phonemethod.addItem("")
        self.phonemethod.addItem("")
        self.phonemethod.addItem("")
        self.horizontalLayout_4.addWidget(self.phonemethod)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.fuzzy_k = QtWidgets.QSpinBox(Form)
        self.fuzzy_k.setMaximum(100)
        self.fuzzy_k.setProperty("value", 80)
        self.fuzzy_k.setObjectName("fuzzy_k")
        self.horizontalLayout_5.addWidget(self.fuzzy_k)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.applySettings = QtWidgets.QPushButton(Form)
        self.applySettings.setObjectName("applySettings")
        self.horizontalLayout_6.addWidget(self.applySettings)
        self.clearSearch = QtWidgets.QPushButton(Form)
        self.clearSearch.setObjectName("clearSearch")
        self.horizontalLayout_6.addWidget(self.clearSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.find.setText(_translate("Form", "Find"))
        self.casechk.setText(_translate("Form", "Case sensitive "))
        self.label.setText(_translate("Form", "Search by:"))
        self.phone.setText(_translate("Form", "Phone number"))
        self.name.setText(_translate("Form", "Name"))
        self.email.setText(_translate("Form", "Email"))
        self.label_2.setText(_translate("Form", "Search type"))
        self.searchtype.setItemText(0, _translate("Form", "Equal"))
        self.searchtype.setItemText(1, _translate("Form", "Contain"))
        self.searchtype.setItemText(2, _translate("Form", "Fuzzy"))
        self.label_3.setText(_translate("Form", "Phone search method:"))
        self.phonemethod.setItemText(0, _translate("Form", "Default"))
        self.phonemethod.setItemText(1, _translate("Form", "At start"))
        self.phonemethod.setItemText(2, _translate("Form", "At end"))
        self.phonemethod.setItemText(3, _translate("Form", "All"))
        self.label_4.setText(_translate("Form", "Fuzzy search coefficient"))
        self.applySettings.setText(_translate("Form", "Apply settings"))
        self.clearSearch.setText(_translate("Form", "Clear results"))