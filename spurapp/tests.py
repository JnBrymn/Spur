"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from spurapp.models import *
from spurapp.views import *

class SimpleTest(TestCase):
    """
    TODO: Remove this class
    """
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class DonationTrackingTest(TestCase):
    def make_fake_IPN(self,name,email,amount,transaction_id):
        names = (name + " ").split(" ")
        parameters = {
            "payer_email":email,
            "first_name": names[0],
            "last_name": names[1],
            "mc_gross": amount,
            "txn_id": transaction_id,
        }
        transaction_complete(parameters)

    def test_donation_creation(self):
        self.make_fake_IPN("John Berryman","test@whatever.com",100,"1111")
        donation = Donation.objects.get(transaction_id="1111")
        self.assertEqual(donation.donor.name,"John Berryman")
