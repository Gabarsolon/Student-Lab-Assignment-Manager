class Student:
    def __init__(self, student_id, name, group):
        """
        Initialize the student object
        :param student_id: integer, which represents the student's id
        :param name: string, which represents the student's name
        :param group: integer, which indicates the group where the student belongs to
        """
        self._check_student_id(student_id)
        self._check_name(name)
        self._check_group(group)
        self._student_id = student_id
        self._name = name
        self._group = group

    @property
    def student_id(self):
        return self._student_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._check_name(name)
        self._name = name

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._check_group(group)
        self._group = group

    @staticmethod
    def _check_name(name):
        if any(character.isdigit() for character in name):
            raise ValueError("Invalid student name")

    @staticmethod
    def _check_student_id(student_id):
        if student_id < 0:
            raise ValueError("Student id must be >= 0")

    @staticmethod
    def _check_group(group):
        if group not in range(911, 918):
            raise ValueError("Group number must be between 911 and 917")

    def __str__(self):
        """
        Modify the str function for student class
        :return: a string of form "student_id: name group"
        """
        return str(self._student_id) + ": " + self._name + ", Group: " + str(self._group)

    def __eq__(self, other):
        """
        Check if 2 student objects are equal
        :param other: a student object to compare
        :return: True, if they are equal, False otherwise
        """
        return str(self) == str(other)
