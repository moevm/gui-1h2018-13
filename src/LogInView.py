import logging
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import QUrl, QUrlQuery
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
