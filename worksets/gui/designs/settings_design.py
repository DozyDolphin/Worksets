# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NEW_settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        settings_dialog.setObjectName("settings_dialog")
        settings_dialog.resize(500, 360)
        settings_dialog.setMinimumSize(QtCore.QSize(500, 350))
        settings_dialog.setMaximumSize(QtCore.QSize(500, 360))
        self.buttonBox = QtWidgets.QDialogButtonBox(settings_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 313, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(settings_dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 501, 301))
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setObjectName("tabWidget")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setAutoFillBackground(True)
        self.settings_tab.setObjectName("settings_tab")
        self.language_label = QtWidgets.QLabel(self.settings_tab)
        self.language_label.setEnabled(True)
        self.language_label.setGeometry(QtCore.QRect(20, 70, 121, 31))
        self.language_label.setMinimumSize(QtCore.QSize(83, 0))
        self.language_label.setObjectName("language_label")
        self.language_combobox = QtWidgets.QComboBox(self.settings_tab)
        self.language_combobox.setEnabled(True)
        self.language_combobox.setGeometry(QtCore.QRect(330, 70, 150, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language_combobox.sizePolicy().hasHeightForWidth())
        self.language_combobox.setSizePolicy(sizePolicy)
        self.language_combobox.setMinimumSize(QtCore.QSize(150, 31))
        self.language_combobox.setMaximumSize(QtCore.QSize(150, 31))
        self.language_combobox.setObjectName("language_combobox")
        self.script_dir_label = QtWidgets.QLabel(self.settings_tab)
        self.script_dir_label.setGeometry(QtCore.QRect(20, 110, 181, 27))
        self.script_dir_label.setMinimumSize(QtCore.QSize(83, 0))
        self.script_dir_label.setMaximumSize(QtCore.QSize(16777215, 28))
        self.script_dir_label.setObjectName("script_dir_label")
        self.script_dir_input = QtWidgets.QLineEdit(self.settings_tab)
        self.script_dir_input.setGeometry(QtCore.QRect(150, 110, 299, 27))
        self.script_dir_input.setObjectName("script_dir_input")
        self.script_dir_picker = QtWidgets.QPushButton(self.settings_tab)
        self.script_dir_picker.setGeometry(QtCore.QRect(450, 110, 31, 27))
        self.script_dir_picker.setObjectName("script_dir_picker")
        self.log_checkBox = QtWidgets.QCheckBox(self.settings_tab)
        self.log_checkBox.setGeometry(QtCore.QRect(20, 150, 151, 22))
        self.log_checkBox.setObjectName("log_checkBox")
        self.pushButton = QtWidgets.QPushButton(self.settings_tab)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 461, 31))
        self.pushButton.setObjectName("pushButton")
        self.log_dir_label = QtWidgets.QLabel(self.settings_tab)
        self.log_dir_label.setGeometry(QtCore.QRect(20, 220, 181, 27))
        self.log_dir_label.setMinimumSize(QtCore.QSize(83, 0))
        self.log_dir_label.setMaximumSize(QtCore.QSize(16777215, 28))
        self.log_dir_label.setObjectName("log_dir_label")
        self.loglevel_combobox = QtWidgets.QComboBox(self.settings_tab)
        self.loglevel_combobox.setEnabled(True)
        self.loglevel_combobox.setGeometry(QtCore.QRect(330, 180, 150, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loglevel_combobox.sizePolicy().hasHeightForWidth())
        self.loglevel_combobox.setSizePolicy(sizePolicy)
        self.loglevel_combobox.setMinimumSize(QtCore.QSize(150, 31))
        self.loglevel_combobox.setMaximumSize(QtCore.QSize(150, 31))
        self.loglevel_combobox.setObjectName("loglevel_combobox")
        self.log_dir_input = QtWidgets.QLineEdit(self.settings_tab)
        self.log_dir_input.setGeometry(QtCore.QRect(150, 220, 299, 27))
        self.log_dir_input.setObjectName("log_dir_input")
        self.loglevel_label = QtWidgets.QLabel(self.settings_tab)
        self.loglevel_label.setEnabled(True)
        self.loglevel_label.setGeometry(QtCore.QRect(20, 180, 121, 31))
        self.loglevel_label.setMinimumSize(QtCore.QSize(83, 0))
        self.loglevel_label.setObjectName("loglevel_label")
        self.log_dir_picker = QtWidgets.QPushButton(self.settings_tab)
        self.log_dir_picker.setGeometry(QtCore.QRect(450, 220, 31, 27))
        self.log_dir_picker.setObjectName("log_dir_picker")
        self.log_to_console_checkBox = QtWidgets.QCheckBox(self.settings_tab)
        self.log_to_console_checkBox.setGeometry(QtCore.QRect(330, 150, 151, 22))
        self.log_to_console_checkBox.setObjectName("log_to_console_checkBox")
        self.tabWidget.addTab(self.settings_tab, "")
        self.about_tab = QtWidgets.QWidget()
        self.about_tab.setAutoFillBackground(True)
        self.about_tab.setObjectName("about_tab")
        self.title_label = QtWidgets.QLabel(self.about_tab)
        self.title_label.setGeometry(QtCore.QRect(190, 100, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.version_label = QtWidgets.QLabel(self.about_tab)
        self.version_label.setGeometry(QtCore.QRect(210, 130, 81, 20))
        self.version_label.setAlignment(QtCore.Qt.AlignCenter)
        self.version_label.setObjectName("version_label")
        self.desc_label = QtWidgets.QLabel(self.about_tab)
        self.desc_label.setGeometry(QtCore.QRect(70, 150, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.desc_label.setFont(font)
        self.desc_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.desc_label.setLineWidth(1)
        self.desc_label.setObjectName("desc_label")
        self.label = QtWidgets.QLabel(self.about_tab)
        self.label.setGeometry(QtCore.QRect(70, 230, 361, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.about_tab)
        self.label_2.setGeometry(QtCore.QRect(80, 190, 341, 51))
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.about_tab, "")

        self.retranslateUi(settings_dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(settings_dialog.accept)
        self.buttonBox.rejected.connect(settings_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(settings_dialog)
