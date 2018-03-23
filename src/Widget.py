import logging
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout
from .LogInView import LogInView
from .VKApi import VKApi
from .ChatWidget import ChatWidget
from .DialogsWidget import DialogsWidget


class Widget(QWidget):
    """
    This class is the main class of the application.
    """
    log = logging.getLogger(name='Widget')
    __webView = None
    __api = None
    __chatWidget = None
    __dialogsWidget = None

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
        self.__api = VKApi(parent=self)

    def __init__(self, parent=None):
        super().__init__(parent)
        __api = VKApi(self)
        self.log.info('Creating main Widget...')
        self.setWindowTitle('Messenger')
        self.setLayout(QHBoxLayout())
        self.__webView = LogInView(self)
        self.__webView.tokenTaken.connect(__api.takeToken)
        self.__webView.tokenTaken.connect(self.closeLogInView)
        self.layout().addWidget(self.__webView)
