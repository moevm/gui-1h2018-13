import vk
import logging
from threading import Thread
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QObject


class VKApi(QObject):
    """
    VK interaction class.
    """
    changeTitle = Signal(str)

    log = logging.getLogger(name='VKApi')

    @Slot(str, name='takeToken')
    def takeToken(self, token):
        self.__token = token
        self.log.info(f'Token in API: {self.__token}')
        self.__session = vk.Session(access_token=token)
        self.log.info(f'Session: {self.__session}')
        self.__api = vk.API(self.__session)
        self.log.info(f'API: {self.__api}')
        def function():
            answer = self.__api.account.getProfileInfo(v=5.73)
            title = answer['first_name'] + ' ' + answer['last_name']
            self.log.info(f'answer: {answer}')
            self.log.info(f'title: {title}')
            self.changeTitle.emit(title)
        Thread(target=function).start()

    def __init__(self, token, parent=None):
        super().__init__(parent)
