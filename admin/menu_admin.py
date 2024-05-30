# from PyQt6 import QtWidgets
# from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
# import mysql.connector
#
# class AdminWindow(QtWidgets.QMainWindow):
#     def __init__(self, connection):
#         super().__init__()
#         self.connection = connection
#         self.setWindowTitle("Admin Menu")
#         self.setGeometry(500, 300, 1000, 600)
#
#         central_widget = QtWidgets.QWidget()
#         self.setCentralWidget(central_widget)
#
#         layout = QVBoxLayout()
#
#         self.add_book_button = QPushButton("Добавить книгу", self)
#         self.add_book_button.clicked.connect(self.show_add_book_form)
#
#         self.check_orders_button = QPushButton("Проверка заказов", self)
#         self.check_orders_button.clicked.connect(self.show_orders_table)
#
#         layout.addWidget(self.add_book_button)
#         layout.addWidget(self.check_orders_button)
#         self.form_layout = QVBoxLayout()
#         layout.addLayout(self.form_layout)
#
#         central_widget.setLayout(layout)
#
#     def show_add_book_form(self):
#         self.clear_form_layout()
#
#         self.title_input = QLineEdit(self)
#         self.author_input = QComboBox(self)
#         self.year_input = QLineEdit(self)
#         self.genre_input = QLineEdit(self)
#         self.status_input = QComboBox(self)
#         self.copies_input = QLineEdit(self)
#         self.publisher_input = QComboBox(self)
#
#         # Заполнение выпадающих списков авторов и издателей
#         self.load_authors()
#         self.load_publishers()
#         self.status_input.addItems(["доступно", "недоступно"])
#
#         add_button = QPushButton("Добавить книгу", self)
#         add_button.clicked.connect(self.add_book)
#
#         self.form_layout.addWidget(QLabel('Название книги'))
#         self.form_layout.addWidget(self.title_input)
#         self.form_layout.addWidget(QLabel('Автор'))
#         self.form_layout.addWidget(self.author_input)
#         self.form_layout.addWidget(QLabel('Год издания'))
#         self.form_layout.addWidget(self.year_input)
#         self.form_layout.addWidget(QLabel('Жанр'))
#         self.form_layout.addWidget(self.genre_input)
#         self.form_layout.addWidget(QLabel('Статус'))
#         self.form_layout.addWidget(self.status_input)
#         self.form_layout.addWidget(QLabel('Количество копий'))
#         self.form_layout.addWidget(self.copies_input)
#         self.form_layout.addWidget(QLabel('Издательство'))
#         self.form_layout.addWidget(self.publisher_input)
#         self.form_layout.addWidget(add_button)
#
#     def show_orders_table(self):
#         self.clear_form_layout()
#
#         self.orders_table = QTableWidget(self)
#         self.orders_table.setColumnCount(6)
#         self.orders_table.setHorizontalHeaderLabels(['Логин пользователя', 'ID книги', 'Дата заказа', 'Статус', 'Название книги', 'Подтвердить'])
#         self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
#
#         self.load_orders()
#
#         self.form_layout.addWidget(self.orders_table)
#
#     def clear_form_layout(self):
#         while self.form_layout.count():
#             child = self.form_layout.takeAt(0)
#             if child.widget():
#                 child.widget().deleteLater()
#
#     def load_authors(self):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("SELECT id, name FROM authors")
#             authors = cursor.fetchall()
#             for author in authors:
#                 self.author_input.addItem(author[1], author[0])
#             cursor.close()
#         except mysql.connector.Error as err:
#             QMessageBox.critical(self, "Ошибка базы данных", str(err))
#
#     def load_publishers(self):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("SELECT id, name FROM publishers")
#             publishers = cursor.fetchall()
#             for publisher in publishers:
#                 self.publisher_input.addItem(publisher[1], publisher[0])
#             cursor.close()
#         except mysql.connector.Error as err:
#             QMessageBox.critical(self, "Ошибка базы данных", str(err))
#
#     def load_orders(self):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("""
#                 SELECT u.username, o.book_id, o.order_date, o.status, b.title
#                 FROM orders o
#                 JOIN users u ON o.user_id = u.id
#                 JOIN books b ON o.book_id = b.id
#                 WHERE o.status = 'не выдано'
#             """)
#             orders = cursor.fetchall()
#
#             self.orders_table.setRowCount(len(orders))
#
#             for row, order in enumerate(orders):
#                 for col, value in enumerate(order):
#                     item = QTableWidgetItem(str(value))
#                     self.orders_table.setItem(row, col, item)
#
#                 confirm_button = QPushButton("Подтвердить", self)
#                 confirm_button.clicked.connect(lambda _, r=row: self.confirm_order(r))
#                 self.orders_table.setCellWidget(row, 5, confirm_button)
#
#             cursor.close()
#         except mysql.connector.Error as err:
#             QMessageBox.critical(self, "Ошибка базы данных", str(err))
#
#     def add_book(self):
#         title = self.title_input.text().strip()
#         author_id = self.author_input.currentData()
#         year_published = self.year_input.text().strip()
#         genre = self.genre_input.text().strip()
#         status = self.status_input.currentText()
#         total_copies = self.copies_input.text().strip()
#         publisher_id = self.publisher_input.currentData()
#
#         if not title or not year_published.isdigit() or not total_copies.isdigit():
#             QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля правильно.")
#             return
#
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("""
#                 INSERT INTO books (title, author_id, year_published, genre, status, total_copies, publisher_id)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#             """, (title, author_id, int(year_published), genre, status, int(total_copies), publisher_id))
#             self.connection.commit()
#             cursor.close()
#             QMessageBox.information(self, "Успех", "Книга успешно добавлена.")
#             self.clear_fields()
#         except mysql.connector.Error as err:
#             QMessageBox.critical(self, "Ошибка базы данных", str(err))
#
#     def confirm_order(self, row):
#         try:
#             cursor = self.connection.cursor()
#             user_login = self.orders_table.item(row, 0).text()
#             book_id = self.orders_table.item(row, 1).text()
#
#             cursor.execute("""
#                 UPDATE orders SET status = 'выдано'
#                 WHERE book_id = %s AND user_id = (SELECT id FROM users WHERE username = %s)
#             """, (book_id, user_login))
#
#             self.connection.commit()
#             cursor.close()
#             QMessageBox.information(self, "Успех", f"Заказ пользователя {user_login} на книгу {book_id} подтвержден.")
#             self.load_orders()
#         except mysql.connector.Error as err:
#             QMessageBox.critical(self, "Ошибка базы данных", str(err))
#
#     def clear_fields(self):
#         self.title_input.clear()
#         self.year_input.clear()
#         self.genre_input.clear()
#         self.status_input.setCurrentIndex(0)
#         self.copies_input.clear()
#         self.author_input.setCurrentIndex(0)
#         self.publisher_input.setCurrentIndex(0)




