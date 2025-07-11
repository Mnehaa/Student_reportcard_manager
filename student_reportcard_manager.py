import json
import uuid
import tkinter as tk
from tkinter import messagebox, simpledialog

class Student:
    def __init__(self, name, student_id, subjects=None):
        self.id = student_id
        self.name = name
        self.subjects = subjects if subjects else {}

    def add_subject(self, subject, score):
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        self.subjects[subject] = score

    def calculate_average(self):
        if not self.subjects:
            return 0
        return sum(self.subjects.values()) / len(self.subjects)

    def get_grade(self):
        avg = self.calculate_average()
        if avg >= 90:
            return "A"
        elif avg >= 75:
            return "B"
        elif avg >= 60:
            return "C"
        else:
            return "Fail"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subjects': self.subjects
        }

    @classmethod
    def from_dict(cls, data):
        return cls(name=data['name'], student_id=data['id'], subjects=data['subjects'])


class GradeManager:
    def __init__(self):
        self.students = []

    def add_student(self, name, student_id, subjects):
        if self.find_student(student_id):
            raise ValueError("Student ID already exists")
        student = Student(name, student_id)
        for subject, score in subjects.items():
            student.add_subject(subject, score)
        self.students.append(student)
        return student.id

    def update_scores(self, student_id, subject, score):
        student = self.find_student(student_id)
        if student:
            student.add_subject(subject, score)
            return True
        return False

    def view_report(self, student_id):
        student = self.find_student(student_id)
        if student:
            report = f"Report for {student.name} (ID: {student.id})\n"
            for subject, score in student.subjects.items():
                report += f"{subject}: {score}\n"
            avg = student.calculate_average()
            grade = student.get_grade()
            report += f"Average: {avg:.2f}\nGrade: {grade}\n"
            return report
        return "Student not found."

    def delete_student(self, student_id):
        for i, student in enumerate(self.students):
            if student.id == student_id:
                del self.students[i]
                return True
        return False

    def save_to_file(self, filename='grades.json'):
        data = [student.to_dict() for student in self.students]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename='grades.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.students = [Student.from_dict(item) for item in data]
        except FileNotFoundError:
            pass

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None


def main_gui():
    gm = GradeManager()
    gm.load_from_file()

    def add_student():
        name = simpledialog.askstring("Input", "Enter student name:")
        student_id = simpledialog.askstring("Input", "Enter a unique student ID:")
        if not name or not student_id:
            return
        subjects = {}
        while True:
            subject = simpledialog.askstring("Input", "Enter subject (or type 'done'):")
            if subject == 'done':
                break
            try:
                score = float(simpledialog.askstring("Input", f"Enter score for {subject}:"))
                subjects[subject] = score
            except:
                messagebox.showerror("Error", "Invalid score")
        try:
            sid = gm.add_student(name, student_id, subjects)
            messagebox.showinfo("Success", f"Student added with ID: {sid}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_score():
        sid = simpledialog.askstring("Input", "Enter student ID:")
        subject = simpledialog.askstring("Input", "Enter subject to update:")
        try:
            score = float(simpledialog.askstring("Input", "Enter new score:"))
            if gm.update_scores(sid, subject, score):
                messagebox.showinfo("Success", "Score updated.")
            else:
                messagebox.showerror("Error", "Student not found.")
        except:
            messagebox.showerror("Error", "Invalid input.")

    def view_report():
        sid = simpledialog.askstring("Input", "Enter student ID:")
        report = gm.view_report(sid)
        messagebox.showinfo("Report", report)

    def delete_student():
        sid = simpledialog.askstring("Input", "Enter student ID:")
        if gm.delete_student(sid):
            messagebox.showinfo("Success", "Student deleted.")
        else:
            messagebox.showerror("Error", "Student not found.")

    def save_data():
        gm.save_to_file()
        messagebox.showinfo("Saved", "Data saved to grades.json")

    def load_data():
        gm.load_from_file()
        messagebox.showinfo("Loaded", "Data loaded from grades.json")

    root = tk.Tk()
    root.title("Student Report Card Manager")
    root.geometry("400x300")

    tk.Button(root, text="Add Student", width=25, command=add_student).pack(pady=5)
    tk.Button(root, text="Update Scores", width=25, command=update_score).pack(pady=5)
    tk.Button(root, text="View Report", width=25, command=view_report).pack(pady=5)
    tk.Button(root, text="Delete Student", width=25, command=delete_student).pack(pady=5)
    tk.Button(root, text="Save Data", width=25, command=save_data).pack(pady=5)
    tk.Button(root, text="Load Data", width=25, command=load_data).pack(pady=5)
    tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
