from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QTextEdit


class SearchWidget(QWidget):
    resultList = None
    searchButton = None
    searchText = None

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.resultList = QListWidget(self)
        self.searchButton = QPushButton(self)
        self.searchButton.setText('Search')
        self.searchText = QTextEdit(self)
        layout.addWidget(self.resultList)
        secondLayout = QHBoxLayout(self)
        secondLayout.addWidget(self.searchText)
        secondLayout.addWidget(self.searchButton)
        layout.addItem(secondLayout)
        self.setLayout(layout)
