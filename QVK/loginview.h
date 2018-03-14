#ifndef LOGINVIEW_H
#define LOGINVIEW_H

#include <QtWebEngineWidgets/QWebEngineView>
#include <QtWidgets/QWidget>
#include <QtWidgets/QGridLayout>
#include <QUrlQuery>
#include <QUrl>

class LogInView : public QWebEngineView {
    Q_OBJECT

public:
    explicit LogInView(QWidget *parent = nullptr);
    void loadAuthPage();
signals:
    void tokenTaken(const QString);
private:
    const int m_appId = 6390333;
    const int m_appPermission = 524288;
    QString m_accessToken = QStringLiteral("");
};

#endif // LOGINVIEW_H
