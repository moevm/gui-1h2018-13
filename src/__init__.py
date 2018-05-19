import logging
import sys

from PyQt5.QtWidgets import QApplication

from .Widget import Widget


def main():
    app = QApplication(sys.argv)
    logging.basicConfig(level=logging.INFO)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
