import unittest

from src.repository.assigment_repository import *
from src.domain.assignment import Assignment
from src.repository.student_repository import *
from src.domain.grade import Grade
from src.repository.grade_repository import *
from src.domain.student import Student
from datetime import date
from src.repository.assigment_repository import AssignmentRepository
from src.repository.grade_repository import GradeRepository
from src.repository.student_repository import StudentRepository
from src.repository.undo_redo_repository import UndoRedoRepository
from src.services.assignment_service import AssignmentService
from src.services.grade_service import GradeService
from src.services.student_service import StudentService
from src.services.undo_redo_service import UndoRedoService, UndoRedoServiceException


class assignment_tests(unittest.TestCase):
    def setUp(self) -> None:
        assignment_repository = AssignmentRepository()
        self._assignment_service = AssignmentService(assignment_repository, UndoRedoService(UndoRedoRepository()))
        self._assignment_service.generate_assignments()

    def tearDown(self) -> None:
        pass

    def test_add_assignment__valid_assignment__add_to_repository(self):
        self._assignment_service.add_assignment(302, 'some description', date(2021, 11, 15))
        self.assertEqual(self._assignment_service.get_assignments()[302],
                         Assignment(302, 'some description', date(2021, 11, 15)))

    def test_add_assignment__duplicate_assigment__raise_repository_exception(self):
        with self.assertRaises(AssignmentRepositoryException):
            self._assignment_service.add_assignment(2, 'some more description', date(2021, 11, 15))

    def test_add_assignment__invalid_assignment_id__raise_value_error(self):
        with self.assertRaises(ValueError):
            self._assignment_service.add_assignment(-5, "some description", date(2021, 11, 15))

    def test_remove_assignment__valid_assignment__remove_from_repository(self):
        self._assignment_service.remove_assignment(5)
        with self.assertRaises(KeyError):
            self._assignment_service.get_assignments()[5]

    def test_remove_assignment__assignment_non_existent__raise_repository_exception(self):
        with self.assertRaises(AssignmentRepositoryException):
            self._assignment_service.remove_assignment(30)

    def test_update_assignment_description__valid_assignment__update_succesfully(self):
        self._assignment_service.update_assignment_description(2, 'sum thang')
        self.assertEqual(self._assignment_service.get_assignments()[2].description, "sum thang")

    def test_update_assignment_description__asignment_non_existent__raise_repository_exception(self):
        with self.assertRaises(AssignmentRepositoryException):
            self._assignment_service.update_assignment_description(3000, 'jeah boah')

    def test_update_assignment_deadline__valid_assignment__update_successfully(self):
        self._assignment_service.update_assignment_deadline(2, date.fromisoformat('2021-07-21'))
        self.assertEqual(self._assignment_service.get_assignments()[2].deadline, date(2021, 7, 21))

    def test_update_assignment_deadline__assignment_non_existent__raise_repository_exception(self):
        with self.assertRaises(AssignmentRepositoryException):
            self._assignment_service.update_assignment_deadline(3000, date(2021, 7, 30))

    def test_check_valid_assignment_id__assignment_not_present_in_repository__raise_repository_exception(self):
        with self.assertRaises(AssignmentRepositoryException):
            self._assignment_service.check_valid_assignment(15)

    def test_check_valid_assignment_id__assignment_present_in_repository__raise_repository_exception(self):
        with self.assertRaises(AssignmentRepositoryException):
            self._assignment_service.check_valid_assignment(15)


