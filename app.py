import sys
import logging
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QUrl, QUrlQuery
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class LogInView(QWebEngineView):
    """
    This is class where user can login
    """
    appId = 6390333
    appPermission = 524288

    tokenTaken = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        print('Create LogInView...')
        self.loadAuthPage()
        self.urlChanged.connect(self.onUrlChanged)

    @Slot(QUrl, name='onUrlChanged')
    def onUrlChanged(self, newUrl: QUrl):
        """
        URL changed handler.
        """
        url = QUrl(newUrl.toString().replace('#', '?'))

        print(f'url was changed to {url.toString()}')
        if url.hasQuery():
            query = QUrlQuery(url.query())
            if query.hasQueryItem('access_token'):
                token = query.queryItemValue('access_token')
                self.tokenTaken.emit(token)
                self.deleteLater()
                print(f'TOKEN: {token}')

    def loadAuthPage(self):
        """
        This method loads auth page, so user can login in VK.
        """
        url = QUrl('https://oauth.vk.com/authorize')
        query = QUrlQuery()

        query.addQueryItem('client_id', str(self.appId))
        query.addQueryItem('redirect_uri', 'https://oauth.vk.com/blank.html')
        query.addQueryItem('display', 'mobile')
        query.addQueryItem('scope', str(self.appPermission))
        query.addQueryItem('response_type', 'token')
        query.addQueryItem('v', '5.73')
        query.addQueryItem('revoke', '1')

        url.setQuery(query)
        self.load(url)


class Widget(QWidget):
    """
    This class is the main class of the application.
    """
    webView = None

    @Slot(name='closeLogInView')
    def closeLogInView(self):
        """
        This slot closes the login view, when token is being taken.
        """
        print('Closing LogInWidget...')
        self.webView.close()
        self.webView.tokenTaken.disconnect(self.closeLogInView)
        self.webView = None

    def __init__(self, parent=None):
        super().__init__(parent)
        print('Creating main Widget...')
        self.setWindowTitle('Messenger')
        self.setLayout(QHBoxLayout())
        self.webView = LogInView(self)
        self.webView.tokenTaken.connect(self.closeLogInView)
        self.layout().addWidget(self.webView)


def main():
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
