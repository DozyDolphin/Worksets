# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NEW_workset_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_workset_dialog(object):
    def setupUi(self, workset_dialog):
        workset_dialog.setObjectName("workset_dialog")
        workset_dialog.resize(500, 430)
        workset_dialog.setMinimumSize(QtCore.QSize(500, 430))
        workset_dialog.setMaximumSize(QtCore.QSize(500, 430))
        self.buttonBox = QtWidgets.QDialogButtonBox(workset_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 382, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.name_label = QtWidgets.QLabel(workset_dialog)
        self.name_label.setGeometry(QtCore.QRect(20, 30, 67, 17))
        self.name_label.setObjectName("name_label")
        self.init_label = QtWidgets.QLabel(workset_dialog)
        self.init_label.setGeometry(QtCore.QRect(20, 70, 71, 17))
        self.init_label.setObjectName("init_label")
        self.apps_label = QtWidgets.QLabel(workset_dialog)
        self.apps_label.setGeometry(QtCore.QRect(20, 110, 171, 17))
        self.apps_label.setObjectName("apps_label")
        self.app_list = QtWidgets.QListWidget(workset_dialog)
        self.app_list.setGeometry(QtCore.QRect(20, 130, 461, 191))
        self.app_list.setObjectName("app_list")
        self.delete_btn = QtWidgets.QPushButton(workset_dialog)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setGeometry(QtCore.QRect(20, 330, 97, 26))
        self.delete_btn.setObjectName("delete_btn")
        self.add_app_btn = QtWidgets.QPushButton(workset_dialog)
        self.add_app_btn.setGeometry(QtCore.QRect(304, 330, 177, 26))
        self.add_app_btn.setObjectName("add_app_btn")
        self.name_input = QtWidgets.QLineEdit(workset_dialog)
        self.name_input.setGeometry(QtCore.QRect(110, 30, 371, 27))
        self.name_input.setObjectName("name_input")
        self.test_btn = QtWidgets.QPushButton(workset_dialog)
        self.test_btn.setGeometry(QtCore.QRect(20, 385, 97, 26))
        self.test_btn.setObjectName("test_btn")
        self.init_line_edit = QtWidgets.QLineEdit(workset_dialog)
        self.init_line_edit.setGeometry(QtCore.QRect(110, 67, 338, 27))
        self.init_line_edit.setObjectName("init_line_edit")
        self.init_filechooser = QtWidgets.QPushButton(workset_dialog)
        self.init_filechooser.setGeometry(QtCore.QRect(450, 67, 31, 26))
        self.init_filechooser.setObjectName("init_filechooser")

        self.retranslateUi(workset_dialog)
        self.buttonBox.accepted.connect(workset_dialog.accept)
        self.buttonBox.rejected.connect(workset_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(workset_dialog)
