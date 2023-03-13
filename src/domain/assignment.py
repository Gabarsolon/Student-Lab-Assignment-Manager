class Assignment:
    def __init__(self, assignment_id, description, deadline):
        """
        Initialize the assignment object
        :param assignment_id: integer, which represents the assignment's id
        :param description: string, which represents the description of the assignment
        :param deadline: datetime object, which represents the date of the deadline
        """
        self._check_assignment_id(assignment_id)
        self._assignment_id = assignment_id
        self._description = description
        self._deadline = deadline

    @property
    def assigment_id(self):
        return self._assignment_id

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, deadline):
        self._deadline = deadline

    @staticmethod
    def _check_assignment_id(assignment_id):
        if assignment_id < 0:
            raise ValueError("Assignment id must be >= 0")

    def __str__(self):
        """
        Modify the str function for assignment class
        :return: a string of form : "assignment_id: description deadline"
        """
        return str(self._assignment_id) + ": " + self._description + "  " + str(self._deadline)

    def __eq__(self, other):
        """
        Check if 2 assignments are equal
        :param other: assigment object to compare
        :return: True, if they are equal, False otherwise
        """
        return str(self) == str(other)
