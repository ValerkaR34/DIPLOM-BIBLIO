

# import sys
# import bcrypt
# from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
# import mysql.connector
# from mysql.connector import Error
# from books_window import BooksWindow  # Импортируем новый класс BooksWindow
# from admin.menu_admin import AdminWindow  # Импортируем окно администратора
#
# class LoginDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.admin_window = None
#         self.books_window = None
#         self.connection = None
#         self.groups = []
#         self.courses = []
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle('Login/Register')
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f0f0f0;
#             }
#             QLineEdit {
#                 border: 2px solid #ccc;
#                 border-radius: 5px;
#                 padding: 10px;
#                 font-size: 16px;
#             }
#             QComboBox {
#                 border: 2px solid #ccc;
#                 border-radius: 5px;
#                 padding: 10px;
#                 font-size: 16px;
#             }
#             QPushButton {
#                 background-color: #007BFF;
#                 border: none;
#                 color: white;
#                 padding: 10px 20px;
#                 text-align: center;
#                 font-size: 16px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #0056b3;
#             }
#             QLabel {
#                 font-size: 16px;
#                 padding: 2px;
#             }
#         """)
#
#         layout = QVBoxLayout()
#
#         self.username_input = QLineEdit(self)
#         self.password_input = QLineEdit(self)
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         self.group_combo = QComboBox(self)
#         self.course_combo = QComboBox(self)
#
#         self.load_groups_and_courses()
#
#         self.login_button = QPushButton('Авторизация', self)
#         self.register_button = QPushButton('Регистрация', self)
#
#         layout.addWidget(QLabel('Логин'))
#         layout.addWidget(self.username_input)
#         layout.addWidget(QLabel('Пароль'))
#         layout.addWidget(self.password_input)
#         layout.addWidget(QLabel('Группа'))
#         layout.addWidget(self.group_combo)
#         layout.addWidget(QLabel('Курс'))
#         layout.addWidget(self.course_combo)
#         layout.addWidget(self.login_button)
#         layout.addWidget(self.register_button)
#         self.setLayout(layout)
#
#         self.login_button.clicked.connect(self.attempt_login)
#         self.register_button.clicked.connect(self.attempt_register)
#
#         self.showMaximized()
#
#     def create_connection(self):
#         """Create a database connection to a MySQL database"""
#         try:
#             self.connection = mysql.connector.connect(
#                 host='localhost',
#                 database='biblio_diplom',
#                 user='root',
#                 password=''  # Убедитесь, что здесь правильный пароль
#             )
#             if self.connection.is_connected():
#                 print('Connected to MySQL database')
#             return self.connection
#         except Error as e:
#             print(e)
#             return None
#
#     def load_groups_and_courses(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 # Загрузка групп
#                 cursor.execute("SELECT id, name FROM groups")
#                 self.groups = cursor.fetchall()
#                 self.group_combo.addItems([group[1] for group in self.groups])
#                 print(f"Группы загружены: {self.groups}")  # Отладочное сообщение
#
#                 # Загрузка курсов
#                 cursor.execute("SELECT id, course_number FROM courses")
#                 self.courses = cursor.fetchall()
#                 self.course_combo.addItems([str(course[1]) for course in self.courses])
#                 print(f"Курсы загружены: {self.courses}")  # Отладочное сообщение
#                 cursor.close()
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при загрузке групп и курсов: {e}')
#                 print(e)  # Для отладки
#
#     def attempt_login(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 username = self.username_input.text()
#                 password = self.password_input.text()
#                 cursor = connection.cursor()
#                 cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
#                 user_data = cursor.fetchone()
#                 cursor.close()
#
#                 if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
#                     QMessageBox.information(self, 'Успех', 'Вы вошли!')
#                     # Проверка роли пользователя и открытие соответствующего окна
#                     if user_data[2] == 'admin':
#                         self.admin_window = AdminWindow()
#                         self.admin_window.show()
#                     else:
#                         self.books_window = BooksWindow(connection, user_data[0])
#                         self.books_window.show()
#                     self.close()
#                 else:
#                     QMessageBox.warning(self, 'Ошибка', 'Имя пользователя или пароль указаны неверно')
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
#                 print(e)  # Для отладки
#             finally:
#                 pass  # Не закрываем соединение сразу после логина
#
#     def attempt_register(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 username = self.username_input.text()
#                 password = self.password_input.text()
#                 group_index = self.group_combo.currentIndex()
#                 course_index = self.course_combo.currentIndex()
#                 group_id = self.groups[group_index][0]
#                 course_id = self.courses[course_index][0]
#
#                 cursor = connection.cursor()
#                 cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#                 if cursor.fetchone():
#                     QMessageBox.warning(self, 'Ошибка', 'Имя пользователя занято!')
#                 else:
#                     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#                     cursor.execute("INSERT INTO users (username, password, role, group_id, course_id) VALUES (%s, %s, 'user', %s, %s)",
#                                    (username, hashed_password, group_id, course_id))
#                     connection.commit()
#                     QMessageBox.information(self, 'Успех', 'Вы успешно зарегистрировались!')
#                 cursor.close()
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
#                 print(e)  # Для отладки
#             finally:
#                 connection.close()
#
# def main():
#     app = QApplication(sys.argv)
#     login_dialog = LoginDialog()
#     login_dialog.exec()
#     sys.exit(app.exec())
#
# if __name__ == '__main__':
#     main()

