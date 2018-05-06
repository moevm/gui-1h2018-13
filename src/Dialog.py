import logging
import urllib.request as urllib
from functools import lru_cache

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem


@lru_cache(maxsize=64)
def loadImage(url):
    return urllib.urlopen(url).read()


class Dialog(QListWidgetItem):
    log = logging.getLogger('Dialog')

    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message
        try:
            self.log.info("Load image from: {}, for {}".format(message['photo_50'],
                                                               message['first_name'] + ' ' + message['last_name']))
            data = loadImage(message['photo_50'])
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            icon = QIcon(pixmap)
            self.setIcon(icon)
            self.setText(message['first_name'] + ' ' + message['last_name'] + ':\n' + message['body'])
        except Exception:
            self.log.info('Bots are not supported')
