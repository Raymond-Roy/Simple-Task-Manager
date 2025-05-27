import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit, QMessageBox
)

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Task Manager")
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task")
        self.layout.addWidget(self.task_input)

        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Task")
        self.update_btn = QPushButton("Update Task")
        self.delete_btn = QPushButton("Delete Task")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)

        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

        self.add_btn.clicked.connect(self.add_task)
        self.update_btn.clicked.connect(self.update_task)
        self.delete_btn.clicked.connect(self.delete_task)

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            self.task_list.addItem(task_text)
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Task cannot be empty!")

    def update_task(self):
        selected_item = self.task_list.currentItem()
        new_text = self.task_input.text().strip()
        if selected_item and new_text:
            selected_item.setText(new_text)
            self.task_input.clear()
        elif not selected_item:
            QMessageBox.warning(self, "Selection Error", "No task selected!")
        else:
            QMessageBox.warning(self, "Input Error", "Task cannot be empty!")

    def delete_task(self):
        selected_row = self.task_list.currentRow()
        if selected_row >= 0:
            self.task_list.takeItem(selected_row)
        else:
            QMessageBox.warning(self, "Selection Error", "No task selected!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
