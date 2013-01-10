"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    """
    TODO: Remove this class
    """
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class BasicSpurTests(TestCase):
    def test_click_percolation(self):
        """
        implement this
        """
        self.assertEqual(1 + 1, 4)
