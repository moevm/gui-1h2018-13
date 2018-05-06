import logging
import random

import vk
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot

from .utils import makeRequest

API_VERSION = 5.73

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
    textFound = Signal(list)

    log = logging.getLogger(name='VKApi')

    @Slot(int, int, int, name='onUpdateMessages')
    def onUpdateMessages(self, offset, count, user_id):
        @makeRequest
        def req():
            messages = self.__api.messages.getHistory(user_id=user_id, offset=offset, count=count, v=API_VERSION)
            self.log.info('messages: {}'.format(messages))
            self.changeMessages.emit(messages)

        req()

    @Slot(str, int, name='onSendMessage')
    def onSendMessage(self, message, to):
        @makeRequest
        def req():
            self.__api.messages.send(message=message, user_id=to, peer_id=to, v=API_VERSION,
                                     random_id=random.randint(0, 100000))
            self.messageSent.emit()

        req()

    @Slot(int, int, bool, name='onUpdateDialogs')
    def onUpdateDialogs(self, offset, count, unread):
        @makeRequest
        def req():
            dialogs = self.__api.messages.getDialogs(preview_length=30, offset=offset, count=count, v=API_VERSION)
            dialogs['items'] = [item for item in dialogs['items'] if 'chat_id' not in item['message']]
            self.log.info('dialogs: {}'.format(dialogs))
            self.log.info('Load names...')
            ids = [str(item['message']['user_id']) for item in dialogs['items']]
            self.log.info('IDS: {}'.format(ids))
            usersInfo = self.__api.users.get(user_ids=','.join(ids), fields='photo_50', v=API_VERSION)

            for dialogItem in dialogs['items']:
                for item in usersInfo:
                    if item['id'] == dialogItem['message']['user_id']:
                        dialogItem['message']['photo_50'] = item['photo_50']
                        dialogItem['message']['first_name'] = item['first_name']
                        dialogItem['message']['last_name'] = item['last_name']
                        break
                    self.log.info('Dialog item now: {}'.format(dialogItem))
            self.changeDialogs.emit(dialogs)

        req()

    @Slot(name='onUpdateTitle')
    def onUpdateTitle(self):
        @makeRequest
        def req():
            answer = self.__api.account.getProfileInfo(v=API_VERSION)
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

    @Slot(int, str, name='onSearchText')
    def onSearchText(self, toLoad: int, text: str):
        @makeRequest
        def req():
            nonlocal toLoad
            if toLoad > 100:
                toLoad = 100
            items = self.__api.messages.search(q=text, count=toLoad, v=API_VERSION)['items']
            items = [item for item in items if 'chat_id' not in item]
            self.log.info('Found: {}'.format(items))
            ids = [str(item['user_id']) for item in items]
            info = self.__api.users.get(user_ids=','.join(ids), v=API_VERSION)
            for item in items:
                for info_item in info:
                    if info_item['id'] == item['user_id']:
                        item['first_name'] = info_item['first_name']
                        item['last_name'] = info_item['last_name']
                        break
            self.log.info('Messages with names: {}'.format(items))
            self.textFound.emit(items)

        req()


    def __init__(self, parent=None):
        super().__init__(parent)
