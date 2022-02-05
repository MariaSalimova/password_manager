import sys
import sqlite3
from password_manager_ui import Ui_MainWindow
from PyQt5 import QtWidgets
from password import Password
import sets_of_characters


class PasswordManager(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.connection = sqlite3.connect('passwords_db.sqlite')
        self.password_save_pushbutton.clicked.connect(self.save_password)
        self.save_file_choice_pushbutton.clicked.connect(self.save_file_choice)
        self.search_button.clicked.connect(self.search)
        self.save_file_name = None
        self.password_generate_button.clicked.connect(self.generate_password)
        self.password_status = 0
        self.resource_lineedit.textChanged.connect(self.update_current_resource)
        self.login_lineedit.textChanged.connect(self.update_current_login)
        self.email_lineedit.textChanged.connect(self.update_current_email)
        self.password_lineedit.textChanged.connect(self.update_current_password)
        self.current_resource = self.resource_lineedit.text()
        self.current_login = self.login_lineedit.text()
        self.current_email = self.email_lineedit.text()
        self.current_password = self.password_lineedit.text()
        if str(self.password_type_combobox.currentText()) == 'Собственный пароль':
            self.password_generate_button.setCheckable(False)
            self.password_length_spinbox.setEnabled(False)
        else:
            self.password_generate_button.setCheckable(True)
            self.password_length_spinbox.setEnabled(True)

    def update_current_resource(self):
        self.current_resource = self.resource_lineedit.text()

    def update_current_login(self):
        self.current_login = self.login_lineedit.text()

    def update_current_email(self):
        self.current_email = self.email_lineedit.text()

    def update_current_password(self):
        self.current_password = self.password_lineedit.text()
        self.password_status_label.setText(Password.password_reliability_check(self.current_password))

    def update_status(self):
        if self.password_status == 1:
            self.password_status_label.setText('Ненадежный пароль')
        elif self.password_status == 2:
            self.password_status_label.setText('Пароль среднего уровня надежности')
        elif self.password_status == 0:
            self.password_status_label.setText('')
        else:
            self.password_status_label.setText('Надежный пароль')

    def input_password(self):
        # обрабатывает введенный пользователем парль
        self.current_password = str(self.password_lineedit.text())
        self.self.password_status = self.current_password_object.password_reliability_check(self.current_password)
        self.password_status_label.setText(self.self.password_status)

    def generate_password(self):
        # отвечает за генерацию пароля
        self.password_generate_button.setCheckable(True)
        self.password_length_spinbox.setEnabled(True)
        self.current_password_characters = ''
        if str(self.password_generation_instructions_combobox.currentText()) == 'Цифры':
            self.current_password_characters = sets_of_characters.numbers
        elif str(self.password_generation_instructions_combobox.currentText()) == 'Буквы':
            self.current_password_characters = sets_of_characters.letters
        elif str(self.password_generation_instructions_combobox.currentText()) == 'Символы':
            self.current_password_characters = sets_of_characters.symbols
        elif str(self.password_generation_instructions_combobox.currentText()) == 'Буквы + цифры':
            self.current_password_characters = sets_of_characters.letters_numbers
        elif str(self.password_generation_instructions_combobox.currentText()) == 'Буквы + Цифры + Символы':
            self.current_password_characters = sets_of_characters.letters_numbers_symbols
        self.current_password_length = int(self.password_length_spinbox.text())
        self.current_password_object = Password(self.current_password_length, self.current_password_characters)
        self.current_password = self.current_password_object.generate_password()
        self.password_status = self.current_password_object.password_reliability_check(self.current_password)
        self.password_lineedit.setText(self.current_password)
        self.password_status_label.setText(self.self.password_status)

    def save_password(self):
        # сохраняет пароль в базу данных
        if self.save_to_database_radiobutton.isChecked():
            self.save_file_choice_pushbutton.setCheckable(False)
            validation = QtWidgets.QMessageBox.question(self, '', 'Сохранить?',
                                                        QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if validation == QtWidgets.QMessageBox.Yes:
                addition_cursor = self.connection.cursor()
                ids = addition_cursor.execute("""SELECT id FROM passwords""").fetchall()
                if ids:
                    current_id = int(ids[-1][0] + 1)
                else:
                    current_id = 1
                que = f"""INSERT INTO passwords VALUES (?, ?, ?, ?, ?)
                """
                print(current_id, self.current_resource, self.current_login,
                                                   self.current_email, self.current_password)
                addition_cursor.execute(que, (current_id, self.current_resource, self.current_login,
                                                   self.current_email, self.current_password))
                self.connection.commit()
        # сохраняет пароль в выбраный пользователем файл
        elif self.save_to_file_radiobutton.isChecked():
            self.save_file_choice_pushbutton.setCheckable(True)
            if self.save_file_name:
                validation = QtWidgets.QMessageBox.question(self, '', f'Сохранить в {self.save_file_name}',
                                                            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if validation == QtWidgets.QMessageBox.Yes:
                    with open(self.save_file_name, mode='w') as current_save_file:
                        if self.current_resource:
                            current_save_file.write(f'"РЕСУРС: {self.current_resource}')
                        if self.current_login:
                            current_save_file.write(f'ЛОГИН: {self.current_login}')
                        if self.current_email:
                            current_save_file.write(f'"ЭЛЕКТРОННАЯ ПОЧТА: {self.current_email}')
                        if self.current_password:
                            current_save_file.write(f'ПАРОЛЬ: {self.current_password}')
            else:
                warning = QtWidgets.QErrorMessage()
                warning.showMessage('Не выбран файл для сохранения')
        self.login_lineedit.clear()
        self.password_lineedit.clear()
        self.resource_lineedit.clear()
        self.email_lineedit.clear()
        self.password_length_spinbox.setValue(0)

    def save_file_choice(self):
        self.save_file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл', '',
                                                                    'Текстовый файл (*.txt)')[0]

    def search(self):
        search_cursor = self.connection.cursor()
        res = None
        if self.search_by_combobox.currentText() == 'Электронная почта':
            que = """SELECT * FROM passwords
            WHERE email = ?"""
            res = search_cursor.execute(que, (self.search_lineedit.text(),)).fetchall()
        elif self.search_by_combobox.currentText() == 'Логин':
            que = """SELECT * FROM passwords
            WHERE login = ?"""
            res = search_cursor.execute(que, (self.search_lineedit.text(),)).fetchall()
        elif self.search_by_combobox.currentText() == 'Ресурс':
            que = """SELECT * FROM passwords
            WHERE resource = ?"""
            res = search_cursor.execute(que, (self.search_lineedit.text(),)).fetchall()
        self.passwords_tablewidget.setRowCount(len(res))
        self.passwords_tablewidget.setColumnCount(5)
        self.passwords_tablewidget.setHorizontalHeaderLabels(['id', 'Ресурс', 'Логин', 'Электронная почта', 'Пароль'])
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.passwords_tablewidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))
        self.passwords_tablewidget.resizeColumnsToContents()
        self.passwords_tablewidget.resizeRowsToContents()


sys._excepthook = sys.excepthook

def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook
if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    password_manager_app = PasswordManager()
    password_manager_app.show()
    sys.exit(application.exec())
