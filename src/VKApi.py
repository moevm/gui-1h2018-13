import logging

import vk
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from time import sleep

from .utils import makeRequest


class VKApi(QObject):
    """
    VK interaction class.
    """
    __token = None
    __session = None
    __api = None

    initialized = Signal()
    changeTitle = Signal(str)
    changeDialogs = Signal(dict)
    changeMessages = Signal(dict)

    log = logging.getLogger(name='VKApi')

    @Slot(int, int, int, name='onUpdateMessages')
    def onUpdateMessages(self, offset, count, user_id):
        @makeRequest
        def req():
            messages = self.__api.messages.getHistory(user_id=user_id, offset=offset, count=count, v=5.73)
            self.log.info(f'messages: {messages}')
            self.changeMessages.emit(messages)

        req()

    @Slot(int, int, bool, name='onUpdateDialogs')
    def onUpdateDialogs(self, offset, count, unread):
        @makeRequest
        def req():
            dialogs = self.__api.messages.getDialogs(preview_length=30, offset=offset, count=count, v=5.73)
            self.log.info(f'dialogs: {dialogs}')
            self.log.info('Load names...')
            for item in dialogs['items']:
                user = self.__api.users.get(v=5.73, user_ids=item['message']['user_id'], fields='photo_50')[0]
                item['message']['photo_50'] = user['photo_50']
                item['message']['first_name'] = user['first_name']
                item['message']['last_name'] = user['last_name']
                self.log.info(f'Now user: {item}')
                sleep(0.3)

            self.changeDialogs.emit(dialogs)

        req()

    @Slot(name='onUpdateTitle')
    def onUpdateTitle(self):
        @makeRequest
        def req():
            answer = self.__api.account.getProfileInfo(v=5.73)
            title = answer['first_name'] + ' ' + answer['last_name']
            self.log.info(f'title: {title}')
            self.changeTitle.emit(title)

        req()

    @Slot(str, name='takeToken')
    def takeToken(self, token):
        self.__token = token
        self.log.info(f'Token in API: {self.__token}')
        self.__session = vk.Session(access_token=token)
        self.log.info(f'Session: {self.__session}')
        self.__api = vk.API(self.__session)
        self.log.info(f'API: {self.__api}')
        self.initialized.emit()

    def __init__(self, parent=None):
        super().__init__(parent)
