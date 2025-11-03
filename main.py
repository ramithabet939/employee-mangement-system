import sys
from datetime import datetime
import sqlite3


from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, \
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QToolBar, QStatusBar, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Employee Managment System')
        grid = QGridLayout()


        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        add_employee_action = QAction(QIcon("icons/add.png"), "Add Employee",self)
        add_employee_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_employee_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        edit_employee_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_employee_action.triggered.connect(self.search)
        edit_menu_item.addAction(edit_employee_action)


        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Employee", "Phone Number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create Toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_employee_action)
        toolbar.addAction(edit_employee_action)

        # Create a status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDI()
        dialog.exec()

class AboutDI(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Information')
        content = """
        This app was created during my internship as a simple app to help manage employee information.
        Feel free to modify and reuse this app.
        """
        self.setText(content)

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Employee Details')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Get student name from selected row
        index = main_window.table.currentRow()
        employee_name = main_window.table.item(index, 1).text()

        self.employee_id = main_window.table.item(index, 0).text()

        # ADD EMPLOYEE NAME
        layout = QVBoxLayout()
        self.employee_name = QLineEdit(employee_name)
        self.employee_name.setPlaceholderText(" Enter Employee Name")
        layout.addWidget(self.employee_name)

        department = main_window.table.item(index, 2).text()

        # ADD COMBO BOX FOR DEPARTMENT
        self.department = QComboBox()
        department_name = ["Sales", "HR", "Managment", "Accounting", "IT"]
        self.department.addItems(department_name)
        self.department.setCurrentText(department)
        layout.addWidget(self.department)

        mobile = main_window.table.item(index, 3).text()

        # ADD MOBILE WIDGET
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Enter Employee mobile number")
        layout.addWidget(self.mobile)

        # Submit Button
        button = QPushButton("Update", self)
        button.clicked.connect(self.update_employee)
        self.setLayout(layout)

    def update_employee(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
            (
                self.employee_name.text(),
                self.department.itemText(self.department.currentIndex()),
                self.mobile.text(),
                self.employee_id
            )
        )
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()





class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Employee')


        layout = QGridLayout()
        confirmation = QLabel(" Are you sure you want to delete this Employee?")
        yes = QPushButton("Yes", self)
        no = QPushButton("No", self)
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_employee)

    def delete_employee(self):
        index = main_window.table.currentRow()
        employee_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (employee_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()
        confirmation_delete = QMessageBox()
        confirmation_delete.setWindowTitle = ("Sucess")
        confirmation_delete.setText("The employee has been removed successfully")
        confirmation_delete.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Enter Employee Details')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # ADD EMPLOYEE NAME
        layout = QVBoxLayout()
        self.employee_name = QLineEdit()
        self.employee_name.setPlaceholderText("Enter Employee Name")
        layout.addWidget(self.employee_name)

        # ADD COMBO BOX FOR DEPARTMENT
        self.department = QComboBox()
        department_name = ["Sales", "HR", "Managment", "Accounting", "IT"]
        self.department.addItems(department_name)
        layout.addWidget(self.department)

        # ADD MOBILE WIDGET
        self.mobile =  QLineEdit()
        self.mobile.setPlaceholderText("Enter Employee mobile number")
        layout.addWidget(self.mobile)

        #Submit Button
        button = QPushButton("Add Employee", self)
        button.clicked.connect(self.add_employee)
        self.setLayout(layout)




    def add_employee(self):
        name = self.employee_name.text()
        department = self.department.itemText(self.department.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)', (name, department, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Employee')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # ADD EMPLOYEE NAME
        layout = QVBoxLayout()
        self.employee_name = QLineEdit()
        self.employee_name.setPlaceholderText("Name")
        layout.addWidget(self.employee_name)

        # Search Button
        button = QPushButton("Search", self)
        button.clicked.connect(self.search_employee)
        layout.addWidget(button)

        self.setLayout(layout)


    def search_employee(self):
        name = self.employee_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        cursor.close()
        connection.close()
        main_window.load_data()

        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)





app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())














