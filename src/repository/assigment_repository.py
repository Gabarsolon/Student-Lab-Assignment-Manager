import pickle

from src.domain.assignment import Assignment
from datetime import date

from src.repository.iter_sort_filter import Iterator, filter_a_list


class AssignmentRepositoryException(Exception):
    pass


class AssignmentRepository():
    def __init__(self):
        """
        Intialize the repository for assignments
        """
        self._assignment_data = Iterator()

    def add_assignment(self, assignment):
        """
        Add assignment object to assignment data
        :param assignment: an assignment object to add
        :except AssignmentRepositoryException, if there is a assignment with the same id in the assignment data
        """
        if assignment.assigment_id in self._assignment_data:
            raise AssignmentRepositoryException(
                "Assignment with id: " + str(assignment.assigment_id) + " already in repository")
        self._assignment_data[assignment.assigment_id] = assignment

    def remove_assignment(self, assignment_id):
        """
        Remove assignment object from asignment data
        :param assignment_id: an integer which indicates the assignment id
        """
        self.check_valid_assignment_id(assignment_id)
        del self._assignment_data[assignment_id]

    def update_assignment_description(self, assignment_id, new_description):
        """
        Update the description of a assignment object
        :param assignment_id: an integer which represent the id of the assignment which we want to update
        :param new_description: a string that must replace the old description of the assignment object
        """
        self.check_valid_assignment_id(assignment_id)
        self._assignment_data[assignment_id].description = new_description

    def update_assignment_deadline(self, assignment_id, new_deadline):
        """
        Update the deadline of a assignment object
        :param assignment_id: an integer which represent the id of the assignment which we want to update
        :param new_deadline: a datetime object that must replace the old date of the assignment object
        """
        self.check_valid_assignment_id(assignment_id)
        self._assignment_data[assignment_id].deadline = new_deadline

    def check_valid_assignment_id(self, assignment_id):
        """
        Check if a assignment is present in the repository
        :param assignment_id:
        :except: AssignmentRepositoryException, if the assignment is not presesnt in the assignment data
        """
        if assignment_id not in self._assignment_data:
            raise AssignmentRepositoryException(
                "Assignment with id: " + str(assignment_id) + " not present in repository")

    def get_assignment_data(self):
        return self._assignment_data

class AssignmentTextFileRepository(AssignmentRepository):
    def __init__(self, file_name):
        """
        Initialize the text-file based assignment repository
        :param file_name: a string which represent the name/location of the file where the data from repository is stored
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        """
        Read assignments from the file and store them in assignment_data
        """
        file = open(self._file_name, "rt")
        for line in file.readlines():
            id, description, deadline = line.split(maxsplit = 2, sep="/")
            self.add_assignment(Assignment(int(id), description, date.fromisoformat(deadline.rstrip())))
        file.close()

    def _save_file(self):
        """
        Write the new state of assignment_data to the file
        """
        file = open(self._file_name, "wt")
        for assignment in self._assignment_data.values():
            file.write(str(assignment.assigment_id) + "/" + assignment.description + "/" + str(assignment.deadline) + "\n")
        file.close()

    def add_assignment(self, assignment):
        super().add_assignment(assignment)
        self._save_file()

    def remove_assignment(self, assignment_id):
        super().remove_assignment(assignment_id)
        self._save_file()

    def update_assignment_description(self, assignment_id, new_description):
        super().update_assignment_description(assignment_id, new_description)
        self._save_file()

    def update_assignment_deadline(self, assignment_id, new_deadline):
        super().update_assignment_deadline(assignment_id, new_deadline)
        self._save_file()


class AssignmentBinaryFileRepository(AssignmentRepository):
    def __init__(self, file_name):
        """
        Initialize the binary-file based assignment repository
        :param file_name: a string which represent the name/location of the file where the data from repository is stored
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        """
        Read assignments from the file and store them in assignment_data
        """
        file = open(self._file_name, "rb")
        self._data = pickle.load(file)
        file.close()

    def _save_file(self):
        """
        Write the new state of assignment_data to the file
        """
        file = open(self._file_name, "wb")
        pickle.dump(self._data, file)
        file.close()

    def add_assignment(self, assignment):
        super().add_assignment(assignment)
        self._save_file()

    def remove_assignment(self, assignment_id):
        super().remove_assignment(assignment_id)
        self._save_file()

    def update_assignment_description(self, assignment_id, new_description):
        super().update_assignment_description(assignment_id, new_description)
        self._save_file()

    def update_assignment_deadline(self, assignment_id, new_deadline):
        super().update_assignment_deadline(assignment_id, new_deadline)
        self._save_file()
