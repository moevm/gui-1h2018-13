import logging
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import QObject
import urllib.request as urllib
from .utils import makeRequest
from time import sleep

class Dialog(QListWidgetItem):
    log = logging.getLogger('Dialog')

    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message
        self.log.info(f"Load image from: {message['photo_50']}, for {message['first_name'] + ' ' + message['last_name']}")
        data = urllib.urlopen(message['photo_50']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setText(message['first_name'] + ' ' + message['last_name'] + ':\n' + message['body'])
