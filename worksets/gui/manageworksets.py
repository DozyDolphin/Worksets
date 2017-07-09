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

from .worksetdialog import WorksetDialog
from .designs import mw_design as design


class ManageWorksets(QtWidgets.QDialog, design.Ui_manage_worksets):

    def __init__(self, controller, publisher, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(' ManageWorksets')
        self.setupUi(self)
        self.controller = controller
        self.publisher = publisher
        self.publisher.register(['UPDATED', 'INSERTED', 'REMOVED'],
                                self,
                                self._update_workset_list)
        self.initiate_workset_list()

        self.new_workset_btn.clicked.connect(self.workset_dialog)
        self.delete_btn.clicked.connect(self._remove_worksets)

    def initiate_workset_list(self):
        self.workset_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.workset_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.workset_list.itemSelectionChanged.connect(self._change_del_btn_state)
        self._populate_workset_list()

    def _populate_workset_list(self):
        self.workset_list.clear()
        self.worksets = self.controller.get_worksets()
        for workset in self.worksets:
            item = QtWidgets.QListWidgetItem(workset.name)
            self.workset_list.addItem(item)
        self.workset_list.itemDoubleClicked.connect(self.workset_dialog)

    def _update_workset_list(self, message):
        self.logger.debug("Updating workset list: " + message)
        self._populate_workset_list()

    def _remove_worksets(self):
        item_names = [item.text()
                      for item
                      in self.workset_list.selectedItems()]
        confirm = self.confirm_delete(item_names)
        if confirm == QtWidgets.QMessageBox.Yes:
            for name in item_names:
                self.controller.remove_workset_by_name(name)

    def confirm_delete(self, item_names):
        message = _("Delete the following worksets?") + '\n\n'.join(item_names)
        confirm = QtWidgets.QMessageBox.question(self,
                                                 _('Confirm deletion'),
                                                 message,
                                                 QtWidgets.QMessageBox.Yes |
                                                 QtWidgets.QMessageBox.No,
                                                 QtWidgets.QMessageBox.No)
        return confirm

    def workset_dialog(self, item):
        if isinstance(item, QtWidgets.QListWidgetItem):
            workset = next((workset
                            for workset
                            in self.worksets
                            if workset.name == item.text()),
                           None)
            workset_dialog = WorksetDialog(self.controller, workset)
        else:
            workset_dialog = WorksetDialog(self.controller)
        workset_dialog.exec_()

    def _change_del_btn_state(self):
        if self.workset_list.currentItem().isSelected() is True:
            self.delete_btn.setEnabled(True)
        if self.workset_list.currentItem().isSelected() is False:
            self.delete_btn.setEnabled(False)

    def unregister_from_publisher(self):
        self.publisher.unregister(['UPDATED',
                                   'INSERTED',
                                   'REMOVED'],
                                  self)

    def accept(self):
        items = []
        for index in range(self.workset_list.count()):
            items.append(self.workset_list.item(index))
        workset_names = [i.text() for i in items]
        self.controller.rearrange_worksets(workset_names)
        self.unregister_from_publisher()
        super(ManageWorksets, self).accept()

    def reject(self):
        self.unregister_from_publisher()
        super(ManageWorksets, self).reject()

    def retranslateUi(self, manage_worksets):
        _translate = QtCore.QCoreApplication.translate
        manage_worksets.setWindowTitle(_translate("manage_worksets", _("Manage worksets")))
        self.new_workset_btn.setText(_translate("manage_worksets", _("New workset")))
        self.delete_btn.setText(_translate("manage_worksets", _("Delete")))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(_translate("&Cancel", _('&Cancel')))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(_translate("&Ok", _('&Ok')))