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
    def setUp(self):
        self.make_fake_IPN("John Berryman","test@whatever.com",100,"1111")
        self.make_fake_IPN("Krystal Xu","test@whoever.com",100,"2222")
        charity = Charity.objects.create(name="UNICEF")
        campaign = Campaign.objects.create(name="save babies",start_date=timezone.now(),end_date=timezone.now(),charity=charity,website="www.google.com")
        donation = Donation.objects.get(transaction_id="1111")
        donation.campaign=campaign
        donation.save()

    def make_fake_IPN(self,name,email,amount,transaction_id):
        names = (name + " ").split(" ")
        parameters = {
            "payer_email":email,
            "first_name": names[0],
            "last_name": names[1],
            "mc_gross": amount,
            "txn_id": transaction_id,
        }
        #refactor so that transaction_complete is in a test TODO
        transaction_complete(parameters)

    def test_donation_completion(self):
        """
        If a new user clicks a badge, make a donation, and shares, then a new
        Donor should be created, should have the appropriate parent_donation,
        and amount.
        """
        #user clicks badge
        response = self.client.get('/redirect/1');
        self.assertEqual(self.client.cookies['parentID'].value,'1')
        #user donates
        parameters = {
            "payer_email":"arthur@asdf.com",
            "first_name": "Arthur",
            "last_name": "Wu",
            "mc_gross": 50,
            "txn_id": "3333",
        }
        transaction_complete(parameters)
        donation = Donation.objects.get(transaction_id="3333")
        self.assertEqual(donation.donor.name,"Arthur Wu")
        #user shares
        response = self.client.get('/share/1?tx=3333')
        donation = Donation.objects.get(pk=donation.pk)
        self.assertEqual(donation.parent_donation.donor.name,"John Berryman")

    def test_donation_creation(self):
        donation = Donation.objects.get(transaction_id="1111")
        self.assertEqual(donation.donor.name,"John Berryman")

