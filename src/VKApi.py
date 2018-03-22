import vk
import logging
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QObject


class VKApi(QObject):
    """
    VK interaction class.
    """
    log = logging.getLogger(name='VKApi')

    @Slot(str, name='takeToken')
    def takeToken(self, token):
        self.__token = token
        self.log.info(f'Token in API: {self.__token}')
        self.__session = vk.Session(access_token=token)
        self.log.info(f'Session: {self.__session}')
        self.__api = vk.API(self.__session)
        self.log.info(f'API: {self.__api}')

    def __init__(self, parent=None):
        super().__init__(parent)
