import logging
import random
from time import sleep

import vk
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot

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
    messageSent = Signal()

    log = logging.getLogger(name='VKApi')

    @Slot(int, int, int, name='onUpdateMessages')
    def onUpdateMessages(self, offset, count, user_id):
        @makeRequest
        def req():
            messages = self.__api.messages.getHistory(user_id=user_id, offset=offset, count=count, v=5.73)
            self.log.info('messages: {}'.format(messages))
            self.changeMessages.emit(messages)

        req()

    @Slot(str, int, name='onSendMessage')
    def onSendMessage(self, message, to):
        @makeRequest
        def req():
            sleep(0.1)
            self.__api.messages.send(message=message, user_id=to, peer_id=to, v=5.73, random_id=random.randint(0, 100000))
            self.messageSent.emit()

        req()
    @Slot(int, int, bool, name='onUpdateDialogs')
    def onUpdateDialogs(self, offset, count, unread):
        @makeRequest
        def req():
            dialogs = self.__api.messages.getDialogs(preview_length=30, offset=offset, count=count, v=5.73)
            dialogs['items'] = [item for item in dialogs['items'] if 'chat_id' not in item['message']]
            self.log.info('dialogs: {}'.format(dialogs))
            self.log.info('Load names...')
            ids = [str(item['message']['user_id']) for item in dialogs['items']]
            self.log.info('IDS: {}'.format(ids))
            usersInfo = self.__api.users.get(user_ids=','.join(ids), fields='photo_50', v=5.73)
            
            for dialogItem , item in zip(dialogs['items'], usersInfo):
                dialogItem['message']['photo_50'] = item['photo_50']
                dialogItem['message']['first_name'] = item['first_name']
                dialogItem['message']['last_name'] = item['last_name']
                self.log.info('Dialog item now: {}'.format(dialogItem))

            self.changeDialogs.emit(dialogs)

        req()

    @Slot(name='onUpdateTitle')
    def onUpdateTitle(self):
        @makeRequest
        def req():
            answer = self.__api.account.getProfileInfo(v=5.73)
            title = answer['first_name'] + ' ' + answer['last_name']
            self.log.info('title: {}'.format(title))
            self.changeTitle.emit(title)

        req()

    @Slot(str, name='takeToken')
    def takeToken(self, token):
        self.__token = token
        self.log.info('Token in API: {}'.format(self.__token))
        self.__session = vk.Session(access_token=token)
        self.log.info('Session: {}'.format(self.__session))
        self.__api = vk.API(self.__session)
        self.log.info('API: {}'.format(self.__api))
        self.initialized.emit()

    def __init__(self, parent=None):
        super().__init__(parent)
