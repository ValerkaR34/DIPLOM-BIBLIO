#
# from PyQt6 import QtWidgets
# from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QTableWidget, QPushButton, QLineEdit
# import mysql.connector
# from my_orders import MyOrdersWindow  # Импортируем новый класс MyOrdersWindow
#
# class BooksWindow(QtWidgets.QMainWindow):
#     def __init__(self, connection, user_id):
#         super().__init__()
#         self.connection = connection
#         self.user_id = user_id  # Идентификатор текущего пользователя
#         self.setWindowTitle("Список книг")
#         self.setGeometry(500, 300, 800, 450)  # Увеличиваем высоту для размещения новых элементов
#
#         # Применение стилей к таблице
#         self.table = QTableWidget(self)
#         self.table.setGeometry(20, 20, 760, 360)
#         self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
#         self.table.setStyleSheet("""
#             QTableWidget {
#                 border: 1px solid #ccc;
#                 border-radius: 5px;
#                 gridline-color: #ccc;
#             }
#             QHeaderView::section {
#                 background-color: #f0f0f0;
#                 padding: 4px;
#                 border: 1px solid #ddd;
#                 font-size: 14px;
#             }
#             QTableWidgetItem {
#                 padding: 4px;
#                 color: #555;
#                 font-size: 14px;
#             }
#         """)
#
#         # Элементы для бронирования книг
#         self.book_id_input = QLineEdit(self)
#         self.book_id_input.setPlaceholderText("Введите ID книги")
#         self.book_id_input.setGeometry(20, 385, 200, 30)
#
#         self.reserve_button = QPushButton("Бронировать", self)
#         self.reserve_button.setGeometry(230, 385, 120, 30)
#         self.reserve_button.clicked.connect(self.reserve_book)
#
#         # Кнопка для просмотра заказов
#         self.my_orders_button = QPushButton("Мои заказы", self)
#         self.my_orders_button.setGeometry(360, 385, 120, 30)
#         self.my_orders_button.clicked.connect(self.open_my_orders)
#
#         self.load_books()
#
#     def load_books(self):
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute("""
#                 SELECT b.title, a.name AS author, b.year_published, b.genre, b.status, b.total_copies,
#                        p.name AS publisher, b.id
#                 FROM books b
#                 JOIN authors a ON b.author_id = a.id
#                 JOIN publishers p ON b.publisher_id = p.id
#             """)
#             books = cursor.fetchall()
#
#             self.table.setRowCount(len(books))
#             self.table.setColumnCount(8)
#             self.table.setHorizontalHeaderLabels(
#                 ['Название', 'Автор', 'Год издания', 'Жанр', 'Статус', 'Количество копий', 'Издательство', 'ID'])
#
#             for row, book in enumerate(books):
#                 for col, value in enumerate(book):
#                     item = QTableWidgetItem(str(value))
#                     self.table.setItem(row, col, item)
#
#             self.table.resizeColumnsToContents()
#             cursor.close()
#         except mysql.connector.Error as err:
#             QMessageBox.critical(self, "Ошибка базы данных", str(err))
#         except Exception as e:
#             QMessageBox.critical(self, "Неизвестная ошибка", str(e))
#
#     def reserve_book(self):
#         book_id = self.book_id_input.text().strip()
#         if not book_id.isdigit():
#             QMessageBox.warning(self, "Внимание", "ID книги должен быть числом.")
#             return
#
#         try:
#             cursor = self.connection.cursor()
#
#             # Проверка, бронировал ли пользователь уже эту книгу (независимо от статуса)
#             query = """
#                 SELECT COUNT(*) FROM orders
#                 WHERE user_id = %s AND book_id = %s
#             """
#             cursor.execute(query, (self.user_id, book_id))
#             reservation_count = cursor.fetchone()[0]
#
#             if reservation_count >= 1:
#                 QMessageBox.warning(self, "Ошибка", "Вы не можете бронировать эту книгу более одного раза.")
#                 return
#
#             # Запрос на бронирование
#             insert_query = "INSERT INTO orders (user_id, book_id, status, order_date) VALUES (%s, %s, 'не выдано', NOW())"
#             cursor.execute(insert_query, (self.user_id, book_id))
#
#             # Обновление количества копий книги
#             update_query = "UPDATE books SET total_copies = total_copies - 1 WHERE id = %s AND total_copies > 0"
#             cursor.execute(update_query, (book_id,))
#             if cursor.rowcount == 0:
#                 self.connection.rollback()
#                 QMessageBox.warning(self, "Ошибка",
#                                     "Невозможно зарезервировать книгу. Проверьте ID или доступность книги.")
#             else:
#                 self.connection.commit()
#                 QMessageBox.information(self, "Успех", "Книга успешно забронирована.")
#                 self.load_books()  # Обновление списка книг
#
#             cursor.close()
#         except mysql.connector.Error as err:
#             self.connection.rollback()
#             QMessageBox.critical(self, "Ошибка базы данных", str(err))
#         finally:
#             cursor.close()
#
#     def open_my_orders(self):
#         self.my_orders_window = MyOrdersWindow(self.connection, self.user_id)
#         self.my_orders_window.show()
#
#     def showEvent(self, event):
#         super().showEvent(event)
#         self.showMaximized()  # Открытие окна в максимизированном виде


