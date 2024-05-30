from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QTableWidget
import mysql.connector

class MyOrdersWindow(QtWidgets.QMainWindow):
    def __init__(self, connection, user_id):
        super().__init__()
        self.connection = connection
        self.user_id = user_id
        self.setWindowTitle("Мои заказы")
        self.setGeometry(600, 300, 800, 450)

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

        self.load_orders()

    def load_orders(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT b.title, a.name AS author, o.order_date, o.status
                FROM orders o
                JOIN books b ON o.book_id = b.id
                JOIN authors a ON b.author_id = a.id
                WHERE o.user_id = %s
            """, (self.user_id,))
            orders = cursor.fetchall()

            self.table.setRowCount(len(orders))
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(['Название', 'Автор', 'Дата заказа', 'Статус'])

            for row, order in enumerate(orders):
                for col, value in enumerate(order):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row, col, item)

            self.table.resizeColumnsToContents()
            cursor.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Ошибка базы данных", str(err))
        except Exception as e:
            QMessageBox.critical(self, "Неизвестная ошибка", str(e))
