from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import QObject
import urllib.request as urllib

class Dialog(QListWidgetItem):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message
        data = urllib.urlopen(message['photo_50']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setText('-' + message['first_name'] + ' ' + message['last_name'] + '\n' + message['body'])
