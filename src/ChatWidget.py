import logging
from PyQt5.QtWidgets import (QWidget, QListWidget, QTextEdit, QVBoxLayout, QPushButton)


class ChatWidget(QWidget):
    log = logging.getLogger(name='CHatWidget')
    messsages = None
    userId = None
    sendButton = None
    messageEdit = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = QListWidget(self)
        self.messageEdit = QTextEdit(self)
        self.sendButton = QPushButton(self)
        self.sendButton.setText('Send')
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.messages)
        self.layout().addWidget(self.messageEdit)
        self.layout().addWidget(self.sendButton)
