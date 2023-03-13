import pickle

from src.domain.student import Student
from src.repository.iter_sort_filter import Iterator


class StudentRepositoryException(Exception):
    pass


class StudentRepository():
    def __init__(self):
        """
        Initialize the student repository
        """
        self._student_data = Iterator()

    def add_student(self, student):
        """
        Add student object to student data
        :param student: a student object to add
        """
        if student.student_id in self._student_data:
            raise StudentRepositoryException("Student with id: " + str(student.student_id) + " already in repository")
        self._student_data[student.student_id] = student

    def remove_student(self, student_id):
        """
        Remove student object from student data
        :param student_id: a integer which indicates the student to remove
        """
        self.check_valid_student_id(student_id)
        del self._student_data[student_id]

    def update_student_name(self, student_id, new_name):
        """
        Update the name for a student object in repository
        :param student_id: a integer which indicates the student to update
        :param new_name: a string which will be the new student name
        """
        self.check_valid_student_id(student_id)
        self._student_data[student_id].name = new_name

    def update_student_group(self, student_id, new_group):
        """
        Update the group for a student in repository
        :param student_id: a integer which indicates the student to update
        :param new_group: a integer which represent the new student group number
        """
        self.check_valid_student_id(student_id)
        self._student_data[student_id].group = new_group

    def check_valid_student_id(self, student_id):
        """
        Check if a student is present in the student repository
        :param student_id: a integer which represents the id to check
        :except StudentRepositoryException, if the student with the specified id is not present in the student data
        """
        if student_id not in self._student_data:
            raise StudentRepositoryException("Student with id: " + str(student_id) + " not present in repository")

    def get_student_data(self):
        return self._student_data


class StudentFileTextRepository(StudentRepository):
    def __init__(self, file_name):
        """
        Initialize the text-file based student repository
        :param file_name: a string which represent the name/location of the file where the data from repository is stored
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        """
        Read students from the file and store them in students_data
        """
        file = open(self._file_name, "rt")
        for line in file.readlines():
            student_id, name, group = line.split(maxsplit = 2, sep="/")
            self.add_student(Student(int(student_id), name, int(group.rstrip())))
        file.close()

    def _save_file(self):
        """
        Write the new state of students_data to the file
        """
        file = open(self._file_name, "wt")
        for student in self._students_data.values():
            file.write((str(student.student_id)) + "/" + student.name + "/" + str(student.group) + "\n")
        file.close()

    def add_student(self, student):
        super().add_student(student)
        self._save_file()

    def remove_student(self, student_id):
        super().remove_student(student_id)
        self._save_file()

    def update_student_name(self, student_id, new_name):
        super().update_student_name(student_id, new_name)
        self._save_file()

    def update_student_group(self, student_id, new_group):
        super().update_student_group(student_id, new_group)
        self._save_file()


class StudentBinaryFileRepository(StudentRepository):
    def __init__(self, file_name):
        """
        Initialize the binary-file based students repository
        :param file_name: a string which represent the name/location of the file where the data from repository is stored
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        """
        Read students from the file and store them in students_data
        """
        file = open(self._file_name, "rb")
        self._students_data = pickle.load(file)
        file.close()

    def _save_file(self):
        """
        Write the new state of students_data to the file
        """
        file = open(self._file_name, "wb")
        pickle.dump(self._students_data, file)
        file.close()

    def add_student(self, student):
        super().add_student(student)
        self._save_file()

    def remove_student(self, student_id):
        super().remove_student(student_id)
        self._save_file()

    def update_student_name(self, student_id, new_name):
        super().update_student_name(student_id, new_name)
        self._save_file()

    def update_student_group(self, student_id, new_group):
        super().update_student_group(student_id, new_group)
        self._save_file()