# import sys
# import bcrypt
# from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
# import mysql.connector
# from mysql.connector import Error
# from books_window import BooksWindow
# from admin.menu_admin import AdminWindow
#
# class LoginDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.admin_window = None
#         self.books_window = None
#         self.connection = None
#         self.groups = []
#         self.courses = []
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle('Login/Register')
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f0f0f0;
#             }
#             QLineEdit {
#                 border: 2px solid #ccc;
#                 border-radius: 5px;
#                 padding: 10px;
#                 font-size: 16px;
#             }
#             QComboBox {
#                 border: 2px solid #ccc;
#                 border-radius: 5px;
#                 padding: 10px;
#                 font-size: 16px;
#             }
#             QPushButton {
#                 background-color: #007BFF;
#                 border: none;
#                 color: white;
#                 padding: 10px 20px;
#                 text-align: center;
#                 font-size: 16px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #0056b3;
#             }
#             QLabel {
#                 font-size: 16px;
#                 padding: 2px;
#             }
#         """)
#
#         layout = QVBoxLayout()
#
#         self.username_input = QLineEdit(self)
#         self.password_input = QLineEdit(self)
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         self.group_combo = QComboBox(self)
#         self.course_combo = QComboBox(self)
#
#         self.load_groups_and_courses()
#
#         self.login_button = QPushButton('Авторизация', self)
#         self.register_button = QPushButton('Регистрация', self)
#
#         layout.addWidget(QLabel('Логин'))
#         layout.addWidget(self.username_input)
#         layout.addWidget(QLabel('Пароль'))
#         layout.addWidget(self.password_input)
#         layout.addWidget(QLabel('Группа'))
#         layout.addWidget(self.group_combo)
#         layout.addWidget(QLabel('Курс'))
#         layout.addWidget(self.course_combo)
#         layout.addWidget(self.login_button)
#         layout.addWidget(self.register_button)
#         self.setLayout(layout)
#
#         self.login_button.clicked.connect(self.attempt_login)
#         self.register_button.clicked.connect(self.attempt_register)
#
#         self.showMaximized()
#
#     def create_connection(self):
#         """Create a database connection to a MySQL database"""
#         try:
#             self.connection = mysql.connector.connect(
#                 host='localhost',
#                 database='biblio_diplom',
#                 user='root',
#                 password=''  # Убедитесь, что здесь правильный пароль
#             )
#             if self.connection.is_connected():
#                 print('Connected to MySQL database')
#             return self.connection
#         except Error as e:
#             print(e)
#             return None
#
#     def load_groups_and_courses(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 # Загрузка групп
#                 cursor.execute("SELECT id, name FROM groups")
#                 self.groups = cursor.fetchall()
#                 self.group_combo.addItems([group[1] for group in self.groups])
#                 print(f"Группы загружены: {self.groups}")  # Отладочное сообщение
#
#                 # Загрузка курсов
#                 cursor.execute("SELECT id, course_number FROM courses")
#                 self.courses = cursor.fetchall()
#                 self.course_combo.addItems([str(course[1]) for course in self.courses])
#                 print(f"Курсы загружены: {self.courses}")  # Отладочное сообщение
#                 cursor.close()
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при загрузке групп и курсов: {e}')
#                 print(e)  # Для отладки
#
#     def attempt_login(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 username = self.username_input.text()
#                 password = self.password_input.text()
#                 cursor = connection.cursor()
#                 cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
#                 user_data = cursor.fetchone()
#                 cursor.close()
#
#                 if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
#                     QMessageBox.information(self, 'Успех', 'Вы вошли!')
#                     # Проверка роли пользователя и открытие соответствующего окна
#                     if user_data[2] == 'admin':
#                         self.admin_window = AdminWindow()
#                         self.admin_window.show()
#                     else:
#                         self.books_window = BooksWindow(connection, user_data[0])
#                         self.books_window.show()
#                     self.close()
#                 else:
#                     QMessageBox.warning(self, 'Ошибка', 'Имя пользователя или пароль указаны неверно')
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
#                 print(e)  # Для отладки
#             finally:
#                 pass  # Не закрываем соединение сразу после логина
#
#     def attempt_register(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 username = self.username_input.text()
#                 password = self.password_input.text()
#                 group_index = self.group_combo.currentIndex()
#                 course_index = self.course_combo.currentIndex()
#                 group_id = self.groups[group_index][0]
#                 course_id = self.courses[course_index][0]
#
#                 cursor = connection.cursor()
#                 cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#                 if cursor.fetchone():
#                     QMessageBox.warning(self, 'Ошибка', 'Имя пользователя занято!')
#                 else:
#                     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#                     cursor.execute("INSERT INTO users (username, password, role, group_id, course_id) VALUES (%s, %s, 'user', %s, %s)",
#                                    (username, hashed_password, group_id, course_id))
#                     connection.commit()
#                     QMessageBox.information(self, 'Успех', 'Вы успешно зарегистрировались!')
#                 cursor.close()
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
#                 print(e)  # Для отладки
#             finally:
#                 connection.close()
#
# def main():
#     app = QApplication(sys.argv)
#     login_dialog = LoginDialog()
#     login_dialog.exec()
#     sys.exit(app.exec())
#
# if __name__ == '__main__':
#     main()

