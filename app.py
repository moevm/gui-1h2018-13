import vk
import sys
import logging
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QUrl, QUrlQuery, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class LogInView(QWebEngineView):
    """
    This is class where user can login
    """
    logger = logging.getLogger(name='LogInView')
    appId = 6390333
    appPermission = ['friends', 'photos', 'pages', 'status', 'messages', 'notifications']

    tokenTaken = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadAuthPage()
        self.urlChanged.connect(self.onUrlChanged)

    @Slot(QUrl, name='onUrlChanged')
    def onUrlChanged(self, newUrl: QUrl):
        """
        URL changed handler.
        """
        url = QUrl(newUrl.toString().replace('#', '?'))

        self.logger.info(f'url was changed to {url.toString()}')
        if url.hasQuery():
            query = QUrlQuery(url.query())
            if query.hasQueryItem('access_token'):
                token = query.queryItemValue('access_token')
                self.tokenTaken.emit(token)
                self.deleteLater()

    def loadAuthPage(self):
        """
        This method loads auth page, so user can login in VK.
        """
        url = QUrl('https://oauth.vk.com/authorize')
        query = QUrlQuery()

        query.addQueryItem('client_id', str(self.appId))
        query.addQueryItem('redirect_uri', 'https://oauth.vk.com/blank.html')
        query.addQueryItem('display', 'mobile')
        query.addQueryItem('scope', ','.join(self.appPermission))
        query.addQueryItem('response_type', 'token')
        query.addQueryItem('v', '5.73')
        query.addQueryItem('revoke', '1')

        url.setQuery(query)
        self.load(url)


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


def main():
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.INFO)
    w = Widget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