from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QTableWidget, QPushButton, QLineEdit
import mysql.connector
from my_orders import MyOrdersWindow  # Импортируем новый класс MyOrdersWindow

class BooksWindow(QtWidgets.QMainWindow):
    def __init__(self, connection, user_id):
        super().__init__()
        self.connection = connection
        self.user_id = user_id  # Идентификатор текущего пользователя
        self.setWindowTitle("Список книг")
        self.setGeometry(500, 300, 800, 450)  # Увеличиваем высоту для размещения новых элементов

        # Применение стилей к таблице
        self.table = QTableWidget(self)
        self.table.setGeometry(20, 20, 760, 360)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QTableWidgetItem {
                padding: 4px;
                color: #555;
                font-size: 14px;
            }
        """)

        # Элементы для бронирования книг
        self.book_id_input = QLineEdit(self)
        self.book_id_input.setPlaceholderText("Введите ID книги")
        self.book_id_input.setGeometry(20, 385, 200, 30)

        self.reserve_button = QPushButton("Бронировать", self)
        self.reserve_button.setGeometry(230, 385, 120, 30)
        self.reserve_button.clicked.connect(self.reserve_book)

        # Кнопка для просмотра заказов
        self.my_orders_button = QPushButton("Мои заказы", self)
        self.my_orders_button.setGeometry(360, 385, 120, 30)
        self.my_orders_button.clicked.connect(self.open_my_orders)

        self.load_books()

    def load_books(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT b.title, a.name AS author, b.year_published, b.genre, b.status, b.total_copies,
                       p.name AS publisher, b.id
                FROM books b
                JOIN authors a ON b.author_id = a.id
                JOIN publishers p ON b.publisher_id = p.id
            """)
            books = cursor.fetchall()

            self.table.setRowCount(len(books))
            self.table.setColumnCount(8)
            self.table.setHorizontalHeaderLabels(
                ['Название', 'Автор', 'Год издания', 'Жанр', 'Статус', 'Количество копий', 'Издательство', 'ID'])

            for row, book in enumerate(books):
                for col, value in enumerate(book):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row, col, item)

            self.table.resizeColumnsToContents()
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", str(err))
        except Exception as e:
            QMessageBox.critical(self, "Неизвестная ошибка", str(e))

    def reserve_book(self):
        book_id = self.book_id_input.text().strip()
        if not book_id.isdigit():
            QMessageBox.warning(self, "Внимание", "ID книги должен быть числом.")
            return

        try:
            cursor = self.connection.cursor()

            # Проверка статуса книги и количества копий
            cursor.execute("SELECT status, total_copies FROM books WHERE id = %s", (book_id,))
            book_data = cursor.fetchone()
            if book_data is None:
                QMessageBox.warning(self, "Ошибка", "Книга с таким ID не найдена.")
                return

            status, total_copies = book_data
            if status == 'недоступно':
                QMessageBox.warning(self, "Ошибка", "Книга недоступна для бронирования.")
                return

            # Проверка, бронировал ли пользователь уже эту книгу (независимо от статуса)
            query = """
                SELECT COUNT(*) FROM orders
                WHERE user_id = %s AND book_id = %s
            """
            cursor.execute(query, (self.user_id, book_id))
            reservation_count = cursor.fetchone()[0]

            if reservation_count >= 1:
                QMessageBox.warning(self, "Ошибка", "Вы не можете бронировать эту книгу более одного раза.")
                return

            # Запрос на бронирование
            insert_query = "INSERT INTO orders (user_id, book_id, status, order_date) VALUES (%s, %s, 'не выдано', NOW())"
            cursor.execute(insert_query, (self.user_id, book_id))

            # Обновление количества копий книги
            update_query = "UPDATE books SET total_copies = total_copies - 1 WHERE id = %s AND total_copies > 0"
            cursor.execute(update_query, (book_id,))
            if cursor.rowcount == 0:
                self.connection.rollback()
                QMessageBox.warning(self, "Ошибка",
                                    "Невозможно зарезервировать книгу. Проверьте ID или доступность книги.")
            else:
                # Проверка и обновление статуса книги
                cursor.execute("SELECT total_copies FROM books WHERE id = %s", (book_id,))
                total_copies = cursor.fetchone()[0]
                if total_copies == 0:
                    cursor.execute("UPDATE books SET status = 'недоступно' WHERE id = %s", (book_id,))
                self.connection.commit()
                QMessageBox.information(self, "Успех", "Книга успешно забронирована.")
                self.load_books()  # Обновление списка книг

            cursor.close()
        except mysql.connector.Error as err:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка базы данных", str(err))
        finally:
            cursor.close()

    def open_my_orders(self):
        self.my_orders_window = MyOrdersWindow(self.connection, self.user_id)
        self.my_orders_window.show()

    def showEvent(self, event):
        super().showEvent(event)
        self.showMaximized()  # Открытие окна в максимизированном виде
