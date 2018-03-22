import logging
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from .LogInView import LogInView
from .VKApi import VKApi 


class Widget(QWidget):
    """
    This class is the main class of the application.
    """
    logger = logging.getLogger(name='Widget')
    webView = None
    api = None

    @Slot(name='closeLogInView')
    def closeLogInView(self):
        """
        This slot closes the login view, when token is being taken.
        """
        self.webView.close()
        self.webView.tokenTaken.disconnect(self.closeLogInView)
        self.webView = None
        self.logger.info('LogInView is to delete.')

    def __init__(self, parent=None):
        super().__init__(parent)
        api = VKApi(self)
        self.logger.info('Creating main Widget...')
        self.setWindowTitle('Messenger')
        self.setLayout(QHBoxLayout())
        self.webView = LogInView(self)
        self.webView.tokenTaken.connect(api.takeToken)
        self.webView.tokenTaken.connect(self.closeLogInView)
        self.layout().addWidget(self.webView)
