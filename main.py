from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize

import os
back = ['..']

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('btc mainer')
        self.setFixedSize(QSize(600, 400))

        self.line_edit = QLineEdit(os.getcwd() + '\\')
        self.list_box = QListWidget()
        self.list_box.addItems(back + sorted(os.listdir()))

        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.list_box)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.list_box.itemClicked.connect(self.add_url_dir)
        self.line_edit.textChanged.connect(self.line_edit_changed)


    def line_edit_changed(self):
        self.list_box.clear()
        self.list_box.addItems(back + os.listdir(self.line_edit.text()))

    def add_url_dir(self, e):
        if '.' not in e.text():
            self.line_edit.setText(self.line_edit.text() + e.text() + '\\')
        elif '..' == e.text():
            self.line_edit.setText('\\'.join(self.line_edit.text().split('\\')[:-2]) + '\\')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
