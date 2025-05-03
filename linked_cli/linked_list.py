from .data_generator import Item  # import the Item dataclass for type hints
class Node:
    """
    A single node in the linked list, holding an Item and a pointer to the next node.
    """
    def __init__(self, data: Item):
        self.data = data    # the payload of this node
        self.next = None    # pointer to the next node in the chain
class LinkedList:
    """
    A singly linked list implementation supporting append, search, to_list, and in-place merge-sort.
    """
    def __init__(self):
        # The head pointer starts as None, indicating an empty list
        self.head = None

    def append(self, item: Item):
        """
        Add a new item to the end of the list in O(n) time (walk to the tail).
        If the list is empty, the new node becomes the head.
        """
        node = Node(item)
        if not self.head:
            self.head = node
            return
        cur = self.head
        # Traverse until the tail (node.next is None)
        while cur.next:
            cur = cur.next
        cur.next = node

    def search(self, name: str):
        """
        Traverse the list to find the first Item with matching name.
        Returns the Item if found, or None otherwise. O(n) time.
        """
        cur = self.head
        while cur:
            if cur.data.name == name:
                return cur.data
            cur = cur.next
        return None

    def to_list(self) -> list[Item]:
        """
        Convert the linked list into a Python list of Items, preserving order.
        Useful for printing or testing. O(n) time.
        """
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def sort(self, ascending: bool = True):
        """
        Sort the linked list by the 'date' field of each Item using merge-sort.
        Merge-sort on linked lists is O(n log n) time and requires O(log n) recursion depth.
        """
        def merge(left, right):
            # Dummy node to simplify edge cases
            dummy = tail = Node(None)  # type: ignore
            # Merge two sorted sublists
            while left and right:
                # Compare dates, invert comparison if descending
                if (left.data.date < right.data.date) == ascending:
                    tail.next, left = left, left.next
                else:
                    tail.next, right = right, right.next
                tail = tail.next
            # Attach the remaining tail
            tail.next = left or right
            return dummy.next

        def merge_sort(node):
            # Base case: empty or single-node list is already sorted
            if not node or not node.next:
                return node
            # Split list into two halves using slow/fast pointers
            slow, fast = node, node.next
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            mid, slow.next = slow.next, None
            # Recursively sort each half
            left = merge_sort(node)
            right = merge_sort(mid)
            # Merge the two sorted halves
            return merge(left, right)

        # Kick off merge-sort on the head and reassign head to the sorted list
        self.head = merge_sort(self.head)
