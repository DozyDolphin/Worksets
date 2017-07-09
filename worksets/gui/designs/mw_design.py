# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NEW_manage_worksets.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_manage_worksets(object):
    def setupUi(self, manage_worksets):
        manage_worksets.setObjectName("manage_worksets")
        manage_worksets.resize(500, 350)
        manage_worksets.setMinimumSize(QtCore.QSize(500, 300))
        manage_worksets.setMaximumSize(QtCore.QSize(500, 350))
        self.buttonBox = QtWidgets.QDialogButtonBox(manage_worksets)
        self.buttonBox.setGeometry(QtCore.QRect(140, 300, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.workset_list = QtWidgets.QListWidget(manage_worksets)
        self.workset_list.setGeometry(QtCore.QRect(21, 20, 459, 221))
        self.workset_list.setMinimumSize(QtCore.QSize(459, 0))
        self.workset_list.setMaximumSize(QtCore.QSize(341, 350))
        self.workset_list.setObjectName("workset_list")
        self.new_workset_btn = QtWidgets.QPushButton(manage_worksets)
        self.new_workset_btn.setGeometry(QtCore.QRect(380, 250, 101, 26))
        self.new_workset_btn.setObjectName("new_workset_btn")
        self.delete_btn = QtWidgets.QPushButton(manage_worksets)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setGeometry(QtCore.QRect(20, 250, 101, 26))
        self.delete_btn.setObjectName("delete_btn")

        self.retranslateUi(manage_worksets)
        self.buttonBox.accepted.connect(manage_worksets.accept)
        self.buttonBox.rejected.connect(manage_worksets.reject)
        QtCore.QMetaObject.connectSlotsByName(manage_worksets)
