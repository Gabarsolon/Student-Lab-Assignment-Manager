class Call:
    def __init__(self, function_name, *function_params):
        """
        Initialize the call object
        :param function_name: a string which represent the name of the function
        :param function_params: a list of packed parameters
        """
        self._function_name = function_name
        self._function_params = function_params

    def call(self):
        """
        Call the function with the unpacked parameters
        """
        self._function_name(*self._function_params)


class Operation:
    def __init__(self, undo_call, redo_call):
        """
        Initialize the operation object
        :param undo_call: a call object used for calling the corresponding function for undoing a program modification
        :param redo_call: a call object used for calling the corresponding function for redoing a program modification
        """
        self._undo_call = undo_call
        self._redo_call = redo_call

    def undo(self):
        """
        Call the undo function
        """
        self._undo_call.call()

    def redo(self):
        """
        Call the redo function
        """
        self._redo_call.call()


class ComplexOperation:
    def __init__(self, operation):
        """
        Initialize the complex operation object
        :param operation: a list of operation objects
        """
        self._operations = operation

    def undo(self):
        """
        Call the undo function for every operation in the operations list
        """
        for operation in self._operations:
            operation.undo()

    def redo(self):
        """
        Call the redo function for every operation in the operations list
        """
        for operation in self._operations:
            operation.redo()


