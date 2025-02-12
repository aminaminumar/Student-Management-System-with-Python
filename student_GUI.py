from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import csv
STUDENT_FILE = "Students_Record.csv"

class StudentManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(100, 100, 400, 300)
        
        # Create labels and input fields
        self.label_id = QLabel("Student ID:")
        self.entry_id = QLineEdit()
        
        self.label_name = QLabel("Name:")
        self.entry_name = QLineEdit()
        
        self.label_age = QLabel("Age:")
        self.entry_age = QLineEdit()
        
        self.label_grade = QLabel("Grade:")
        self.entry_grade = QLineEdit()
        
        # Create buttons
        self.btn_add = QPushButton("Add Student")
        self.btn_update = QPushButton("Update Student")
        self.btn_delete = QPushButton("Delete Student")
        self.btn_view = QPushButton("View Students")
        
        # Connect buttons to functions
        self.btn_add.clicked.connect(self.add_student)
        self.btn_update.clicked.connect(self.update_student)
        self.btn_delete.clicked.connect(self.delete_student)
        self.btn_view.clicked.connect(self.view_students)
        
        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_id)
        layout.addWidget(self.entry_id)
        layout.addWidget(self.label_name)
        layout.addWidget(self.entry_name)
        layout.addWidget(self.label_age)
        layout.addWidget(self.entry_age)
        layout.addWidget(self.label_grade)
        layout.addWidget(self.entry_grade)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_view)
        
        self.setLayout(layout)
    
    def add_student(self):
        student_id = self.entry_id.text().strip()
        name = self.entry_name.text().strip()
        age = self.entry_age.text().strip()
        grade = self.entry_grade.text().strip()
        
        if not (student_id and name and age and grade):
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return
        
        students = self.load_students()
        if student_id in students:
            QMessageBox.warning(self, "Warning", "Student ID already exists!")
            return
        
        students[student_id] = [name, age, grade]
        self.save_students(students)
        QMessageBox.information(self, "Success", "Student added successfully!")
    
    def update_student(self):
        student_id = self.entry_id.text().strip()
        if not student_id:
            QMessageBox.warning(self, "Warning", "Enter Student ID to update!")
            return
        
        students = self.load_students()
        if student_id not in students:
            QMessageBox.warning(self, "Warning", "Student not found!")
            return
        
        name = self.entry_name.text().strip()
        age = self.entry_age.text().strip()
        grade = self.entry_grade.text().strip()
        
        if name:
            students[student_id][0] = name
        if age:
            students[student_id][1] = age
        if grade:
            students[student_id][2] = grade
        
        self.save_students(students)
        QMessageBox.information(self, "Success", "Student updated successfully!")
    
    def delete_student(self):
        student_id = self.entry_id.text().strip()
        if not student_id:
            QMessageBox.warning(self, "Warning", "Enter Student ID to delete!")
            return
        
        students = self.load_students()
        if student_id not in students:
            QMessageBox.warning(self, "Warning", "Student not found!")
            return
        
        del students[student_id]
        self.save_students(students)
        QMessageBox.information(self, "Success", "Student deleted successfully!")
    
    def view_students(self):
        students = self.load_students()
        if not students:
            QMessageBox.information(self, "Info", "No students found.")
            return
        
        student_list = "\n".join([f"ID: {sid}, Name: {data[0]}, Age: {data[1]}, Grade: {data[2]}" for sid, data in students.items()])
        QMessageBox.information(self, "Student Records", student_list)
    
    def load_students(self):
        students = {}
        try:
            with open(STUDENT_FILE, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4:
                        students[row[0]] = row[1:]
        except FileNotFoundError:
            pass
        return students
    
    def save_students(self, students):
        with open(STUDENT_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            for student_id, data in students.items():
                writer.writerow([student_id] + data)

if __name__ == "__main__":
    app = QApplication([])
    window = StudentManagement()
    window.show()
    app.exec()
