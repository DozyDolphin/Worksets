'''
Copyright 2017 Anders Lykke Gade

This file is part of Worksets.

Worksets is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Worksets is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Worksets.  If not, see <http://www.gnu.org/licenses/>.
'''

import logging
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from .designs import settings_design as design


class SettingsDialog(QtWidgets.QDialog, design.Ui_settings_dialog):

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(' Settings dialog')
        self.setupUi(self)
        self.controller = controller
        self.populate_fields()

        self.pushButton.clicked.connect(self._rescan)
        self.script_dir_picker.clicked.connect(self._choose_dir)
        self.log_dir_picker.clicked.connect(self._choose_dir)
        self.log_checkBox.clicked.connect(self._change_log_state)

    def populate_fields(self):
        languages = self.controller.get_languages()
        for desc, key in languages.items():
            self.language_combobox.addItem(desc)
        index = self.language_combobox.findText(self.controller.get_language())
        self.language_combobox.setCurrentIndex(index)
        self.script_dir_input.setText(self.controller.get_script_dir())
        log_levels = self.controller.get_log_levels()
        for each in log_levels:
            self.loglevel_combobox.addItem(each)
        index = self.loglevel_combobox.findText(self.controller.get_log_level())
        self.loglevel_combobox.setCurrentIndex(index)
        self.log_dir_input.setText(self.controller.get_log_dir())
        self.log_checkBox.setChecked(self.controller.get_log_enabled())
        self.log_to_console_checkBox.setChecked(self.controller.get_log_to_console())
        self._change_log_state()
        self.version_label.setText(self.controller.get_version())

    def _rescan(self):
        self.controller.update_screen_config()


    def _change_log_state(self):
        state = self.log_checkBox.isChecked()
        self.loglevel_combobox.setEnabled(state)
        self.log_dir_picker.setEnabled(state)
        self.log_dir_input.setEnabled(state)
        self.log_to_console_checkBox.setEnabled(state)

    def _choose_dir(self):
        sender = self.sender()
        if sender.objectName() == 'script_dir_picker':
            receiver = self.script_dir_input
        elif sender.objectName() == 'log_dir_picker':
            receiver = self.log_dir_input
        directory = receiver.text()

        dialog = QtWidgets.QFileDialog()
        folder_path = dialog.getExistingDirectory(self, _("Select Folder"), directory)
        if not folder_path == '':
            receiver.setText(folder_path)

    def get_settings_data(self):
        return {'language': str(self.language_combobox.currentText()),
                'script_dir': self.script_dir_input.text().strip(),
                'log_enabled': self.log_checkBox.isChecked(),
                'log_to_console': self.log_to_console_checkBox.isChecked(),
                'log_level': self.loglevel_combobox.currentText(),
                'log_dir': self.log_dir_input.text().strip()}

    def accept(self):
        self.logger.info("Saving settings")
        settings_data = self.get_settings_data()
        self.controller.save_settings(settings_data)
        super().accept()

    def retranslateUi(self, settings_dialog):
        _translate = QtCore.QCoreApplication.translate
        settings_dialog.setWindowTitle(_translate("settings_dialog", _("Settings")))
        self.language_label.setText(_translate("settings_dialog", _("Language:")))
        self.script_dir_label.setText(_translate("settings_dialog", _("Script directory:")))
        self.script_dir_picker.setText(_translate("settings_dialog", "..."))
        self.log_checkBox.setText(_translate("settings_dialog", _("Logging enabled")))
        self.pushButton.setText(_translate("settings_dialog", _("Scan for system changes")))
        self.log_dir_label.setText(_translate("settings_dialog", _("Log directory:")))
        self.loglevel_label.setText(_translate("settings_dialog", _("Log level:")))
        self.log_dir_picker.setText(_translate("settings_dialog", "..."))
        self.log_to_console_checkBox.setText(_translate("settings_dialog", _("Log to console")))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), _translate("settings_dialog", _("General")))
        self.title_label.setText(_translate("settings_dialog", "Worksets"))
        self.version_label.setText(_translate("settings_dialog", "Version"))
        self.desc_label.setText(_translate("settings_dialog", "<html><head/><body><p align=\"center\">" + _("Quickly launch and arrange multiple applications <br/>in your desktop environment to support a specific workflow.") + "</p></body></html>"))
        self.label.setText(_translate("settings_dialog", "<html><head/><body><p align=\"center\">Copyright © 2017 Anders Lykke Gade</p></body></html>"))
        self.label_2.setText(_translate("settings_dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:8pt;\">" + _("This program is distributed") + " </span><span style=\" font-size:8pt; font-style:italic;\">" + _("without any warranty whatsoever") + "</span><span style=\" font-size:8pt;\"><br/>" + _("under the") + " </span><a href=\"https://www.gnu.org/licenses/gpl-3.0.html\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">" + _("GNU General Public Licence, version 3 or later") + "</span></a><span style=\" font-size:8pt;\">.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.about_tab), _translate("settings_dialog", _("About")))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(_translate("&Cancel", _('&Cancel')))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(_translate("&Ok", _('&Ok')))
