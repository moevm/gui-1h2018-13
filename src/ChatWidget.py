import logging
from PyQt5.QtWidgets import (QWidget, QListWidget, QTextEdit, QVBoxLayout, QPushButton)


class ChatWidget(QWidget):
    log = logging.getLogger(name='CHatWidget')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__messages = QListWidget(self)
        self.__messageEdit = QTextEdit(self)
        self.__sendButton = QPushButton(self)
        self.__sendButton.setText('Send')
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__messages)
        self.layout().addWidget(self.__messageEdit)
        self.layout().addWidget(self.__sendButton)
