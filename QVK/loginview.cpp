#include "loginview.h"

LogInView::LogInView(QWidget *parent)
    : QWebEngineView(parent) {
    connect(this, &LogInView::urlChanged, [this](const QUrl &newUrl) {
        QUrl url = newUrl.toString().replace("#","?");

        if (url.hasQuery()) {
            QScopedPointer<QUrlQuery> q(new QUrlQuery(url.query().replace("#", "?")));
            if (q->hasQueryItem("access_token")) {
                m_accessToken = q->queryItemValue("access_token");
                emit tokenTaken(m_accessToken);
                deleteLater();
                qDebug() << "TOKEN: " << m_accessToken;
            }
        }
    });
}

void LogInView::loadAuthPage() {
    QUrl url("https://oauth.vk.com/authorize");
    QScopedPointer<QUrlQuery> q(new QUrlQuery());

    q->addQueryItem("client_id", QString::number(m_appId));
    q->addQueryItem("redirect_uri", "https://oauth.vk.com/blank.html");
    q->addQueryItem("display", "mobile");
    q->addQueryItem("scope", QString::number(m_appPermission));
    q->addQueryItem("response_type", "token");
    q->addQueryItem("v", "5.73");
    q->addQueryItem("revoke", "1");

    url.setQuery(*q);
    load(url);
}
