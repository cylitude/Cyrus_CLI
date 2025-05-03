import unittest
from datetime import datetime
from linked_cli.data_generator import Item
from linked_cli.linked_list import LinkedList

class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.items = [
            Item(name="A", date=datetime(2021, 1, 1)),
            Item(name="B", date=datetime(2020, 5, 5)),
            Item(name="C", date=datetime(2022, 12, 12)),
        ]
        self.ll = LinkedList()
        for it in self.items:
            self.ll.append(it)

    def test_to_list(self):
        self.assertEqual(self.ll.to_list(), self.items)

    def test_search_found(self):
        self.assertIsNotNone(self.ll.search("B"))

    def test_search_not_found(self):
        self.assertIsNone(self.ll.search("X"))

    def test_sort_ascending(self):
        self.ll.sort(ascending=True)
        dates = [itm.date for itm in self.ll.to_list()]
        self.assertEqual(dates, sorted(dates))

    def test_sort_descending(self):
        self.ll.sort(ascending=False)
        dates = [itm.date for itm in self.ll.to_list()]
        self.assertEqual(dates, sorted(dates, reverse=True))

if __name__ == "__main__":
    unittest.main()