# import sys
# import bcrypt
# from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
# import mysql.connector
# from mysql.connector import Error
# from books_window import BooksWindow
# from admin.menu_admin import AdminWindow
#
# class LoginDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.admin_window = None
#         self.books_window = None
#         self.connection = None
#         self.groups = []
#         self.courses = []
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle('Login/Register')
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #f0f0f0;
#             }
#             QLineEdit {
#                 border: 2px solid #ccc;
#                 border-radius: 5px;
#                 padding: 10px;
#                 font-size: 16px;
#             }
#             QComboBox {
#                 border: 2px solid #ccc;
#                 border-radius: 5px;
#                 padding: 10px;
#                 font-size: 16px;
#             }
#             QPushButton {
#                 background-color: #007BFF;
#                 border: none;
#                 color: white;
#                 padding: 10px 20px;
#                 text-align: center;
#                 font-size: 16px;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #0056b3;
#             }
#             QLabel {
#                 font-size: 16px;
#                 padding: 2px;
#             }
#         """)
#
#         layout = QVBoxLayout()
#
#         self.username_input = QLineEdit(self)
#         self.password_input = QLineEdit(self)
#         self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
#         self.group_combo = QComboBox(self)
#         self.course_combo = QComboBox(self)
#
#         self.load_groups_and_courses()
#
#         self.login_button = QPushButton('Авторизация', self)
#         self.register_button = QPushButton('Регистрация', self)
#
#         layout.addWidget(QLabel('Логин'))
#         layout.addWidget(self.username_input)
#         layout.addWidget(QLabel('Пароль'))
#         layout.addWidget(self.password_input)
#         layout.addWidget(QLabel('Группа'))
#         layout.addWidget(self.group_combo)
#         layout.addWidget(QLabel('Курс'))
#         layout.addWidget(self.course_combo)
#         layout.addWidget(self.login_button)
#         layout.addWidget(self.register_button)
#         self.setLayout(layout)
#
#         self.login_button.clicked.connect(self.attempt_login)
#         self.register_button.clicked.connect(self.attempt_register)
#
#         self.showMaximized()
#
#     def create_connection(self):
#         """Create a database connection to a MySQL database"""
#         try:
#             self.connection = mysql.connector.connect(
#                 host='localhost',
#                 database='biblio_diplom',
#                 user='root',
#                 password=''  # Убедитесь, что здесь правильный пароль
#             )
#             if self.connection.is_connected():
#                 print('Connected to MySQL database')
#             return self.connection
#         except Error as e:
#             print(e)
#             return None
#
#     def load_groups_and_courses(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 cursor = connection.cursor()
#                 # Загрузка групп
#                 cursor.execute("SELECT id, name FROM groups")
#                 self.groups = cursor.fetchall()
#                 self.group_combo.addItems([group[1] for group in self.groups])
#                 print(f"Группы загружены: {self.groups}")  # Отладочное сообщение
#
#                 # Загрузка курсов
#                 cursor.execute("SELECT id, course_number FROM courses")
#                 self.courses = cursor.fetchall()
#                 self.course_combo.addItems([str(course[1]) for course in self.courses])
#                 print(f"Курсы загружены: {self.courses}")  # Отладочное сообщение
#                 cursor.close()
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при загрузке групп и курсов: {e}')
#                 print(e)  # Для отладки
#
#     def attempt_login(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 username = self.username_input.text()
#                 password = self.password_input.text()
#                 cursor = connection.cursor()
#                 cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
#                 user_data = cursor.fetchone()
#                 cursor.close()
#
#                 if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
#                     QMessageBox.information(self, 'Успех', 'Вы вошли!')
#                     # Проверка роли пользователя и открытие соответствующего окна
#                     if user_data[2] == 'admin':
#                         self.admin_window = AdminWindow(connection)
#                         self.admin_window.show()
#                     else:
#                         self.books_window = BooksWindow(connection, user_data[0])
#                         self.books_window.show()
#                     self.close()
#                 else:
#                     QMessageBox.warning(self, 'Ошибка', 'Имя пользователя или пароль указаны неверно')
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
#                 print(e)  # Для отладки
#             finally:
#                 pass  # Не закрываем соединение сразу после логина
#
#     def attempt_register(self):
#         connection = self.create_connection()
#         if connection:
#             try:
#                 username = self.username_input.text()
#                 password = self.password_input.text()
#                 group_index = self.group_combo.currentIndex()
#                 course_index = self.course_combo.currentIndex()
#                 group_id = self.groups[group_index][0]
#                 course_id = self.courses[course_index][0]
#
#                 cursor = connection.cursor()
#                 cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#                 if cursor.fetchone():
#                     QMessageBox.warning(self, 'Ошибка', 'Имя пользователя занято!')
#                 else:
#                     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#                     cursor.execute("INSERT INTO users (username, password, role, group_id, course_id) VALUES (%s, %s, 'user', %s, %s)",
#                                    (username, hashed_password, group_id, course_id))
#                     connection.commit()
#                     QMessageBox.information(self, 'Успех', 'Вы успешно зарегистрировались!')
#                 cursor.close()
#             except Error as e:
#                 QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
#                 print(e)  # Для отладки
#             finally:
#                 connection.close()
#
# def main():
#     app = QApplication(sys.argv)
#     login_dialog = LoginDialog()
#     login_dialog.exec()
#     sys.exit(app.exec())
#
# if __name__ == '__main__':
#     main()