class student_tests(unittest.TestCase):

    def setUp(self) -> None:
        student_repository = StudentRepository()
        self._student_service = StudentService(student_repository, UndoRedoService(UndoRedoRepository()))
        self._student_service.generate_students()

    def tearDown(self) -> None:
        pass

    def test_add_student__valid_student__add_to_repository(self):
        self._student_service.add_student(13, 'Gigel', 912)
        self.assertEqual(self._student_service.get_students()[13], Student(13, 'Gigel', 912))

    def test_add_student__duplicate_student__raise_repository_exception(self):
        with self.assertRaises(StudentRepositoryException):
            self._student_service.add_student(3002, 'Someone', 913)

    def test_add_student__invalid_student_id__raise_value_error(self):
        with self.assertRaises(ValueError):
            self._student_service.add_student(-1000, "Someone", 914)

    def test_add_student__invalid_student_group__raise_value_error(self):
        with self.assertRaises(ValueError):
            self._student_service.add_student(3002, "someone", 918)

    def test_remove_student__valid_student__remove_from_repository(self):
        self._student_service.remove_student(3001)
        with self.assertRaises(KeyError):
            self._student_service.get_students()[3001]

    def test_remove_student__student_non_existent__raise_repository_exception(self):
        with self.assertRaises(StudentRepositoryException):
            self._student_service.remove_student(300)

    def test_update_student_name__valid_student__update_successfully(self):
        self._student_service.update_student_name(3002, 'Ionel')
        self.assertEqual(self._student_service.get_students()[3002].name, 'Ionel')

    def test_update_student_name__invalid_student_name__raise_value_error(self):
        with self.assertRaises(ValueError):
            self._student_service.update_student_name(3002, 'G1G3L')

    def test_update_student_name__non_existent_student__raise_repository_exception(self):
        with self.assertRaises(StudentRepositoryException):
            self._student_service.update_student_name(2000, 'Gigel')

    def test_update_student_group__valid_student__update_successfully(self):
        self._student_service.update_student_group(3002, 914)
        self.assertEqual(self._student_service.get_students()[3002].group, 914)

    def test_update_student_group__non_existent_student__raise_repository_exception(self):
        with self.assertRaises(StudentRepositoryException):
            self._student_service.update_student_group(2000, 916)


