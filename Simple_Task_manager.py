import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLineEdit, QMessageBox, QDateTimeEdit
)
from PyQt5.QtCore import QTimer, QDateTime

class Task:
    def __init__(self, description, datetime):
        self.description = description
        self.datetime = datetime

    def __str__(self):
        return f"{self.description} @ {self.datetime.toString('yyyy-MM-dd hh:mm:ss')}"

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager with Time & Notification")
        self.setGeometry(100, 100, 500, 400)
        self.tasks = []
        self.setup_ui()
        self.init_timer()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task description")
        self.layout.addWidget(self.task_input)

        self.time_input = QDateTimeEdit()
        self.time_input.setDateTime(QDateTime.currentDateTime())
        self.time_input.setCalendarPopup(True)
        self.layout.addWidget(self.time_input)

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

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_notifications)
        self.timer.start(1000)  # check every second

    def add_task(self):
        desc = self.task_input.text().strip()
        time = self.time_input.dateTime()

        if desc:
            task = Task(desc, time)
            self.tasks.append(task)
            self.task_list.addItem(str(task))
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Task description cannot be empty!")

    def update_task(self):
        selected_index = self.task_list.currentRow()
        if selected_index >= 0:
            desc = self.task_input.text().strip()
            time = self.time_input.dateTime()
            if desc:
                task = Task(desc, time)
                self.tasks[selected_index] = task
                self.task_list.item(selected_index).setText(str(task))
                self.task_input.clear()
            else:
                QMessageBox.warning(self, "Input Error", "Task description cannot be empty!")
        else:
            QMessageBox.warning(self, "Selection Error", "No task selected!")

    def delete_task(self):
        selected_index = self.task_list.currentRow()
        if selected_index >= 0:
            self.tasks.pop(selected_index)
            self.task_list.takeItem(selected_index)
        else:
            QMessageBox.warning(self, "Selection Error", "No task selected!")

    def check_notifications(self):
        current_time = QDateTime.currentDateTime()
        for i, task in enumerate(self.tasks):
            if task.datetime <= current_time:
                QMessageBox.information(self, "Task Reminder", f"Time for: {task.description}")
                self.tasks.pop(i)
                self.task_list.takeItem(i)
                break  # avoid iteration issues

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
