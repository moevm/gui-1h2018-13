import logging
from PyQt5.QtWidgets import (QWidget, QListWidget, QVBoxLayout, QPushButton)


class DialogsWidget(QWidget):
    log = logging.getLogger(name='DialogsWidget')
    dialogs = None
    findDialogButton = None
    updateButton = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialogs = QListWidget(self)
        self.findDialogButton = QPushButton(self)
        self.updateButton = QPushButton(self)
        self.updateButton.setText('Update dialogs.')
        self.findDialogButton.setText('Start Dialog')
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.dialogs)
        self.layout().addWidget(self.findDialogButton)
        self.layout().addWidget(self.updateButton)
