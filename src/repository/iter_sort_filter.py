class Iterator:
    def __init__(self):
        self._data = dict()

    def __contains__(self, key):
        return True if key in self._data else False

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        self._position = 0
        return self

    def __next__(self):
        if self._position == len(self._data):
            raise StopIteration
        self._position += 1
        return self._data[list(self._data.keys())[self._position-1]]

    def __len__(self):
        return len(self._data)

    # def __repr__(self):
    #     representation = ""
    #     for entity in self._data.values():
    #         representation = representation + str(entity) + "\n"
    #     return representation
    #
    # def copy(self):
    #     return self._data.copy()
    #
    # def get_keys(self):
    #     return list(self._data.keys())


def gnome_sort(list_to_sort, compare):
    """
    Function to sort a list using gnome sort algorithm
    :param list_to_sort: a list object
    :param compare: a function used for comparing 2 objects from the list
    :return: the sorted list
    """
    index_for_list = 0
    number_of_entities = len(list_to_sort)
    while index_for_list < number_of_entities:
        if index_for_list == 0 or compare(list_to_sort[index_for_list], list_to_sort[index_for_list-1]):
            index_for_list = index_for_list + 1
        else:
            list_to_sort[index_for_list], list_to_sort[index_for_list - 1] = list_to_sort[index_for_list - 1], list_to_sort[index_for_list]
            index_for_list = index_for_list - 1
    return list_to_sort

def filter_a_list(list_to_filter, accept):
    """
    Function to filter a list by a specified criteria
    :param list_to_filter: a list that will be filtered
    :param accept: a function that will return True if a element passes the filter or False otherwise
    :return: the filtered list
    """
    filtered_list = []
    for element in list_to_filter:
        if accept(element):
            filtered_list.append(element)
    return filtered_list