from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
import mysql.connector

class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.setWindowTitle("Admin Menu")
        self.setGeometry(500, 300, 1000, 600)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.add_book_button = QPushButton("Добавить книгу", self)
        self.add_book_button.clicked.connect(self.show_add_book_form)

        self.check_orders_button = QPushButton("Проверка заказов", self)
        self.check_orders_button.clicked.connect(self.show_orders_table)

        self.delete_book_button = QPushButton("Удалить книгу", self)
        self.delete_book_button.clicked.connect(self.show_delete_book_form)

        layout.addWidget(self.add_book_button)
        layout.addWidget(self.check_orders_button)
        layout.addWidget(self.delete_book_button)
        self.form_layout = QVBoxLayout()
        layout.addLayout(self.form_layout)

        central_widget.setLayout(layout)

    def show_add_book_form(self):
        self.clear_form_layout()

        self.title_input = QLineEdit(self)
        self.author_input = QComboBox(self)
        self.year_input = QLineEdit(self)
        self.genre_input = QLineEdit(self)
        self.status_input = QComboBox(self)
        self.copies_input = QLineEdit(self)
        self.publisher_input = QComboBox(self)

        # Заполнение выпадающих списков авторов и издателей
        self.load_authors()
        self.load_publishers()
        self.status_input.addItems(["доступно", "недоступно"])

        add_button = QPushButton("Добавить книгу", self)
        add_button.clicked.connect(self.add_book)

        self.form_layout.addWidget(QLabel('Название книги'))
        self.form_layout.addWidget(self.title_input)
        self.form_layout.addWidget(QLabel('Автор'))
        self.form_layout.addWidget(self.author_input)
        self.form_layout.addWidget(QLabel('Год издания'))
        self.form_layout.addWidget(self.year_input)
        self.form_layout.addWidget(QLabel('Жанр'))
        self.form_layout.addWidget(self.genre_input)
        self.form_layout.addWidget(QLabel('Статус'))
        self.form_layout.addWidget(self.status_input)
        self.form_layout.addWidget(QLabel('Количество копий'))
        self.form_layout.addWidget(self.copies_input)
        self.form_layout.addWidget(QLabel('Издательство'))
        self.form_layout.addWidget(self.publisher_input)
        self.form_layout.addWidget(add_button)

    def show_delete_book_form(self):
        self.clear_form_layout()
        self.delete_book_id_input = QLineEdit(self)
        self.delete_book_id_input.setPlaceholderText("Введите ID книги для удаления")
        delete_button = QPushButton("Удалить книгу", self)
        delete_button.clicked.connect(self.delete_book)

        self.books_table = QTableWidget(self)  # Создание таблицы для отображения списка книг
        self.books_table.setColumnCount(2)
        self.books_table.setHorizontalHeaderLabels(['ID', 'Название'])
        self.books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.form_layout.addWidget(QLabel('ID книги для удаления'))
        self.form_layout.addWidget(self.delete_book_id_input)
        self.form_layout.addWidget(delete_button)
        self.form_layout.addWidget(self.books_table)

        self.load_books_list()  # Загрузка списка книг

    def delete_book(self):
        book_id = self.delete_book_id_input.text().strip()
        if not book_id.isdigit():
            QMessageBox.warning(self, "Ошибка", "ID книги должен быть числом.")
            return

        try:
            cursor = self.connection.cursor()
            # Проверяем наличие книги перед удалением
            cursor.execute("SELECT title FROM books WHERE id = %s", (book_id,))
            book = cursor.fetchone()
            if not book:
                QMessageBox.warning(self, "Ошибка", "Книга с таким ID не найдена.")
                return

            reply = QMessageBox.question(self, 'Подтвердить удаление',
                                         f"Вы действительно хотите удалить книгу '{book[0]}' (ID: {book_id})?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
                self.connection.commit()
                QMessageBox.information(self, "Успех", f"Книга '{book[0]}' (ID: {book_id}) успешно удалена.")
                self.load_books_list()  # Перезагрузка списка книг
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка базы данных: {err}")
            print(f"Database error: {err}")  # Логирование для дальнейшего анализа
        except Exception as e:
            QMessageBox.critical(self, "Непредвиденная ошибка", f"Непредвиденная ошибка: {e}")
            print(f"Unexpected error: {e}")  # Логирование для дальнейшего анализа
    def show_orders_table(self):
        self.clear_form_layout()

        self.orders_table = QTableWidget(self)
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels(
            ['Логин пользователя', 'ID книги', 'Дата заказа', 'Статус', 'Название книги', 'Подтвердить'])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_orders()

        self.form_layout.addWidget(self.orders_table)

    def clear_form_layout(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_authors(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name FROM authors")
            authors = cursor.fetchall()
            for author in authors:
                self.author_input.addItem(author[1], author[0])
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", str(err))

    def load_publishers(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, name FROM publishers")
            publishers = cursor.fetchall()
            for publisher in publishers:
                self.publisher_input.addItem(publisher[1], publisher[0])
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", str(err))

    def load_orders(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT u.username, o.book_id, o.order_date, o.status, b.title
                FROM orders o
                JOIN users u ON o.user_id = u.id
                JOIN books b ON o.book_id = b.id
                WHERE o.status = 'не выдано'
            """)
            orders = cursor.fetchall()
            self.orders_table.setRowCount(0)  # Очищаем таблицу перед загрузкой новых данных
            for row_number, order in enumerate(orders):
                self.orders_table.insertRow(row_number)
                for column_number, item in enumerate(order):
                    self.orders_table.setItem(row_number, column_number, QTableWidgetItem(str(item)))
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке заказов: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Непредвиденная ошибка", f"Произошла ошибка: {e}")
            print(f"An unexpected error occurred: {e}")  # Логируем ошибку для анализа

    def add_book(self):
        title = self.title_input.text().strip()
        author_id = self.author_input.currentData()
        year_published = self.year_input.text().strip()
        genre = self.genre_input.text().strip()
        status = self.status_input.currentText()
        total_copies = self.copies_input.text().strip()
        publisher_id = self.publisher_input.currentData()

        if not title or not year_published.isdigit() or not total_copies.isdigit():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля правильно.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                  INSERT INTO books (title, author_id, year_published, genre, status, total_copies, publisher_id)
                  VALUES (%s, %s, %s, %s, %s, %s, %s)
              """, (title, author_id, int(year_published), genre, status, int(total_copies), publisher_id))
            self.connection.commit()
            cursor.close()
            QMessageBox.information(self, "Успех", "Книга успешно добавлена.")
            self.clear_fields()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", str(err))

    def confirm_order(self, row):
        try:
            cursor = self.connection.cursor()
            user_login = self.orders_table.item(row, 0).text()
            book_id = self.orders_table.item(row, 1).text()

            cursor.execute("""
                  UPDATE orders SET status = 'выдано'
                  WHERE book_id = %s AND user_id = (SELECT id FROM users WHERE username = %s)
              """, (book_id, user_login))

            self.connection.commit()
            cursor.close()
            QMessageBox.information(self, "Успех", f"Заказ пользователя {user_login} на книгу {book_id} подтвержден.")
            self.load_orders()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", str(err))

    def load_books_list(self):
        try:
            self.books_table.clearContents()
            self.books_table.setRowCount(0)  # Очищаем таблицу
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, title FROM books")
            books = cursor.fetchall()
            for index, (id, title) in enumerate(books):
                self.books_table.insertRow(index)
                self.books_table.setItem(index, 0, QTableWidgetItem(str(id)))
                self.books_table.setItem(index, 1, QTableWidgetItem(title))
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка при загрузке списка книг: {err}")
            print(f"Error loading books list: {err}")
        except Exception as e:
            QMessageBox.critical(self, "Непредвиденная ошибка", f"Произошла ошибка: {e}")
            print(f"Error while loading books list: {e}")

    def clear_fields(self):
        self.title_input.clear()
        self.year_input.clear()
        self.genre_input.clear()
        self.status_input.setCurrentIndex(0)
        self.copies_input.clear()
        self.author_input.setCurrentIndex(0)
        self.publisher_input.setCurrentIndex(0)


