import unittest
from datetime import datetime
from linked_cli.data_generator import Item
from linked_cli.linked_list import LinkedList

class TestLinkedList(unittest.TestCase):
    """
    Test suite for the LinkedList class functionality:
    - append + to_list
    - search (found & not found)
    - sort (ascending & descending)
    """

    def setUp(self):
        # Called before every test: prepare a linked list with 3 known Items
        self.items = [
            Item(name="A", date=datetime(2021, 1, 1)),
            Item(name="B", date=datetime(2020, 5, 5)),
            Item(name="C", date=datetime(2022, 12, 12)),
        ]
        self.ll = LinkedList()
        for item in self.items:
            self.ll.append(item)

    def test_to_list(self):
        # PART: to_list()
        # Verify that to_list returns the items in insertion order
        self.assertEqual(self.ll.to_list(), self.items)

    def test_search_found(self):
        # PART: search() when item exists
        # We know "B" was inserted; search should return a non-None Item
        result = self.ll.search("B")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "B")

    def test_search_not_found(self):
        # PART: search() when item does not exist
        # Searching for "X" should return None
        self.assertIsNone(self.ll.search("X"))

    def test_sort_ascending(self):
        # PART: sort(ascending=True)
        # After sorting ascending, dates list must equal sorted(dates)
        self.ll.sort(ascending=True)
        dates = [itm.date for itm in self.ll.to_list()]
        self.assertEqual(dates, sorted(dates))

    def test_sort_descending(self):
        # PART: sort(ascending=False)
        # After sorting descending, dates list must equal sorted(dates, reverse=True)
        self.ll.sort(ascending=False)
        dates = [itm.date for itm in self.ll.to_list()]
        self.assertEqual(dates, sorted(dates, reverse=True))

if __name__ == "__main__":
    # Allows running this test file directly
    unittest.main()
