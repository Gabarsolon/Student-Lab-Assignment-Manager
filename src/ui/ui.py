from src.repository.student_repository import StudentRepositoryException
from src.repository.assigment_repository import AssignmentRepositoryException
from src.repository.grade_repository import GradeRepositoryException
from src.services.undo_redo_service import UndoRedoServiceException

from datetime import date


class UI:
    def __init__(self, student_service, assignment_service, grade_service, undo_redo_service):
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service
        self._undo_redo_service = undo_redo_service

    @staticmethod
    def print_menu():
        print("1. Manage students")
        print("2. Manage assignments")
        print("3. Create statistics")
        print("4. Undo the last program modification")
        print("5. Redo the recent program modification that you undo")
        print("6. Exit")
        print()

    @staticmethod
    def print_student_menu():
        print("1. Add student")
        print("2. Remove student")
        print("3. Update student name")
        print("4. Update student group")
        print("5. List students")
        print()

    @staticmethod
    def print_assignment_menu():
        print("1. Add assignment")
        print("2. Remove assignment")
        print("3. Update assignment description")
        print("4. Update assignment deadline")
        print("5. Give assignment to a student")
        print("6. Give assignment to a group of students")
        print("7. Grade student for a given assignment")
        print("8. List assignments")
        print("9. List given assignments")
        print()

    @staticmethod
    def print_statistics_menu():
        print("1. Display all students who received a given assignment, ordered descending by grade")
        print("2. Display all students who are late in handing in at least one assignment")
        print("3. Display Students with the best school situation")
        print()

    def print_students(self):
        for student in self._student_service.get_students():
            print(student)

    def print_assignments(self):
        for assignment in self._assignment_service.get_assignments():
            print(assignment)

    def print_grades(self):
        for grade in self._grade_service.get_grades():
            print(grade)

    def print_ungraded_assignments(self):
        ungraded_assignments_list = self._grade_service.get_ungraded_assignments()
        for current_index in range(len(ungraded_assignments_list)):
            print(str(current_index + 1) + " --> " + str(ungraded_assignments_list[current_index]))

    def print_sorted_students_descending_by_grade_value_for_a_given_assignment(self, assignment_id):
        for grade in self._grade_service.get_list_of_sorted_students_descending_by_grade_value_for_a_given_assignment(
                assignment_id):
            print(str(self._student_service.get_students()[grade.student_id]) + " Grade: " + str(grade.grade_value))

    def print_students_who_are_late_in_handing_in_at_least_one_assignment(self):
        for student in self._grade_service.get_list_of_all_students_who_are_late_in_handing_in_at_least_one_assignment():
            print(student)

    def print_students_with_the_best_school_situation(self):
        good_grade = 5
        students_list = self._grade_service.get_list_of_students_sorted_descending_by_average_grade_received_for_all_assignments()
        for student_id in students_list:
            if students_list[student_id] >= good_grade:
                print(str(self._student_service.get_students()[student_id]) + " Average grade: " + str(
                    students_list[student_id]))

    @staticmethod
    def input_student_id():
        return int(input("Enter student id: "))

    @staticmethod
    def input_student_name():
        return input("Enter student name: ")

    @staticmethod
    def input_group_number():
        return int(input("Enter group number: "))

    @staticmethod
    def input_assignment_id():
        return int(input("Enter assignment id: "))

    @staticmethod
    def input_assignment_description():
        return input("Enter assignment description: ")

    @staticmethod
    def input_assignment_deadline():
        return date.fromisoformat(input("Enter assignment deadline(YYYY-MM-DD): "))

    @staticmethod
    def input_grade_value():
        return int(input("Enter grade value: "))

    def start(self):
        while True:
            try:
                self.print_menu()
                user_option = int(input("Input a option: "))
                if user_option == 1:
                    self.print_student_menu()
                    user_option = int(input("Input a option: "))
                    if user_option == 1:
                        student_id = self.input_student_id()
                        student_name = self.input_student_name()
                        student_group = self.input_group_number()
                        self._student_service.add_student(student_id, student_name, student_group)
                        print("Student added successfully")
                    elif user_option == 2:
                        student_id = self.input_student_id()
                        self._student_service.check_valid_student(student_id)
                        id_position = 1
                        self._grade_service.remove_grades(student_id, id_position)
                        self._student_service.remove_student(student_id)
                        print("Student removed successfully")
                    elif user_option == 3:
                        student_id = self.input_student_id()
                        student_name = self.input_student_name()
                        self._student_service.update_student_name(student_id, student_name)
                        print("Student name updated successfully")
                    elif user_option == 4:
                        student_id = self.input_student_id()
                        student_group = self.input_group_number()
                        self._student_service.update_student_group(student_id, student_group)
                        print("Student group number updated successfully")
                    elif user_option == 5:
                        self.print_students()
                    else:
                        raise ValueError("Invalid option")
                elif user_option == 2:
                    self.print_assignment_menu()
                    user_option = int(input("Input a option: "))
                    if user_option == 1:
                        assignment_id = self.input_assignment_id()
                        assignment_description = self.input_assignment_description()
                        assignment_deadline = self.input_assignment_deadline()
                        self._assignment_service.add_assignment(assignment_id, assignment_description,
                                                                assignment_deadline)
                        print("Assignment added successfully")
                    elif user_option == 2:
                        assignment_id = self.input_assignment_id()
                        self._assignment_service.check_valid_assignment(assignment_id)
                        id_position = 0
                        self._grade_service.remove_grades(assignment_id, id_position)
                        self._assignment_service.remove_assignment(assignment_id)
                        print("Assignment removed successfully")
                    elif user_option == 3:
                        assignment_id = self.input_assignment_id()
                        assignment_description = self.input_assignment_description()
                        self._assignment_service.update_assignment_description(assignment_id, assignment_description)
                        print("Assignment description updated successfully")
                    elif user_option == 4:
                        assignment_id = self.input_assignment_id()
                        assignment_deadline = self.input_assignment_deadline()
                        self._assignment_service.update_assignment_deadline(assignment_id, assignment_deadline)
                        print("Assignment deadline updated successfully")
                    elif user_option == 5:
                        assignment_id = self.input_assignment_id()
                        student_id = self.input_student_id()
                        self._assignment_service.check_valid_assignment(assignment_id)
                        self._student_service.check_valid_student(student_id)
                        self._grade_service.add_grade(assignment_id, student_id)
                        print("Assignment given successfully")
                    elif user_option == 6:
                        assignment_id = self.input_assignment_id()
                        student_group = self.input_group_number()
                        self._assignment_service.check_valid_assignment(assignment_id)
                        self._grade_service.give_assignment_to_a_group_of_students(assignment_id, student_group)
                        print("Assignments given successfully")
                    elif user_option == 7:
                        self.print_ungraded_assignments()
                        assignment_to_grade = int(input("Select a ungraded assignment to grade:")) - 1
                        grade_value = self.input_grade_value()
                        self._grade_service.grade_student_from_ungraded_assignments_list(assignment_to_grade,
                                                                                         grade_value)
                        print("Assignment graded successfully")
                    elif user_option == 8:
                        self.print_assignments()
                    elif user_option == 9:
                        self.print_grades()
                    else:
                        raise ValueError("Invalid option")
                elif user_option == 3:
                    self.print_statistics_menu()
                    user_option = int(input("Input a option: "))
                    if user_option == 1:
                        assignment_id = self.input_assignment_id()
                        self.print_sorted_students_descending_by_grade_value_for_a_given_assignment(assignment_id)
                    elif user_option == 2:
                        self.print_students_who_are_late_in_handing_in_at_least_one_assignment()
                    elif user_option == 3:
                        self.print_students_with_the_best_school_situation()
                elif user_option == 4:
                    self._undo_redo_service.undo()
                    print("Undo successfully")
                elif user_option == 5:
                    self._undo_redo_service.redo()
                    print("Redo successfully")
                elif user_option == 6:
                    return
                else:
                    raise ValueError("Invalid option")
            except ValueError as error_message:
                print(error_message)
            except AttributeError as error_message:
                print(error_message)
            except TypeError as error_message:
                print(error_message)
            except IndexError as error_message:
                print(error_message)
            except KeyError as error_message:
                print(error_message)
            except AssignmentRepositoryException as error_message:
                print(error_message)
            except StudentRepositoryException as error_message:
                print(error_message)
            except GradeRepositoryException as error_message:
                print(error_message)
            except UndoRedoServiceException as error_message:
                print(error_message)
            print()
