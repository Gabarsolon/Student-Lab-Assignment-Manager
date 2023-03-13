class UndoRedoRepository:
    def __init__(self):
        """
        Initialize the repository of undo/redo operations
        """
        # the list of operations
        self._modifications_history = []
        # where we are in the list of operations
        self._index_in_modification_history = -1

    def add_new_operation_to_modifications_history(self, operation):
        """
        Add a new operation to the modifications history
        :param operation: a operation or complex operation object to add
        """
        self._index_in_modification_history += 1
        self._modifications_history.insert(self._index_in_modification_history, operation)

    def get_modifications_history(self):
        """
        Return the list of operations
        :return a list of operation/complex operation objects
        """
        return self._modifications_history

    def get_index_in_modification_history(self):
        """
        Return the current position in modification history
        :return: a integer which represent the current position in modification history
        """
        return self._index_in_modification_history

    def update_index_in_modification_history(self, new_index_value_to_add):
        """
        Update the index in modification history by incrementing or decrementing it
        :param new_index_value_to_add: a integer which represent the value by which we will decrement/increment the index
        """
        self._index_in_modification_history += new_index_value_to_add