class grade_tests(unittest.TestCase):
    def setUp(self) -> None:
        student_repository = StudentRepository()
        assignment_repository = AssignmentRepository()
        grade_repository = GradeRepository()
        self._student_service = StudentService(student_repository, UndoRedoService(UndoRedoRepository()))
        self._assignment_service = AssignmentService(assignment_repository, UndoRedoService(UndoRedoRepository()))
        self._assignment_service.generate_assignments()
        self._grade_service = GradeService(grade_repository, student_repository, assignment_repository,
                                           UndoRedoService(UndoRedoRepository()))

    def test_add_grade__valid_grade__add_grade_to_grade_repository(self):
        self._grade_service.add_grade(1, 3002)
        self.assertEqual(self._grade_service.get_grades()[1, 3002], Grade(1, 3002))

    def test_add_grade__invalid_grade__raise_value_error(self):
        with self.assertRaises(ValueError):
            self._grade_service.add_grade(1, 3002, 'jeah')

    def test_add_grade__grade_already_present_in_repository__raise_repository_exception(self):
        self._grade_service.add_grade(1, 3002)
        with self.assertRaises(GradeRepositoryException):
            self._grade_service.add_grade(1, 3002)

    def test_give_assignment_to_a_group_of_students__valid_assignment_and_group__add_grades_to_repository(self):
        self._student_service.add_student(3006, 'yeah', 917)
        self._student_service.add_student(3005, 'meah', 917)
        self._student_service.add_student(3004, 'duh', 914)
        self._student_service.add_student(3003, 'mneah', 917)
        self._grade_service.give_assignment_to_a_group_of_students(3, 917)
        self.assertEqual(len(self._grade_service.get_grades()), 3)

    def test_remove_grades__valid_entity_id_and_id_position__remove_from_repository(self):
        self._student_service.add_student(3006, 'yeah', 917)
        self._student_service.add_student(3005, 'meah', 913)
        self._student_service.add_student(3004, 'duh', 914)
        self._student_service.add_student(3003, 'mneah', 917)
        self._grade_service.give_assignment_to_a_group_of_students(3, 917)
        self._grade_service.remove_grades(3006, 1)
        self.assertEqual(len(self._grade_service.get_grades()), 1)

    def test_grade_student_from_ungraded_assignments_list__valid_position_in_list__grade_student_successfully(self):
        self._student_service.add_student(3004, 'Batista', 914)
        self._student_service.add_student(3005, 'BatistaMista', 914)
        self._grade_service.give_assignment_to_a_group_of_students(3, 914)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 8)
        self.assertEqual(self._grade_service.get_graded_assignments()[0].grade_value, 8)

    def test_grade_student_from_ungraded_assignments_list__valid_position_in_list__grade_student_successfully(self):
        self._student_service.add_student(3004, 'Batista', 914)
        self._student_service.add_student(3005, 'BatistaMista', 914)
        self._grade_service.give_assignment_to_a_group_of_students(3, 914)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 8)
        self.assertEqual(self._grade_service.get_graded_assignments()[0].grade_value, 8)

    def test_grade_student_from_ungraded_assignments_list__invalid_position_in_list__raise_index_error(self):
        self._student_service.add_student(3004, 'Batista', 914)
        self._student_service.add_student(3005, 'BatistaMista', 914)
        self._grade_service.give_assignment_to_a_group_of_students(3, 914)
        with self.assertRaises(IndexError):
            self._grade_service.grade_student_from_ungraded_assignments_list(2, 8)

    def test_get_list_of_sorted_students_descending_by_grade_value_for_a_given_assignment__valid_assignment_id__return_the_sorted_list(
            self):
        self._student_service.add_student(3004, 'jeah', 914)
        self._student_service.add_student(3005, 'yeah', 914)
        self._student_service.add_student(3006, 'mneah', 914)
        self._grade_service.give_assignment_to_a_group_of_students(3, 914)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 7)
        self._grade_service.grade_student_from_ungraded_assignments_list(1, 8)
        self.assertEqual(
            self._grade_service.get_list_of_sorted_students_descending_by_grade_value_for_a_given_assignment(3),
            [Grade(3, 3006, 8), Grade(3, 3004, 7), Grade(3, 3005, None)])

    def test_get_list_of_sorted_students_descending_by_grade_value_for_a_given_assignment__invalid_assignment_id__raise_repository_exception(
            self):
        self._student_service.add_student(3004, 'jeah', 914)
        self._grade_service.give_assignment_to_a_group_of_students(3, 914)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 7)
        with self.assertRaises(GradeRepositoryException):
            self._grade_service.get_list_of_sorted_students_descending_by_grade_value_for_a_given_assignment(2)

    def test_get_list_of_all_students_who_are_late_in_handing_in_at_least_one_assignment__valid_call_of_the_function__return_a_list_of_students(
            self):
        self._assignment_service.update_assignment_deadline(2, date(2021, 9, 15))
        self._assignment_service.update_assignment_deadline(3, date(2099, 12, 30))
        self._student_service.add_student(3001, "cnv candva", 912)
        self._student_service.add_student(3002, "era cineva", 912)
        self._student_service.add_student(3003, "undeva ceva", 913)
        self._student_service.add_student(3004, "mno bn", 913)
        self._grade_service.give_assignment_to_a_group_of_students(2, 912)
        self._grade_service.give_assignment_to_a_group_of_students(3, 913)
        self.assertEqual(
            self._grade_service.get_list_of_all_students_who_are_late_in_handing_in_at_least_one_assignment(),
            [Student(3001, "cnv candva", 912), Student(3002, "era cineva", 912)])

    def test_get_list_of_students_sorted_descending_by_average_grade_received_for_all_assignments__valid_call_of_function__return_a_dictionary(
            self):
        self._student_service.add_student(3001, "cnv candva", 912)
        self._student_service.add_student(3002, "era cineva", 912)
        self._student_service.add_student(3003, "undeva ceva", 912)
        self._grade_service.give_assignment_to_a_group_of_students(2, 912)
        self._grade_service.give_assignment_to_a_group_of_students(3, 912)
        self._grade_service.give_assignment_to_a_group_of_students(4, 912)

        self._grade_service.grade_student_from_ungraded_assignments_list(0, 7)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 3)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 5)

        self._grade_service.grade_student_from_ungraded_assignments_list(0, 2)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 8)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 6)

        self._grade_service.grade_student_from_ungraded_assignments_list(0, 9)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 10)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 4)
        self.assertEqual(
            self._grade_service.get_list_of_students_sorted_descending_by_average_grade_received_for_all_assignments(),
            [(3002, 7.0), (3001, 6.0), (3003, 5.0)])

    def test_gemerate_grades__valid_method_call__add_grades_to_repository(self):
        self._grade_service.generate_grades()
        self.assertNotEqual(len(self._grade_service.get_grades()), 0)


