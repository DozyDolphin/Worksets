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
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore

from .appdialog import AppDialog
from .designs import workset_design as design


class WorksetDialog(QtWidgets.QDialog, design.Ui_workset_dialog):
    def __init__(self, controller, workset=None, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(' Workset dialog')
        self.setupUi(self)
        self.controller = controller
        self.db_eid = -1
        self.apps = []

        if workset is None:
            self.edit = False
        else:
            self.edit = True
            self.name_before_edit = workset.name
            self.db_eid = workset.db_eid
            self.apps = workset.apps[:]
            self.name_input.setText(workset.name)
            self.init_line_edit.setText(workset.init_script)
            self._populate_app_list()

        self.init_filechooser.clicked.connect(self.select_file)
        self.add_app_btn.clicked.connect(self._app_dialog)
        self.app_list.itemDoubleClicked.connect(self._app_dialog)
        self.app_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.app_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.app_list.itemSelectionChanged.connect(self._change_del_btn_state)
        self.delete_btn.clicked.connect(self._remove_apps)
        self.test_btn.clicked.connect(self._test_workset)

    def _change_del_btn_state(self):
        if self.app_list.currentItem().isSelected() is True:
            self.delete_btn.setEnabled(True)
        if self.app_list.currentItem().isSelected() is False:
            self.delete_btn.setEnabled(False)

    def select_file(self):
        if self.init_line_edit.text() == "":
            script_dir = self.controller.get_script_dir()
        else:
            script_dir = self.init_line_edit.text()

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setDirectory(script_dir)
        file_tuple = file_dialog.getOpenFileName()
        if not file_tuple[0] == '':
            self.init_line_edit.setText(file_tuple[0])

    def _populate_app_list(self):
        self.app_list.clear()
        for app in self.apps:
            item = QtWidgets.QListWidgetItem(app.name)
            self.app_list.addItem(item)

    def _app_dialog(self, item):
        if isinstance(item, QtWidgets.QListWidgetItem):
            app = next((app for app in self.apps if app.name == item.text()), None)
            app_dialog = AppDialog(self.controller, app=app, parent=self)
        else:
            app_dialog = AppDialog(self.controller, parent=self)
        app_dialog.app_changed.connect(self.add_or_update_app)
        app_dialog.exec_()

    def old_add_or_update_app(self, app_dict):
        if app_dict['edit'] is True:
            for index, item in enumerate(self.apps):
                if item.name == app_dict['name_before_edit']:
                    self.apps[index] = app_dict['app']
        else:
            self.apps.append(app_dict['app'])
        self._populate_app_list()

    @pyqtSlot(dict)
    def add_or_update_app(self, app_dict):
        if app_dict['edit'] is True:
            for index, item in enumerate(self.apps):
                if item.name == app_dict['name_before_edit']:
                    self.apps[index] = app_dict['app']
        else:
            self.apps.append(app_dict['app'])
        self._populate_app_list()

    def _test_workset(self):
        self._save_app_order()
        workset_data = self._gather_workset_data()
        try:
            self.controller.test_workset(workset_data)
        except NameError as error:
            self._display_error(error)

    def _remove_apps(self):
        item_names = [item.text() for item in self.app_list.selectedItems()]
        confirm = self._confirm_delete(item_names)
        if confirm == QtWidgets.QMessageBox.Yes:
            for name in item_names:
                self.apps.remove(next((app
                                       for app
                                       in self.apps
                                       if app.name == name)))
        self._populate_app_list()

    def _confirm_delete(self, item_names):
        message = _("Delete the following apps?") + '\n\n' + ''.join(item_names)
        confirm = QtWidgets.QMessageBox.question(self,
                                                 _('Confirm deletion'),
                                                 message,
                                                 QtWidgets.QMessageBox.Yes |
                                                 QtWidgets.QMessageBox.No,
                                                 QtWidgets.QMessageBox.No)
        return confirm

    def _display_error(self, error):
        self.name_input.setObjectName('target')
        self.name_input.setStyleSheet("#target { border: 1px solid red; background-color: #ffe6e6;}")
        self.name_input.setToolTip(str(error))
        self.name_input.textChanged[str].connect(self._revert_error)

    def _revert_error(self):
        self.name_input.setStyleSheet('')
        self.name_input.setToolTip('')
        self.name_input.textChanged[str].disconnect(self._revert_error)

    def _save_app_order(self):
        items = []
        for index in range(self.app_list.count()):
            items.append(self.app_list.item(index))
        apps_from_list = [i.text() for i in items]
        self.apps = sorted(self.apps,
                           key=lambda app: apps_from_list.index(app.name))

    def _gather_workset_data(self):
        return {'name': self.name_input.text(),
                'init_script': self.init_line_edit.text(),
                'apps': self.apps,
                'db_eid': self.db_eid}

    def accept(self):
        # missing name before edit or is this done by eid alone?
        self._save_app_order()
        workset_data = self._gather_workset_data()
        try:
            self.controller.save_or_update_workset(workset_data)
            super(WorksetDialog, self).accept()
        except NameError as error:
            self._display_error(error)

    def retranslateUi(self, workset_dialog):
        _translate = QtCore.QCoreApplication.translate
        workset_dialog.setWindowTitle(_translate("workset_dialog", _("Workset")))
        self.name_label.setText(_translate("workset_dialog", _("Name:")))
        self.init_label.setText(_translate("workset_dialog", _("Init script:")))
        self.apps_label.setText(_translate("workset_dialog", _("Apps:")))
        self.delete_btn.setText(_translate("workset_dialog", _("Delete")))
        self.add_app_btn.setText(_translate("workset_dialog", _("Add app")))
        self.test_btn.setText(_translate("workset_dialog", _("Test")))
        self.init_filechooser.setText(_translate("workset_dialog", "..."))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(_translate("&Cancel", _('&Cancel')))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(_translate("&Ok", _('&Ok')))
