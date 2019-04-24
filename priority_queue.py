import heapq
from functools import total_ordering

@total_ordering
class SpecialSorted:
    """
    A helper class to sort the elements of a PriorityQueue
    """

    def __init__(self, element, value):
        self.element = element
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

class PriorityQueue:
    """Implements a PriorityQueue"""

    def __init__(self, sortkey = lambda x : x):
        """
        Create a new PriorityQueue

        :param sortkey: a function used to sort the elements of the priority queue
        :type sortkey: func
        """
        self.content = []
        self.sortkey = sortkey

    def add(self, item):
        """
        Add an item to the PriorityQueue

        :param item: The item to add
        :type item: obj
        """
        heapq.heappush(self.content, SpecialSorted(item, self.sortkey(item)))

    def peek(self):
        """
        Peeks at the top element

        :return: the top element of the PriorityQueue
        :rtype: obj
        """
        return self.content[0].element if self.content else None

    def poll(self):
        """
        Removes the top element of the PriorityQueue and returns it

        :return: the top element of the PriorityQueue
        :rtype: obj
        """
        return heapq.heappop(self.content).element if len(self.content) > 0 else None

    def is_empty(self):
        """
        Returns whether the PriorityQueue is empty

        :return: True if the PriorityQueue is empty
        :rtype: int
        """
        return len(self.content) == 0

    def __str__(self):
        """
        Returns the string representation of the PriorityQueue

        :return: a string representation
        :rtype: str
        """
        return str(heapq.nsmallest(len(self.content), [item.element for item in self.content]))