import sys
import bcrypt
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
import mysql.connector
from mysql.connector import Error
from books_window import BooksWindow
from admin.menu_admin import AdminWindow

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.admin_window = None
        self.books_window = None
        self.connection = None
        self.groups = []
        self.courses = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login/Register')
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #007BFF;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                font-size: 16px;
                padding: 2px;
            }
        """)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.group_combo = QComboBox(self)
        self.course_combo = QComboBox(self)

        self.load_groups_and_courses()

        self.login_button = QPushButton('Авторизация', self)
        self.register_button = QPushButton('Регистрация', self)

        layout.addWidget(QLabel('Логин'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Пароль'))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel('Группа'))
        layout.addWidget(self.group_combo)
        layout.addWidget(QLabel('Курс'))
        layout.addWidget(self.course_combo)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

        self.login_button.clicked.connect(self.attempt_login)
        self.register_button.clicked.connect(self.attempt_register)

        self.showMaximized()

    def create_connection(self):
        """Create a database connection to a MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='biblio_diplom',
                user='root',
                password=''  # Убедитесь, что здесь правильный пароль
            )
            if self.connection.is_connected():
                print('Connected to MySQL database')
            return self.connection
        except Error as e:
            print(e)
            return None

    def load_groups_and_courses(self):
        connection = self.create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                # Загрузка групп
                cursor.execute("SELECT id, name FROM groups")
                self.groups = cursor.fetchall()
                self.group_combo.addItems([group[1] for group in self.groups])
                print(f"Группы загружены: {self.groups}")  # Отладочное сообщение

                # Загрузка курсов
                cursor.execute("SELECT id, course_number FROM courses")
                self.courses = cursor.fetchall()
                self.course_combo.addItems([str(course[1]) for course in self.courses])
                print(f"Курсы загружены: {self.courses}")  # Отладочное сообщение
                cursor.close()
            except Error as e:
                QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка при загрузке групп и курсов: {e}')
                print(e)  # Для отладки

    def attempt_login(self):
        connection = self.create_connection()
        if connection:
            try:
                username = self.username_input.text()
                password = self.password_input.text()
                cursor = connection.cursor()
                cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
                user_data = cursor.fetchone()
                cursor.close()

                if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
                    QMessageBox.information(self, 'Успех', 'Вы вошли!')
                    # Проверка роли пользователя и открытие соответствующего окна
                    if user_data[2] == 'admin':
                        self.admin_window = AdminWindow(connection)
                        self.admin_window.show()
                    else:
                        self.books_window = BooksWindow(connection, user_data[0])
                        self.books_window.show()
                    self.close()
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Имя пользователя или пароль указаны неверно')
            except Error as e:
                QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
                print(e)  # Для отладки
            finally:
                pass  # Не закрываем соединение сразу после логина

    def attempt_register(self):
        connection = self.create_connection()
        if connection:
            try:
                username = self.username_input.text()
                password = self.password_input.text()
                group_index = self.group_combo.currentIndex()
                course_index = self.course_combo.currentIndex()
                group_id = self.groups[group_index][0]
                course_id = self.courses[course_index][0]

                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    QMessageBox.warning(self, 'Ошибка', 'Имя пользователя занято!')
                else:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("INSERT INTO users (username, password, role, group_id, course_id) VALUES (%s, %s, 'user', %s, %s)",
                                   (username, hashed_password, group_id, course_id))
                    connection.commit()
                    QMessageBox.information(self, 'Успех', 'Вы успешно зарегистрировались!')
                cursor.close()
            except Error as e:
                QMessageBox.warning(self, 'Ошибка', f'Произошла ошибка: {e}')
                print(e)  # Для отладки
            finally:
                connection.close()

def main():
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    login_dialog.exec()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


