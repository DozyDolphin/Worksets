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
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from .designs import app_design as design


class AppDialog(QtWidgets.QDialog, design.Ui_app_dialog):

    app_changed = pyqtSignal(dict)

    def __init__(self, controller, app=None, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger('AppDialog')
        self.parent = parent
        self.setupUi(self)
        self.controller = controller
        self.app = app
        self._populate_fields()
        if self.app is not None:
            self.edit = True  # Should no longer be necessary
            self._populate_app_data()
        else:
            self.edit = False

        self.test_btn.clicked.connect(self.test_app)
        self.window_checkBox.clicked.connect(self._change_window_state)

    def _populate_fields(self):
        self.placements = self.controller.get_placements()
        for desc, key in self.placements.items():
            self.location_combobox.addItem(desc)
        for desktop in self.controller.screen.desktops:
            self.desktop_combobox.addItem(str(desktop.no))
        for no, _ in self.controller.screen.monitors.items():
            self.monitor_combobox.addItem(str(no))

    def _populate_app_data(self):
        self.name_input.setText(self.app.name)
        #  makes it possible to find the workset in database if name has been edited
        self.name_before_edit = self.app.name
        self.exe_input.setText(self.app.executable)
        self.parameters_input.setText(' '.join(self.app.parameters))
        for desc, key in self.placements.items():
            if key == self.app.placement_type:
                index = self.location_combobox.findText(desc)
                self.location_combobox.setCurrentIndex(index)
        index = self.desktop_combobox.findText(str(self.app.placement_desktop))
        self.desktop_combobox.setCurrentIndex(index)
        index = self.monitor_combobox.findText(str(self.app.placement_monitor))
        self.monitor_combobox.setCurrentIndex(index)
        self.window_checkBox.setChecked(self.app.creates_window)
        self.splash_checkBox.setChecked(self.app.has_splash)
        self.uses_existing_checkBox.setChecked(self.app.uses_existing_window)

    def _change_window_state(self):
        state = self.window_checkBox.isChecked()
        self.location_combobox.setEnabled(state)
        self.desktop_combobox.setEnabled(state)
        self.monitor_combobox.setEnabled(state)
        self.splash_checkBox.setEnabled(state)
        self.uses_existing_checkBox.setEnabled(state)

    def _get_app_data(self):
        return {'name': self.name_input.text().strip(),
                'executable': self.exe_input.text().strip(),
                'parameters': self.parameters_input.text().strip(),
                'creates_window': self.window_checkBox.isChecked(),
                'has_splash': self.splash_checkBox.isChecked(),
                'uses_existing_window': self.uses_existing_checkBox.isChecked(),
                'placement': str(self.location_combobox.currentText()),
                'desktop': str(self.desktop_combobox.currentText()),
                'monitor': str(self.monitor_combobox.currentText()), }

    def test_app(self):
        app_data = self._get_app_data()
        if self.app is not None:
            app_data['org_name'] = self.app.name
        try:
            self.controller.test_app_data(app_data, self.parent.apps)
        except NameError as name_error:
            self._display_error(name_error, self.name_input, 'name_target')
        except OSError as exe_error:
            self._display_error(exe_error, self.exe_input, 'exe_target')
        else:
            app = self.controller.create_app(app_data)
            self.controller.test_app(app)

    def _display_error(self, error, target_variable, target_name):
        target_variable.setObjectName(target_name)
        target_variable.setStyleSheet("#" + target_name + " { border: 1px solid red; background-color: #ffe6e6;}")
        target_variable.setToolTip(str(error))
        target_variable.textChanged[str].connect(self._revert_error)

    def _revert_error(self):
        target_variable = self.sender()
        target_variable.setStyleSheet('')
        target_variable.setToolTip('')
        target_variable.textChanged[str].disconnect(self._revert_error)

    def accept(self):
        # Throw error if nothing has been put in
        app_data = self._get_app_data()
        if self.app is not None:
            app_data['org_name'] = self.app.name
        try:
            self.controller.test_app_data(app_data, self.parent.apps)
        except NameError as name_error:
            self._display_error(name_error, self.name_input, 'name_target')
        except OSError as exe_error:
            self._display_error(exe_error, self.exe_input, 'exe_target')
        else:
            app = self.controller.create_app(app_data)
            app_dict = {'app': app, 'edit': self.edit}
            if self.edit is True:
                app_dict['name_before_edit'] = self.name_before_edit
            self.app_changed.emit(app_dict)
            super(AppDialog, self).accept()

    def retranslateUi(self, app_dialog):
        _translate = QtCore.QCoreApplication.translate
        app_dialog.setWindowTitle(_translate("app_dialog", _("App")))
        self.name_label.setText(_translate("app_dialog", _("Name:")))
        self.exe_label.setText(_translate("app_dialog", _("Executable:")))
        self.parameters_label.setText(_translate("app_dialog", _("Parameters:")))
        self.location_label.setText(_translate("app_dialog", _("Location on desktop:")))
        self.desktop_label.setText(_translate("app_dialog", _("Desktop:")))
        self.monitor_label.setText(_translate("app_dialog", _("Monitor:")))
        self.placement_label.setText(_translate("app_dialog", _("Placement")))
        self.test_btn.setText(_translate("app_dialog", _("Test")))
        self.window_checkBox.setText(_translate("app_dialog", _("Creates a new window")))
        self.splash_checkBox.setText(_translate("app_dialog", _("Has splash screen")))
        self.uses_existing_checkBox.setText(_translate("app_dialog", _("Uses existing window if one is present")))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(_translate("&Cancel", _('&Cancel')))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(_translate("&Ok", _('&Ok')))