class UndoRedoServiceException(Exception):
    pass

class UndoRedoService:

    def __init__(self, undo_redo_repository):
        """
        Initialize the undo redo service
        :param undo_redo_repository: a undo redo repository object used for working with operations
        """
        self._undo_redo_repository = undo_redo_repository

    def undo(self):
        """
        Undo the last performed operation
        """
        if self._undo_redo_repository.get_index_in_modification_history() < 0:
            raise UndoRedoServiceException("Cannot undo anymore")
        self._undo_redo_repository.update_index_in_modification_history(-1)
        self._undo_redo_repository.get_modifications_history()[
        self._undo_redo_repository.get_index_in_modification_history()+1].undo()


    def redo(self):
        """
        Redo the recent program modification that you undo
        """
        if self._undo_redo_repository.get_index_in_modification_history() + 1 >= len(self._undo_redo_repository.get_modifications_history()):
            raise UndoRedoServiceException("Cannot redo anymore")
        self._undo_redo_repository.update_index_in_modification_history(1)
        self._undo_redo_repository.get_modifications_history()[
        self._undo_redo_repository.get_index_in_modification_history()].redo()



    def record_operation(self, operation):
        """
        Add a new operation/complex operation to the undo/redo repository
        :param operation: a operation/complex operation object to add
        """
        self._undo_redo_repository.add_new_operation_to_modifications_history(operation)