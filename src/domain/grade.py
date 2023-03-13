class Grade:
    def __init__(self, assignment_id, student_id, grade_value=None):
        """
        Initialize the grade object
        :param assignment_id: integer, which represents the assignment id
        :param student_id: integer, which represents the student id
        :param grade_value: integer, between 1 and 10, which represents the grade value
        """
        self.check_valid_grade(grade_value)
        self._assignment_id = assignment_id
        self._student_id = student_id
        self._grade_value = grade_value

    @property
    def assignment_id(self):
        return self._assignment_id

    @property
    def student_id(self):
        return self._student_id

    @property
    def grade_value(self):
        return self._grade_value

    @grade_value.setter
    def grade_value(self, grade):
        self.check_valid_grade(grade)
        self._grade_value = grade

    @staticmethod
    def check_valid_grade(grade):
        if grade is not None:
            if grade not in range(1, 11):
                raise ValueError("Grade must be between 1 and 10")

    def __str__(self):
        """
        Modify the str for grade object
        :return: a string of form: assignment_id + student_id + grade
        """
        return "Assignment id: " + str(self._assignment_id) + " Student id: " + str(self._student_id) + \
               " Grade: " + str(self._grade_value)

    def __eq__(self, other):
        """
        Check if 2 grades are equal
        :param other: grade object to compare
        :return: True, if they are equal, False otherwise
        """
        return str(self) == str(other)
