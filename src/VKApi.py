import vk
import logging
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QObject


class VKApi(QObject):
    """
    VK interaction class.
    """
    logger = logging.getLogger(name='VKApi')

    @Slot(str, name='takeToken')
    def takeToken(self, token):
        self.token = token
        self.logger.info(f'Token in API: {self.token}')
        self.session = vk.Session(access_token=token)
        self.logger.info(f'Session: {self.session}')
        self.api = vk.API(self.session)
        self.logger.info(f'API: {self.api}')

    def __init__(self, parent=None):
        super().__init__(parent)
