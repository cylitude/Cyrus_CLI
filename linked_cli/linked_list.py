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
    A singly linked list implementation supporting O(1) append, O(1) search by name,
    to_list, and in-place merge-sort.
    """
    def __init__(self):
        # The head pointer starts as None, indicating an empty list
        self.head = None
        # Tail pointer for O(1) append
        self.tail = None
        # name_map dictionary for O(1) lookups by name
        self.name_map = {}

    def append(self, item: Item):
        """
        Add a new item to the end of the list in O(1) time using the tail pointer.
        If the list is empty, the new node becomes both head and tail.
        """
        node = Node(item)
        # Store node in name_map for O(1) lookups
        self.name_map[item.name] = node

        if not self.head:
            # Empty list
            self.head = node
            self.tail = node
        else:
            # Append to tail in O(1) time
            self.tail.next = node
            self.tail = node

    def search(self, name: str):
        """
        Search for an Item with matching name in O(1) time using the name_map.
        Returns the Item if found, or None otherwise.
        """
        node = self.name_map.get(name)
        return node.data if node else None

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
        After sorting, updates the tail pointer and rebuilds the name_map.
        """
        def merge(left: Node, right: Node) -> Node:
            # Dummy node to simplify edge cases
            dummy = tail = Node(None)  # type: ignore
            # Merge two sorted sublists
            while left and right:
                if (left.data.date < right.data.date) == ascending:
                    tail.next, left = left, left.next
                else:
                    tail.next, right = right, right.next
                tail = tail.next
            # Attach any remaining nodes
            tail.next = left or right
            return dummy.next

        def merge_sort(node: Node) -> Node:
            # Base case: empty or single-node list is already sorted
            if not node or not node.next:
                return node

            # Split list into two halves using slow/fast pointers
            slow, fast = node, node.next
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            mid, slow.next = slow.next, None  # cut the list

            # Recursively sort each half
            left = merge_sort(node)
            right = merge_sort(mid)

            # Merge the two sorted halves
            return merge(left, right)

        # If list is empty or single element, nothing to do
        if not self.head or not self.head.next:
            if self.head:
                self.tail = self.head
            return

        # Perform merge sort on the list
        self.head = merge_sort(self.head)

        # Update the tail pointer by traversing to the end
        cur = self.head
        while cur.next:
            cur = cur.next
        self.tail = cur

        # Rebuild the name_map since the order has changed
        self.name_map = {}
        cur = self.head
        while cur:
            self.name_map[cur.data.name] = cur
            cur = cur.next
