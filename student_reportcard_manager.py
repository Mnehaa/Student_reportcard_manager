import json
import streamlit as st
from uuid import uuid4

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


def main():
    st.title("Student Report Card Manager")
    if "gm" not in st.session_state:
        st.session_state.gm = GradeManager()
        st.session_state.gm.load_from_file()

    gm = st.session_state.gm

    menu = ["Add Student", "Update Scores", "View Report", "Delete Student", "Save Data", "Load Data"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Student":
        if "subjects" not in st.session_state:
            st.session_state.subjects = {}

        st.subheader("Add New Student")
        name = st.text_input("Student Name")
        student_id = st.text_input("Student ID")

        subject = st.text_input("Subject")
        score = st.number_input("Score", min_value=0.0, max_value=100.0)

        if st.button("Add Subject"):
            if subject:
                st.session_state.subjects[subject] = score
                st.success(f"Added {subject} with score {score}")
            else:
                st.error("Subject cannot be empty")

        if st.button("Add Student"):
            try:
                gm.add_student(name, student_id, st.session_state.subjects)
                st.success("Student added successfully")
                st.session_state.subjects = {}
            except ValueError as e:
                st.error(str(e))

        if st.session_state.subjects:
            st.write("Subjects added so far:")
            st.write(st.session_state.subjects)

    elif choice == "Update Scores":
        st.subheader("Update Scores")
        sid = st.text_input("Student ID")
        subject = st.text_input("Subject to Update")
        score = st.number_input("New Score", min_value=0.0, max_value=100.0)
        if st.button("Update Score"):
            if gm.update_scores(sid, subject, score):
                st.success("Score updated successfully")
            else:
                st.error("Student not found")

    elif choice == "View Report":
        st.subheader("View Student Report")
        sid = st.text_input("Student ID")
        if st.button("Get Report"):
            report = gm.view_report(sid)
            st.text(report)

    elif choice == "Delete Student":
        st.subheader("Delete Student")
        sid = st.text_input("Student ID")
        if st.button("Delete"):
            if gm.delete_student(sid):
                st.success("Student deleted successfully")
            else:
                st.error("Student not found")

    elif choice == "Save Data":
        gm.save_to_file()
        st.success("Data saved to grades.json")

    elif choice == "Load Data":
        gm.load_from_file()
        st.success("Data loaded from grades.json")

if __name__ == '__main__':
    main()
