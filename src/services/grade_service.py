from src.domain.grade import Grade
from src.repository.grade_repository import GradeRepositoryException
from random import randint
from datetime import date
from src.domain.undo_redo import *
from src.repository.iter_sort_filter import gnome_sort, filter_a_list


class GradeService:
    def __init__(self, grade_repository, student_repository, assignment_repository, undo_redo_service):
        """
        Initialize the grade service object
        :param grade_repository: a GradeRepository object used to manage the grades
        :param student_repository: a StudentRepository object used to get students groups
        """
        self._grade_repository = grade_repository
        self._students_repository = student_repository
        self._assignment_repository = assignment_repository
        self._undo_redo_service = undo_redo_service

    def generate_grades(self):
        """
        Add randomly generated grades to the repository
        """
        for counter in range(15):
            try:
                self._grade_repository.add_grade(Grade(randint(1, 10), randint(3000,3009), None))
            except GradeRepositoryException:
                pass
        ungraded_assignments_list = self.get_ungraded_assignments()
        for current_index in range(0, len(ungraded_assignments_list) // 2):
            self._grade_repository.grade_student_for_a_given_assignment(Grade(ungraded_assignments_list[current_index].assignment_id, ungraded_assignments_list[current_index].student_id, randint(1,10)))

    def add_grade(self, assignment_id, student_id, grade_value=None):
        """
        Add grade to the grade repository
        :param assignment_id: integer, which represents the assignment id
        :param student_id: integer, which represents the student id
        :param grade_value: integer, between 1 and 10, which represents the grade value
        """
        self._grade_repository.add_grade(Grade(assignment_id, student_id, grade_value))

        undo_call = Call(self._grade_repository.remove_a_grade, assignment_id, student_id)
        redo_call = Call(self._grade_repository.add_grade, Grade(assignment_id, student_id, grade_value))
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))

    def give_assignment_to_a_group_of_students(self, assignment_id, group):
        """
        Give an asssignment to a group of students by adding them in the grade repository
        :param assignment_id: a integer which indicate the id of the assignment to give
        :param group: a integer which indicates the group which will get the assignment
        """
        operation_list = []
        for student in self._students_repository.get_student_data():
            if student.group == group:
                try:
                    self._grade_repository.add_grade(Grade(assignment_id, student.student_id))
                    undo_call = Call(self._grade_repository.remove_a_grade, assignment_id, student.student_id)
                    redo_call = Call(self._grade_repository.add_grade, Grade(assignment_id, student.student_id, None))
                    operation_list.append(Operation(undo_call, redo_call))
                except GradeRepositoryException:
                    # if there is a student in the group which already have the assignment, we continue to search for
                    # other students from the group
                    pass
        if len(operation_list)!=0:
            self._undo_redo_service.record_operation(ComplexOperation(operation_list))

    def remove_grades(self, entity_id, id_position):
        """
        Remove grades from the grades repository ( used when removing an student or an assignment
        from the others repository)
        :param entity_id: an integer, which can be the assigment id or the student id
        :param id_position: an integer, which can be 0 or 1 ( postiton of assignment_id or student_id in grade object)
        """
        operations_list = []
        if id_position == 1:
            undo_call = Call(self._students_repository.add_student, self._students_repository.get_student_data()[entity_id])
            redo_call = Call(self._students_repository.remove_student, entity_id)
            operations_list.append(Operation(undo_call, redo_call))
            for grade in self._grade_repository.get_grade_data():
                    if grade.student_id == entity_id:
                        undo_call = Call(self._grade_repository.add_grade, grade)
                        redo_call = Call(self._grade_repository.remove_grades, grade.student_id, id_position)
                        operations_list.append(Operation(undo_call, redo_call))
        else:
            undo_call = Call(self._assignment_repository.add_assignment, self._assignment_repository.get_assignment_data()[entity_id])
            redo_call = Call(self._assignment_repository.remove_assignment, entity_id)
            operations_list.append(Operation(undo_call, redo_call))
            for grade in self._grade_repository.get_grade_data():
                if grade.assignment_id == entity_id:
                    undo_call = Call(self._grade_repository.add_grade, grade)
                    redo_call = Call(self._grade_repository.remove_grades, grade.assignment_id, id_position)
                    operations_list.append(Operation(undo_call, redo_call))
        self._undo_redo_service.record_operation(ComplexOperation(operations_list))
        self._grade_repository.remove_grades(entity_id, id_position)

    def grade_student_from_ungraded_assignments_list(self, position_in_ungraded_assignments_list, grade_value):
        """
        Grade a student from the list of ungraded assignments
        :param position_in_ungraded_assignments_list: a integer which indicates to the assignment that will be graded
        :param grade_value: a integer which will represent the student's grade for the selected assignment
        """
        ungraded_assignment_to_grade = self.get_ungraded_assignments()[position_in_ungraded_assignments_list]
        ungraded_assignment_to_grade.grade_value = grade_value
        self._grade_repository.grade_student_for_a_given_assignment(ungraded_assignment_to_grade)
        assignment_id = ungraded_assignment_to_grade.assignment_id
        student_id = ungraded_assignment_to_grade.student_id
        undo_call = Call(self._grade_repository.grade_student_for_a_given_assignment, Grade(assignment_id, student_id, None))
        redo_call = Call(self._grade_repository.grade_student_for_a_given_assignment, Grade(assignment_id, student_id, grade_value))
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))

    def get_ungraded_assignments(self):
        """
        Get the list of ungraded assignments
        :return: a list of grade objects, which will have the grade value None
        """
        ungraded_assignments_list = list()
        for grade in self._grade_repository.get_grade_data():
            if grade.grade_value is None:
                ungraded_assignments_list.append(grade)
        return ungraded_assignments_list

    def get_graded_assignments(self):
        """
        Get the list of graded assignments
        :return: a list of grade objects, which will have the grade value not None
        """
        graded_assignments_list = list()
        for grade in self._grade_repository.get_grade_data():
            if grade.grade_value is not None:
                graded_assignments_list.append(grade)
        return graded_assignments_list

    def get_list_of_sorted_students_descending_by_grade_value_for_a_given_assignment(self, assignment_id):
        """
        Get the list of ll students who received a given assignment, ordered descending by grade
        :param assignment_id: a integer which represent the id of the assignment
        :return: a list of grades, sorted descending by grade value
                ( the ungraded assignments will be added at the end of the list )
        """
        graded_students_list = []
        ungraded_students_list = []
        for grade in self._grade_repository.get_grade_data():
            if grade.assignment_id == assignment_id:
                if grade.grade_value is None:
                    ungraded_students_list.append(grade)
                else:
                    graded_students_list.append(grade)
        if len(graded_students_list) + len(ungraded_students_list) ==0:
            raise GradeRepositoryException("Assignment with id: " + str(assignment_id) + " isn't given to anyone")
        graded_students_list = gnome_sort(graded_students_list, lambda entity, previous_entity:previous_entity.grade_value > entity.grade_value)
        return graded_students_list + ungraded_students_list

    def get_list_of_all_students_who_are_late_in_handing_in_at_least_one_assignment(self):
        """
        Get the list of all students who are late in handing in at least one assignment.
        These are all the students who have an ungraded assignment for which the deadline has passed.
        :return: a list of ungraded assignments , for which the deadline has passed
        """
        grades_list = self.get_ungraded_assignments()
        # students_list = self._students_repository.get_student_data().copy()
        students_list = dict()
        for student in self._students_repository.get_student_data():
            students_list[student.student_id] = student
        list_of_students_who_are_late = []
        today = date.today()
        grades_list = filter_a_list(grades_list, lambda grade: self._assignment_repository.get_assignment_data()[grade.assignment_id].deadline < today)
        for grade in grades_list:
            if grade.student_id in students_list:
                list_of_students_who_are_late.append(self._students_repository.get_student_data()[grade.student_id])
                students_list.pop(grade.student_id)
        return list_of_students_who_are_late

    def get_list_of_students_sorted_descending_by_average_grade_received_for_all_assignments(self):
        """
        Get the list of students, sorted in descending order of the average grade received for all graded assignments.
        :return: a dictionary sorted by values, where the keys are the id's of the students and the values are
                the average grade received for all graded assignments
        """
        graded_assignments_list = self.get_graded_assignments()
        list_of_average_grade_received = {}
        counter_list = {}
        for grade in graded_assignments_list:
            if grade.student_id not in list_of_average_grade_received:
                counter_list[grade.student_id] = 1
                list_of_average_grade_received[grade.student_id] = grade.grade_value
            else:
                counter_list[grade.student_id] += 1
                list_of_average_grade_received[grade.student_id] += grade.grade_value
        for student_id in list_of_average_grade_received:
            list_of_average_grade_received[student_id] /= counter_list[student_id]
        students_list = []
        for student_id in list_of_average_grade_received:
            students_list.append((student_id, list_of_average_grade_received[student_id]))
        average_grade_position = 1
        return gnome_sort(students_list, lambda entity, previous_entity: entity[average_grade_position] < previous_entity[average_grade_position])

    def get_grades(self):
        return self._grade_repository.get_grade_data()
