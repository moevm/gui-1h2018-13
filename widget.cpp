#include "widget.h"
#include "ui_widget.h"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget) {
    resize(800, 600);
    ui->setupUi(this);
    ui->dialogListWidget->hide();
    ui->messagesListWidget->hide();
    ui->messageTextEdit->hide();
    ui->sendPushButton->hide();
    m_logInView = new LogInView(this);
    layout()->addWidget(m_logInView);
    m_logInView->loadAuthPage();

    connect(m_logInView, &LogInView::tokenTaken,
            this, &Widget::closeLogInView);
}

Widget::~Widget() {
    delete ui;
}

void Widget::closeLogInView() {
    m_logInView->close();
    disconnect(m_logInView, &LogInView::tokenTaken,
               this, &Widget::closeLogInView);
    ui->dialogListWidget->show();
    ui->messagesListWidget->show();
    ui->messageTextEdit->show();
    ui->sendPushButton->show();
}
