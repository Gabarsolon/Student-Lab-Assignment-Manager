from src.domain.student import Student
from random import randint
from src.domain.undo_redo import *

STUDENT_NAMES = ['Turcu', 'Oprea', 'Moldovan', 'Pop', 'Rus', 'Albu', 'Petrovan', 'Jordan', 'Tapoi', 'Mircea',
                 'Andrei', 'Bargaoanu', 'Vidican', 'Forogau', 'Campan', 'Micu', 'Muresan', 'Grigore', 'Iancu', 'Hagi']


class StudentService:
    def __init__(self, student_repository, undo_redo_service):
        """
        Initialize the student service
        :param student_repository: a student repository object
        """
        self._student_repository = student_repository
        self._undo_redo_service = undo_redo_service

    def generate_students(self):
        """
        Add 10 randomly generated students to the repository
        """
        # start the student id's from 3000
        id_counter = 3000
        for current_index in range(10):
            student_id = id_counter
            student_name = STUDENT_NAMES[randint(0, 19)]
            student_group = randint(911, 917)
            self._student_repository.add_student(Student(student_id, student_name, student_group))
            id_counter += 1

    def add_student(self, student_id, name, group):
        """
        Add student to the student repository
        :param student_id: integer, which represents the student's id
        :param name: string, which represents the student's name
        :param group: integer, which indicates the group where the student belongs to
        """
        self._student_repository.add_student(Student(student_id, name, group))
        undo_call = Call(self._student_repository.remove_student, student_id)
        redo_call = Call(self._student_repository.add_student, Student(student_id, name, group))
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))

    def remove_student(self, student_id):
        """
        Remove student from the repository
        :param student_id: a intger which indicates the id of the student object to remove
        """
        self._student_repository.remove_student(student_id)

    def update_student_name(self, student_id, new_name):
        """
        Update the name for a student from repository
        :param student_id: a integer which indicates the id of the student to update
        :param new_name: a string which will replace the actual name of the student
        """
        self.check_valid_student(student_id)
        actual_name = self._student_repository.get_student_data()[student_id].name
        undo_call = Call(self._student_repository.update_student_name, student_id, actual_name)
        redo_call = Call(self._student_repository.update_student_name, student_id, new_name)
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))
        self._student_repository.update_student_name(student_id, new_name)

    def update_student_group(self, student_id, new_group):
        """
        Update the group of a student from student repository
        :param student_id: a integer which represents the id of the student to update
        :param new_group: a integer which repesents the new group number of the student
        """
        self.check_valid_student(student_id)
        actual_group = self._student_repository.get_student_data()[student_id].group
        undo_call = Call(self._student_repository.update_student_group, student_id, actual_group)
        redo_call = Call(self._student_repository.update_student_group, student_id, new_group)
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))
        self._student_repository.update_student_group(student_id, new_group)

    def check_valid_student(self, student_id):
        """
        Check if a student is present or not in the student repository
        :param student_id: a integer which indicates the id of the student to check
        """
        self._student_repository.check_valid_student_id(student_id)

    def get_students(self):
        return self._student_repository.get_student_data()
