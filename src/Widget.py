import logging

from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from .ChatWidget import ChatWidget
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

    updateTitle = Signal()
    updateDialogs = Signal(int, int, bool)
    updateMessages = Signal(int, int)

    @Slot(name='onInitialized')
    def onInitialized(self):
        self.updateTitle.emit()
        self.updateMessages.emit(0, 10)
        self.updateDialogs.emit(0, 10, True)

    @Slot(str, name='onChangeTitle')
    def onChangeTitle(self, title):
        self.log.info(f'New title: {str}')
        self.setWindowTitle(title)

    @Slot(dict, name='onChangeDialogs')
    def onChangeDialogs(self, dialogs):
        self.log.info(f'New dialogs: {dialogs}')

    @Slot(dict, name='onChangeMessages')
    def onChangeMessages(self, messages):
        self.log.info(f'New messages: {messages}')

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
