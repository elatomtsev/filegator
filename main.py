from PySide6.QtWidgets import QMainWindow, QLineEdit, QListWidget, QApplication
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

import os

from ui_main import Ui_MainWindow

back = [".."]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Записываем в строку поиска путь к текущей директории
        self.ui.left_line_edit.setText(os.getcwd() + "\\")
        self.ui.right_line_edit.setText(os.getcwd() + "\\")
        # Добавляем директории и файлы, расположенные в текущей директории
        self.ui.left_list_box.addItems(back + sorted(os.listdir()))
        self.ui.right_list_box.addItems(back + sorted(os.listdir()))

        # При двойном клике по каталогу или файлу открываем его
        self.ui.left_list_box.itemDoubleClicked.connect(
            lambda: self.select_element(self.ui.left_line_edit, self.ui.left_list_box)
        )
        self.ui.right_list_box.itemDoubleClicked.connect(
            lambda: self.select_element(self.ui.right_line_edit, self.ui.right_list_box)
        )
        # При изменение строки поиска обновляем текущий список файлов и каталогов
        self.ui.left_line_edit.textChanged.connect(
            lambda: self.left_line_edit_changed(self.ui.left_line_edit, self.ui.left_list_box)
        )
        self.ui.right_line_edit.textChanged.connect(
            lambda: self.left_line_edit_changed(self.ui.right_line_edit, self.ui.right_list_box)
        )

        self.ui.left_list_box.itemClicked.connect(self.status_upd)

    def left_line_edit_changed(self, line_edit: QLineEdit, list_box: QListWidget):
        list_box.clear()

        # Если строка поиска пуста, то выводим список дисков на ПК
        if line_edit.text() == "":
            # Удаляем слэш из ссылок, чтоб после переход к след. папке небыло двух слэшей
            list_drives = [drive.strip("\\") for drive in os.listdrives()]
            list_box.addItems(list_drives)

        # Если в строке поиска что-то есть
        else:
            list_box.addItems(back + os.listdir(line_edit.text()))

    def select_element(self, line_edit: QLineEdit, list_box: QListWidget):
        # Если это "..", то убираем из строки поиска текущий каталог (возвращаемся назада)
        if ".." == list_box.currentItem().text():
            new_url = "\\".join(line_edit.text().split("\\")[:-2]) + "\\"
            # Если юзер находился в корне диска, то выводим список дисков
            if new_url == "\\":
                line_edit.setText("")
            # Пользователь не в корне диска
            else:
                line_edit.setText("\\".join(line_edit.text().split("\\")[:-2]) + "\\")

        # Если это каталог, то обновляем строку поиска с этим каталогом (двигаемся вглубь)
        elif os.path.isdir(line_edit.text() + list_box.currentItem().text()):
            line_edit.setText(line_edit.text() + list_box.currentItem().text() + "\\")

        # Если это файл, то открываем его
        elif os.path.isfile(line_edit.text() + list_box.currentItem().text()):
            os.startfile(line_edit.text() + list_box.currentItem().text())

    def status_upd(self):
        # !!!!!!!!!!!Баг при выходе в меню дисков (в текущем файле отображается прошлый диск), можно сделать, чтоб при выходе из папки статусбар обновлялся
        self.ui.status_bar.showMessage(self.ui.left_line_edit.text() + self.ui.left_list_box.currentItem().text())


if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    window.show()
    app.exec()