class test_undo_redo_service(unittest.TestCase):
    def setUp(self) -> None:
        undo_redo_repository = UndoRedoRepository()
        student_repository = StudentRepository()
        assignment_repository = AssignmentRepository()
        grade_repository = GradeRepository()
        self._undo_redo_service = UndoRedoService(undo_redo_repository)
        self._assignment_service = AssignmentService(assignment_repository, self._undo_redo_service)
        self._student_service = StudentService(student_repository, self._undo_redo_service)
        self._grade_service = GradeService(grade_repository, student_repository, assignment_repository,
                                           self._undo_redo_service)

    def tearDown(self) -> None:
        pass

    def test_undo_add_assignment__valid_undo__undo_succesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._undo_redo_service.undo()
        self.assertEqual(len(self._assignment_service.get_assignments()), 0)

    def test_redo_add_assignment__valid_redo__redo_succesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len(self._assignment_service.get_assignments()), 1)

    def test_undo_remove_assignment__valid_undo__undo_succesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.remove_grades(2, 0)
        self._assignment_service.remove_assignment(2)
        self._undo_redo_service.undo()
        self.assertEqual(len(self._assignment_service.get_assignments()), 1)

    def test_redo_remove_assignment__valid_redo__redo_succesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.remove_grades(2, 0)
        self._assignment_service.remove_assignment(2)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len(self._assignment_service.get_assignments()), 0)

    def test_undo_update_assignment_description__valid_undo__undo_succesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._assignment_service.update_assignment_description(2, "something else")
        self._undo_redo_service.undo()
        self.assertEqual(self._assignment_service.get_assignments()[2].description, "something")

    def test_redo_update_assignment_description__valid_redo__redo_succsesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._assignment_service.update_assignment_description(2, "something else")
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(self._assignment_service.get_assignments()[2].description, "something else")

    def test_undo_update_assignment_deadline__valid_undo__undo_succesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._assignment_service.update_assignment_deadline(2, date(2020, 10, 5))
        self._undo_redo_service.undo()
        self.assertEqual(self._assignment_service.get_assignments()[2].deadline, date(2020, 10, 10))

    def test_redo_update_assignment_deadline__valid_redo__redo_succesfully(self):
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._assignment_service.update_assignment_deadline(2, date(2020, 10, 5))
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(self._assignment_service.get_assignments()[2].deadline, date(2020, 10, 5))

    def test_undo_add_student__valid_undo__undo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._undo_redo_service.undo()
        self.assertEqual(len(self._student_service.get_students()), 0)

    def test_redo_add_student__valid_redo__redo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len(self._student_service.get_students()), 1)

    def test_undo_remove_student__valid_undo__undo_succesfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._grade_service.remove_grades(3001, 1)
        self._student_service.remove_student(3001)
        self._undo_redo_service.undo()
        self.assertEqual(len(self._student_service.get_students()), 1)

    def test_redo_remove_student__valid_redo__redo_succesfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._grade_service.remove_grades(3001, 1)
        self._student_service.remove_student(3001)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len(self._student_service.get_students()), 0)

    def test_undo_update_student_name__valid_undo__undo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.update_student_name(3001, "someone else")
        self._undo_redo_service.undo()
        self.assertEqual(self._student_service.get_students()[3001].name, "someone")

    def test_redo_update_student_name__valid_redo__successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.update_student_name(3001, "someone else")
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(self._student_service.get_students()[3001].name, "someone else")

    def test_undo_update_student_group__valid_undo__undo_succesfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.update_student_group(3001, 915)
        self._undo_redo_service.undo()
        self.assertEqual(self._student_service.get_students()[3001].group, 917)

    def test_redo_update_student_group__valid_redo__redo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.update_student_group(3001, 915)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(self._student_service.get_students()[3001].group, 915)

    def test_undo_add_grade__valid_undo__undo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3001)
        self._undo_redo_service.undo()
        self.assertEqual(len (self._grade_service.get_grades()), 0)

    def test_redo_add_grade__valid_redo__redo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3001)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len (self._grade_service.get_grades()), 1)

    def test_undo_give_assignment_to_a_group_of_students__valid_undo__undo_succesfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.add_student(3002, "someone else", 917)
        self._student_service.add_student(3003, "just someone", 916)
        self._student_service.add_student(3004, "just somebody", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3003)
        self._grade_service.give_assignment_to_a_group_of_students(2, 917)
        self._undo_redo_service.undo()
        self.assertEqual(len (self._grade_service.get_grades()), 1)

    def test_redo_give_assignment_to_a_group_of_students__valid_redo__redo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.add_student(3002, "someone else", 917)
        self._student_service.add_student(3003, "just someone", 916)
        self._student_service.add_student(3004, "just somebody", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3003)
        self._grade_service.give_assignment_to_a_group_of_students(2, 917)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len (self._grade_service.get_grades()), 4)

    def test_undo_remove_grades_for_a_student__valid_undo__undo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.add_student(3002, "someone else", 917)
        self._student_service.add_student(3003, "just someone", 916)
        self._student_service.add_student(3004, "just somebody", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3003)
        self._grade_service.give_assignment_to_a_group_of_students(2, 917)
        self._grade_service.remove_grades(3002, 1)
        self._student_service.remove_student(3002)
        self._undo_redo_service.undo()
        self.assertEqual(len (self._grade_service.get_grades()), 4)

    def test_redo_remove_grades_for_a_student__valid_redo__redo_succesfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.add_student(3002, "someone else", 917)
        self._student_service.add_student(3003, "just someone", 916)
        self._student_service.add_student(3004, "just somebody", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3003)
        self._grade_service.give_assignment_to_a_group_of_students(2, 917)
        self._grade_service.remove_grades(3002, 1)
        self._student_service.remove_student(3002)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len (self._grade_service.get_grades()), 3)

    def test_undo_remove_grades_for_an_assignment__valid_undo__undo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.add_student(3002, "someone else", 917)
        self._student_service.add_student(3003, "just someone", 916)
        self._student_service.add_student(3004, "just somebody", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._assignment_service.add_assignment(3, "something else", date(2021, 10, 10))
        self._grade_service.add_grade(3, 3003)
        self._grade_service.give_assignment_to_a_group_of_students(2, 917)
        self._grade_service.remove_grades(2, 0)
        self._assignment_service.remove_assignment(2)
        self._undo_redo_service.undo()
        self.assertEqual(len (self._grade_service.get_grades()), 4)

    def test_redo_remove_grades_for_an_assignment__valid_redo__redo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._student_service.add_student(3002, "someone else", 917)
        self._student_service.add_student(3003, "just someone", 916)
        self._student_service.add_student(3004, "just somebody", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._assignment_service.add_assignment(3, "something else", date(2021, 10, 10))
        self._grade_service.add_grade(3, 3003)
        self._grade_service.give_assignment_to_a_group_of_students(2, 917)
        self._grade_service.remove_grades(2, 0)
        self._assignment_service.remove_assignment(2)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(len (self._grade_service.get_grades()), 1)

    def test_undo_grade_student_from_ungraded_assignments_list__valid_undo__undo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3001)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 8)
        self._undo_redo_service.undo()
        self.assertEqual(self._grade_service.get_grades()[2,3001].grade_value, None)

    def test_redo_grade_student_from_ungraded_assignments_list__valid_redo__redo_successfully(self):
        self._student_service.add_student(3001, "someone", 917)
        self._assignment_service.add_assignment(2, "something", date(2020, 10, 10))
        self._grade_service.add_grade(2, 3001)
        self._grade_service.grade_student_from_ungraded_assignments_list(0, 8)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        self.assertEqual(self._grade_service.get_grades()[2,3001].grade_value, 8)

    def test_undo__invalid_undo__raise_service_exception(self):
        self._student_service.add_student(3001, "someone", 917)
        self._undo_redo_service.undo()
        with self.assertRaises(UndoRedoServiceException):
            self._undo_redo_service.undo()

    def test_redo__invalid_redo__raise_service_exception(self):
        self._student_service.add_student(3001, "someone", 917)
        self._undo_redo_service.undo()
        self._undo_redo_service.redo()
        with self.assertRaises(UndoRedoServiceException):
            self._undo_redo_service.redo()
