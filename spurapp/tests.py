from django.test import TestCase
from spurapp.models import *
from spurapp.views import *
from random import randint

class DonationTrackingTest(TestCase):
    def setUp(self):
        self.website="http://www.google.com"
        self.charity = Charity.objects.create(name="UNICEF")
        self.campaign = Campaign.objects.create(name="save babies",start_date=timezone.now(),end_date=timezone.now(),charity=self.charity,website=self.website)
        self.campaign_id = str(self.campaign.pk)
        self.john = Donor.objects.create(name='John Berryman', email='jfberryman@gmail.com')
        self.john_donation = Donation.objects.create(amount=50, donor=self.john, date=timezone.now(), transaction_id='1111', campaign=self.campaign)
        self.john_donation_id = str(self.john_donation.pk)


    def test_redirect(self):
        """
        Clicking a badge (e.g. a redirect link) should redirect you to the appropriate page.
        """
        response = self.client.get('/redirect/'+ self.john_donation_id)
        self.assertNotEqual(response.status_code,404)
        self.assertRedirects(response,self.website)

    def test_badge_click_cookie(self):
        """
        If a new user clicks a badge (e.g. a redirect link) then they should get a cookie associated
        with the badge's donation and campaign.
        """
        #user clicks badge
        response = self.client.get('/redirect/'+ self.john_donation_id)
        self.assertEqual(self.client.cookies['parent_donation_for_campaign_'+ self.campaign_id].value,self.john_donation_id)

    def click_badge_donate_visit_share_page(self, name, amount, donation_clicked=None):
        """
        Click badge (associated with donation_clicked - defaults to badge in setUp),
        donate specified amount under specified name, and visit share page. Return resulting
        donation.
        """
        if not ' ' in name:
            raise Exception("name assumed to have space so as to denote first and last names")
        name = name.split(' ')
        transaction_id = str(randint(100000,999999))
        #user clicks badge
        if donation_clicked:
            self.client.get('/redirect/'+ str(donation_clicked.pk))
        else:
            self.client.get('/redirect/'+ self.john_donation_id)
        #user donates
        parameters = {
            "payer_email":"doesnot"+ transaction_id +"@matter.com",
            "first_name": name[0],
            "last_name": name[1],
            "mc_gross": amount,
            "txn_id": transaction_id,
        }
        transaction_complete(parameters)
        #user visits share page
        self.client.get("/share/"+ self.campaign_id +"?tx="+str(transaction_id))
        return Donation.objects.get(transaction_id=transaction_id)

    def test_donation_completion(self):
        """
        If a new user clicks a badge, make a donation, and shares, then a new
        Donor should be created, should have the appropriate parent_donation,
        and amount.
        """
        donation = self.click_badge_donate_visit_share_page("Arthur Wu",50)
        self.assertTrue(donation)
        self.assertEqual(donation.donor.name,"Arthur Wu")
        self.assertEqual(donation.parent_donation.donor.name,"John Berryman")

    def test_percolation_of_traits(self):
        #raise Exception("incomplete!")
        granny_donation = self.click_badge_donate_visit_share_page("Granny Spur",50)
        momma_donation = self.click_badge_donate_visit_share_page("Momma Spur",30,granny_donation)
        kid_donation = self.click_badge_donate_visit_share_page("Kiddie Spur",10,momma_donation)
        uncle_donation = self.click_badge_donate_visit_share_page("Uncle Spur",20,granny_donation)
        sibling_donation = self.click_badge_donate_visit_share_page("Sibling Spur",40,momma_donation)

        granny_donation = Donation.objects.get(pk=granny_donation.pk)
        momma_donation = Donation.objects.get(pk=momma_donation.pk)
        kid_donation = Donation.objects.get(pk=kid_donation.pk)
        uncle_donation = Donation.objects.get(pk=uncle_donation.pk)
        sibling_donation = Donation.objects.get(pk=sibling_donation.pk)

        self.assertEqual( granny_donation.cumulative_amt, 150)
        self.assertEqual( momma_donation.cumulative_amt, 80)
        self.assertEqual( kid_donation.cumulative_amt, 10)
        self.assertEqual( uncle_donation.cumulative_amt, 20)
        self.assertEqual( sibling_donation.cumulative_amt, 40)

    def test_facebook_share(self):
        pass

    def test_twitter_share(self):
        pass

    def test_email(self):
        pass

