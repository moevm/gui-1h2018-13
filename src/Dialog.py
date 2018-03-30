import logging
import urllib.request as urllib

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem


class Dialog(QListWidgetItem):
    log = logging.getLogger('Dialog')

    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message
        self.log.info("Load image from: {}, for {}".format(message['photo_50'],
                                                           message['first_name'] + ' ' + message['last_name']))
        data = urllib.urlopen(message['photo_50']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setText(message['first_name'] + ' ' + message['last_name'] + ':\n' + message['body'])
