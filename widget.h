#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QListWidget>
#include <QListWidgetItem>
#include <QTextEdit>
#include "loginview.h"

namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();
public slots:
    void closeLogInView();
private:
    LogInView *m_logInView;
    Ui::Widget *ui;
};

#endif // WIDGET_H
