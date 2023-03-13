from src.domain.assignment import Assignment
import random
import datetime
from src.domain.undo_redo import *
from src.services.grade_service import GradeService

ASSIGNMENT_DESCRIPTION = [
    'Implement something cool', 'Create your own site', 'Create your own game', 'Yeah, do something',
    'Compile something',
    'Create a android app', 'Build a game engine', 'Improve your previous code', 'Implement a database manager app',
    'Create a nice app with a friend', 'Write some code man', 'Learn Java', 'Spend your time coding something',
    'Improve your typing skills', 'Solve the German Tank problem', 'Solve 10 problems from current chapter',
    'Coop with a colleague', 'Start a new project', 'Participate in a code contest', 'Teach someone something'
]


class AssignmentService():
    def __init__(self, assignment_repository, undo_redo_service):
        """
        Initialize the assignment service
        :param assignment_repository: an assignment repository object
        """
        self._assignment_repository = assignment_repository
        self._undo_redo_service = undo_redo_service

    def generate_assignments(self):
        """
        Add 10 randomly generated assignments to the repository
        """
        # start the assignments id's from 1
        assignment_counter = 1
        # pick deadlines between 2 dates
        start_date = datetime.date(2021, 9, 1)
        end_date = datetime.date(2022, 6, 1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        for current_index in range(10):
            assignment_index = assignment_counter
            assignment_description = ASSIGNMENT_DESCRIPTION[random.randint(0, 19)]
            random_number_of_days = random.randrange(days_between_dates)
            assignment_deadline = start_date + datetime.timedelta(days=random_number_of_days)
            self._assignment_repository.add_assignment(Assignment(assignment_index, assignment_description,
                                                                  assignment_deadline))
            assignment_counter += 1

    def add_assignment(self, assignment_id, description, deadline):
        """
        Add assignment to the assignment repository
        :param assignment_id: integer, which represents the assignment's id
        :param description: string, which represents the description of the assignment
        :param deadline: datetime object, which represents the date of the deadline
        """
        self._assignment_repository.add_assignment(Assignment(assignment_id, description, deadline))
        undo_call = Call(self._assignment_repository.remove_assignment, assignment_id)
        redo_call = Call(self._assignment_repository.add_assignment, Assignment(assignment_id, description, deadline))
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))

    def remove_assignment(self, assignment_id):
        """
        Remove assignment from repository
        :param assignment_id: a integer which indicates the id of the assignment which we want to remove
        """
        self._assignment_repository.remove_assignment(assignment_id)

    def update_assignment_description(self, assignment_id, new_description):
        """
        Update description of an assignment from repository
        :param assignment_id: a integer which indicate the id of the assignment which we want to  update
        :param new_description: a string which will replace the actual description of the assignment
        """
        self._assignment_repository.check_valid_assignment_id(assignment_id)
        actual_description = self._assignment_repository.get_assignment_data()[assignment_id].description
        undo_call = Call(self._assignment_repository.update_assignment_description, assignment_id, actual_description)
        redo_call = Call(self._assignment_repository.update_assignment_description, assignment_id, new_description)
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))
        self._assignment_repository.update_assignment_description(assignment_id, new_description)

    def update_assignment_deadline(self, assignment_id, new_deadline):
        """
        Update description of an assignment from repository
        :param assignment_id: a integer which indicate the id of the assignment which we want to  update
        :param new_deadline: a datetime object which will replace the actual deadline of the assignment
        """
        self._assignment_repository.check_valid_assignment_id(assignment_id)
        actual_deadline = self._assignment_repository.get_assignment_data()[assignment_id].deadline
        undo_call = Call(self._assignment_repository.update_assignment_deadline, assignment_id, actual_deadline)
        redo_call = Call(self._assignment_repository.update_assignment_deadline, assignment_id, new_deadline)
        self._undo_redo_service.record_operation(Operation(undo_call, redo_call))
        self._assignment_repository.update_assignment_deadline(assignment_id, new_deadline)

    def check_valid_assignment(self, assignment_id):
        """
        Check if a assigment is present in the assignment repository
        :param assignment_id: a integer which represents the id of the assginment to check
        """
        self._assignment_repository.check_valid_assignment_id(assignment_id)

    def get_assignments(self):
        return self._assignment_repository.get_assignment_data()