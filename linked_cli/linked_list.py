from .data_generator import Item

class Node:
    def __init__(self, data: Item):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, item: Item):
        node = Node(item)
        if not self.head:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def search(self, name: str):
        cur = self.head
        while cur:
            if cur.data.name == name:
                return cur.data
            cur = cur.next
        return None

    def to_list(self) -> list[Item]:
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def sort(self, ascending: bool = True):
        def merge(left, right):
            dummy = tail = Node(None)  # type: ignore
            while left and right:
                if (left.data.date < right.data.date) == ascending:
                    tail.next, left = left, left.next
                else:
                    tail.next, right = right, right.next
                tail = tail.next
            tail.next = left or right
            return dummy.next

        def merge_sort(node):
            if not node or not node.next:
                return node
            slow, fast = node, node.next
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            mid, slow.next = slow.next, None
            left = merge_sort(node)
            right = merge_sort(mid)
            return merge(left, right)

        self.head = merge_sort(self.head)