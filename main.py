from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize

import os

from ui_main import Ui_MainWindow

back = [".."]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Записываем в строку поиска путь к текущей директории
        self.ui.line_edit.setText(os.getcwd() + "\\")
        # Добавляем директории и файлы, расположенные в текущей директории
        self.ui.list_box.addItems(back + sorted(os.listdir()))

        # При двойном клике по каталогу или файлу открываем его
        self.ui.list_box.itemDoubleClicked.connect(self.select_element)
        # При изменение строки поиска обновляем текущий список файлов и каталогов
        self.ui.line_edit.textChanged.connect(self.line_edit_changed)

    def line_edit_changed(self):
        self.ui.list_box.clear()
        # Если строка поиска пуста, то выводим список дисков на ПК
        if self.ui.line_edit.text() == "":
            # Удаляем слэш из ссылок, чтоб после переход к след. папке небыло двух слэшей
            list_drives = [drive.strip("\\") for drive in os.listdrives()]
            self.ui.list_box.addItems(list_drives)
        # Если в строке поиска что-то есть
        else:
            self.ui.list_box.addItems(back + os.listdir(self.ui.line_edit.text()))

    def select_element(self, e):
        # Если это каталог, то обновляем строку поиска с этим каталогом (двигаемся вглубь)
        if "." not in e.text():
            self.ui.line_edit.setText(self.ui.line_edit.text() + e.text() + "\\")
        # Если это "..", то убираем из строки поиска текущий каталог (возвращаемся назада)
        elif ".." == e.text():
            new_url = "\\".join(self.ui.line_edit.text().split("\\")[:-2]) + "\\"
            # Если юзер находился в корне диска, то выводим список дисков
            if new_url == "\\":
                self.ui.line_edit.setText("")
            # Пользователь не в корне диска
            else:
                self.ui.line_edit.setText("\\".join(self.ui.line_edit.text().split("\\")[:-2]) + "\\")
        # Если это файл, то открываем его
        elif "." in e.text():
            os.startfile(self.ui.line_edit.text() + e.text())


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
