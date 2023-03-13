from src.repository.student_repository import *
from src.repository.assigment_repository import *
from src.repository.undo_redo_repository import UndoRedoRepository
from src.services.student_service import StudentService
from src.services.assignment_service import AssignmentService
from src.ui.ui import UI
from src.repository.grade_repository import *
from src.services.grade_service import GradeService
from src.services.undo_redo_service import UndoRedoService

settings_file = open("settings.properties", "rt")
lines = settings_file.readlines()

line_number = 0
position_of_repository_type = 2
repository_type = lines[line_number].split(maxsplit=3, sep=" ")[position_of_repository_type].strip()

if repository_type == "inmemory":
    student_repository = StudentRepository()
    assignment_repository = AssignmentRepository()
    grade_repository = GradeRepository()
    undo_redo_repository = UndoRedoRepository()

    undo_redo_service = UndoRedoService(undo_redo_repository)
    student_service = StudentService(student_repository, undo_redo_service)
    assignment_service = AssignmentService(assignment_repository, undo_redo_service)
    grade_service = GradeService(grade_repository, student_repository, assignment_repository, undo_redo_service)

    student_service.generate_students()
    assignment_service.generate_assignments()
    grade_service.generate_grades()

else:
    position_of_file_location = 2

    line_number = 1
    assignments_file_location = lines[line_number].split(maxsplit=3, sep=" ")[
        position_of_file_location].strip()

    line_number = 2
    students_file_location = lines[line_number].split(maxsplit=3, sep=" ")[
        position_of_file_location].strip()

    line_number = 3
    grades_file_location = lines[line_number].split(maxsplit=3, sep=" ")[
        position_of_file_location].strip()

    if repository_type == "textfiles":
        student_repository = StudentFileTextRepository(students_file_location)
        assignment_repository = AssignmentTextFileRepository(assignments_file_location)
        grade_repository = GradeTextFileRepository(grades_file_location)
        undo_redo_repository = UndoRedoRepository()
    elif repository_type == "binaryfiles":
        student_repository = StudentBinaryFileRepository(students_file_location)
        assignment_repository = AssignmentBinaryFileRepository(assignments_file_location)
        grade_repository = GradeBinaryFileRepository(grades_file_location)
        undo_redo_repository = UndoRedoRepository()

    undo_redo_service = UndoRedoService(undo_redo_repository)
    student_service = StudentService(student_repository, undo_redo_service)
    assignment_service = AssignmentService(assignment_repository, undo_redo_service)
    grade_service = GradeService(grade_repository, student_repository, assignment_repository, undo_redo_service)
ui = UI(student_service, assignment_service, grade_service, undo_redo_service)
ui.start()

