import logging

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidgetItem

from .ChatWidget import ChatWidget
from .Dialog import Dialog
from .DialogsWidget import DialogsWidget
from .LogInView import LogInView
from .VKApi import VKApi


class Widget(QWidget):
    """
    This class is the main class of the application.
    """
    log = logging.getLogger(name='Widget')
    __webView = None
    __api = None
    __chatWidget = None
    __dialogsWidget = None
    _loadPerOnce = 20
    _loadDialogsOffset = 0
    _loadMessagesOffset = 0

    updateTitle = Signal()
    updateDialogs = Signal(int, int, bool)
    updateMessages = Signal(int, int, int)

    @Slot(name='onInitialized')
    def onInitialized(self):
        self.updateTitle.emit()

    @Slot(name='onUpdateDialogsClicked')
    def onUpdateDialogsClicked(self):
        self.log.info('\tUPDATE')
        self.updateDialogs.emit(self._loadDialogsOffset, self._loadPerOnce, False)

    @Slot(str, name='onChangeTitle')
    def onChangeTitle(self, title):
        self.log.info('New title: {}'.format(str))
        self.setWindowTitle(title)

    @Slot(dict, name='onChangeDialogs')
    def onChangeDialogs(self, dialogs):
        self.log.info('New dialogs: {}'.format(dialogs))
        self.__dialogsWidget.dialogs.clear()
        for dialog in dialogs['items']:
            item = Dialog(dialog['message'], self.__dialogsWidget.dialogs)
            self.__dialogsWidget.dialogs.addItem(item)

    @Slot(dict, name='onChangeMessages')
    def onChangeMessages(self, messages):
        self.log.info('New messages: {}'.format(messages))
        self.__chatWidget.messages.clear()
        for message in messages['items']:
            item = QListWidgetItem(self.__chatWidget.messages)
            item.setText(message['body'])
            item.setTextAlignment(2 if message['out'] == 1 else 1)
            self.__chatWidget.messages.addItem(item)

    @Slot(QListWidgetItem, name='onItemPressed')
    def onItemPressed(self, dialog: Dialog):
        self.__dialogsWidget.userId = dialog.message['user_id']
        if not dialog.message['user_id'] == self.__chatWidget.userId:
            self.__chatWidget.userId = dialog.message['user_id']
            self.updateMessages.emit(self._loadMessagesOffset, self._loadPerOnce, dialog.message['user_id'])

    @Slot(name='onMessageSent')
    def onMessageSent(self):
        self.updateMessages.emit(self._loadMessagesOffset, self._loadPerOnce, self.__chatWidget.userId)

    @Slot(name='onSendPressed')
    def onSendPressed(self):
        message = self.__chatWidget.messageEdit.toPlainText()
        self.__api.onSendMessage(message, self.__chatWidget.userId)
        self.__chatWidget.messageEdit.setText('')

    @Slot(name='closeLogInView')
    def closeLogInView(self):
        """
        This slot closes the login view, when token is being taken.
        """
        self.__webView.close()
        self.__webView.tokenTaken.disconnect(self.closeLogInView)
        self.__webView = None
        self.log.info('LogInView is to delete.')
        self.__chatWidget = ChatWidget(self)
        self.__dialogsWidget = DialogsWidget(self)
        self.__chatWidget.sendButton.clicked.connect(self.onSendPressed)
        self.__dialogsWidget.dialogs.itemClicked.connect(self.onItemPressed)
        self.__dialogsWidget.updateButton.clicked.connect(self.onUpdateDialogsClicked)
        self.__api.messageSent.connect(self.onMessageSent)
        self.layout().addWidget(self.__dialogsWidget)
        self.layout().addWidget(self.__chatWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__api = VKApi(self)
        self.log.info('Creating main Widget...')
        self.setWindowTitle('Messenger')
        self.setLayout(QHBoxLayout())
        self.__webView = LogInView(self)

        self.__api.initialized.connect(self.onInitialized)
        self.__api.changeMessages.connect(self.onChangeMessages)
        self.__api.changeDialogs.connect(self.onChangeDialogs)
        self.__api.changeTitle.connect(self.onChangeTitle)
        self.updateDialogs.connect(self.__api.onUpdateDialogs)
        self.updateMessages.connect(self.__api.onUpdateMessages)
        self.updateTitle.connect(self.__api.onUpdateTitle)
        self.__webView.tokenTaken.connect(self.__api.takeToken)
        self.__webView.tokenTaken.connect(self.closeLogInView)

        self.layout().addWidget(self.__webView)
