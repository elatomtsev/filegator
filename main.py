from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize

import os

back = [".."]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("btc mainer")
        self.setFixedSize(QSize(600, 400))

        # Записываем в строку поиска путь к текущей директории
        self.line_edit = QLineEdit(os.getcwd() + "\\")
        self.list_box = QListWidget()
        # Добавляем директории и файлы, расположенные в текущей директории
        self.list_box.addItems(back + sorted(os.listdir()))

        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.list_box)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        # При двойном клике по каталогу или файлу открываем его
        self.list_box.itemDoubleClicked.connect(self.select_element)
        # При изменение строки поиска обновляем текущий список файлов и каталогов
        self.line_edit.textChanged.connect(self.line_edit_changed)

    def line_edit_changed(self):
        self.list_box.clear()
        # Если строка поиска пуста, то выводим список дисков на ПК
        if self.line_edit.text() == "":
            # Удаляем слэш из ссылок, чтоб после переход к след. папке небыло двух слэшей
            list_drives = [drive.strip("\\") for drive in os.listdrives()]
            self.list_box.addItems(list_drives)
        # Если в строке поиска что-то есть
        else:
            self.list_box.addItems(back + os.listdir(self.line_edit.text()))

    def select_element(self, e):
        # Если это каталог, то обновляем строку поиска с этим каталогом (двигаемся вглубь)
        if "." not in e.text():
            self.line_edit.setText(self.line_edit.text() + e.text() + "\\")
        # Если это "..", то убираем из строки поиска текущий каталог (возвращаемся назада)
        elif ".." == e.text():
            new_url = "\\".join(self.line_edit.text().split("\\")[:-2]) + "\\"
            # Если юзер находился в корне диска, то выводим список дисков
            if new_url == "\\":
                self.line_edit.setText("")
            # Пользователь не в корне диска
            else:
                self.line_edit.setText("\\".join(self.line_edit.text().split("\\")[:-2]) + "\\")
        # Если это файл, то открываем его
        elif "." in e.text():
            os.startfile(self.line_edit.text() + e.text())


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
