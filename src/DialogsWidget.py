import logging
from PyQt5.QtWidgets import QWidget


class DialogsWidget(QWidget):
    log = logging.getLogger(name='DialogsWidget')

    def __init__(self, parent=None):
        super().__init__(parent)
