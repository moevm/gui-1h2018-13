import logging
from PyQt5.QtWidgets import (QWidget, QListWidget, QVBoxLayout, QPushButton)


class DialogsWidget(QWidget):
    log = logging.getLogger(name='DialogsWidget')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__dialogs = QListWidget(self)
        self.__findDialogButton = QPushButton(self)
        self.__findDialogButton.setText('Start Dialog')
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__dialogs)
        self.layout().addWidget(self.__findDialogButton)
