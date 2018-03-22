import logging
from PyQt5.QtWidgets import QWidget


class ChatWidget(QWidget):
    log = logging.getLogger(name='CHatWidget')

    def __init__(self, parent=None):
        super().__init__(parent)
