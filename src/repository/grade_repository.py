import pickle

from src.domain.grade import Grade
from src.repository.iter_sort_filter import Iterator


class GradeRepositoryException(Exception):
    pass


class GradeRepository():
    def __init__(self):
        """
        Initialize the repository for grades
        """
        self._grade_data = Iterator()

    def add_grade(self, grade_to_add):
        """
        Add a grade object to the grade data
        :param grade_to_add: a grade object to add
        :except GradeRepositoryException, if the grade already exist in the repository
        """
        if (grade_to_add.assignment_id, grade_to_add.student_id) in self._grade_data:
            raise GradeRepositoryException("The student with id: " + str(grade_to_add.student_id) + "already has "
                                                                                                    "the "
                                                                                                    "assignment "
                                                                                                    "with id: "
                                           + str(grade_to_add.assignment_id))
        self._grade_data[grade_to_add.assignment_id, grade_to_add.student_id] = grade_to_add

    def remove_a_grade(self, assignment_id, student_id):
        """
        Remove a grade from the grade data
        :param assignment_id: a integer which represent the assignment id for the grade that will be deleted
        :param student_id: a integer which represent the student id for the grade that will be deleted
        """
        if (assignment_id, student_id) in self._grade_data:
            del self._grade_data[assignment_id, student_id]

    def remove_grades(self, entity_id, id_position):
        """
        Remove all grades for a assignment or a student
        :param entity_id: an integer, which can be the assigment id or the student id
        :param id_position: an integer, which can be 0 or 1 ( postiton of assignment_id or student_id in grade object)
        """
        list_of_grades_to_remove = []
        for grade in self._grade_data:
            if grade.assignment_id == entity_id and id_position == 0 or grade.student_id == entity_id and id_position == 1:
                list_of_grades_to_remove.append((grade.assignment_id, grade.student_id))
        for grade in list_of_grades_to_remove:
            del self._grade_data[grade]

    def grade_student_for_a_given_assignment(self, grade):
        """
        Grade student for a given assignment
        :param grade: a grade object which has a grade value different from None
        :except GradeRepositoryException, if the grade doesn't exist in the repository
        """
        # if grade.assignment_id not in self._grade_data:
        #     raise GradeRepositoryException("The assignment with id: " + str(grade.assignment_id)
        #     + " isn't given to any student")
        # elif grade.student_id not in self._grade_data[grade.assignment_id]:
        #     raise GradeRepositoryException("The student with id: " +  str(grade.student_id) + " doesn't have "
        #                                                                                              "the "
        #                                                                                              "assignment "
        #                                                                                              "with id: "
        #                                    + str(grade.assignment_id))
        self._grade_data[grade.assignment_id, grade.student_id].grade_value = grade.grade_value

    def get_grade_value(self, assignment_id, student_id):
        return self._grade_data[assignment_id, student_id].grade_value

    def get_grade_data(self):
        return self._grade_data


class GradeTextFileRepository(GradeRepository):
    def __init__(self, file_name):
        """
        Initialize the text-file based grade repository
        :param file_name: a string which represent the name/location of the file where the data from repository is stored
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        """
        Read grades from the file and store them in grade_data
        """
        file = open(self._file_name, "rt")
        for line in file.readlines():
            assignment_id, student_id, grade_value = line.split(maxsplit=2, sep="/")
            grade_value = grade_value.rstrip()
            grade_to_add = Grade(int(assignment_id), int(student_id))
            if grade_value != "None":
                grade_to_add.grade_value = int(grade_value)
            self.add_grade(grade_to_add)
        file.close()

    def _save_file(self):
        """
        Write the new state of grade_data to the file
        """
        file = open(self._file_name, "wt")
        for graded_students in self._grade_data.values():
            for grade in graded_students.values():
                file.write(str(grade.assignment_id) + "/" + str(grade.student_id) + "/" + str(grade.grade_value) + "\n")
        file.close()

    def add_grade(self, grade_to_add):
        super().add_grade(grade_to_add)
        self._save_file()

    def remove_a_grade(self, assignment_id, student_id):
        super().remove_a_grade(assignment_id,student_id)
        self._save_file()

    def remove_grades(self, entity_id, id_position):
        super().remove_grades(entity_id,id_position)
        self._save_file()

    def grade_student_for_a_given_assignment(self, grade):
        super().grade_student_for_a_given_assignment(grade)
        self._save_file()


class GradeBinaryFileRepository(GradeRepository):
    def __init__(self, file_name):
        """
        Initialize the binary-file based grade repository
        :param file_name: a string which represent the name/location of the file where the data from repository is stored
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        """
        Read grades from the file and store them in grade_data
        """
        file = open(self._file_name, "rb")
        self._grade_data = pickle.load(file)
        file.close()

    def _save_file(self):
        """
        Write the new state of grade_data to the file
        """
        file = open(self._file_name, "wb")
        pickle.dump(self._grade_data, file)
        file.close()

    def add_grade(self, grade_to_add):
        super().add_grade(grade_to_add)
        self._save_file()

    def remove_a_grade(self, assignment_id, student_id):
        super().remove_a_grade(assignment_id, student_id)
        self._save_file()

    def remove_grades(self, entity_id, id_position):
        super().remove_grades(entity_id, id_position)
        self._save_file()

    def grade_student_for_a_given_assignment(self, grade):
        super().grade_student_for_a_given_assignment(grade)
        self._save_file()