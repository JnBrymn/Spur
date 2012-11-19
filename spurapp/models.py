import datetime
from django.utils import timezone
from django.db import models

class Charity(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    charity = models.ForeignKey(Charity)
    def __unicode__(self):
        return self.name+"_Charity: "+self.charity.name

class Donor(models.Model):
    name = models.CharField(null=True, max_length=200)
    def __unicode__(self):
        return self.name

class Donation(models.Model):
    amount = models.DecimalField(max_digits=16, decimal_places=4)
    campaign = models.ForeignKey(Campaign)
    donor = models.ForeignKey(Donor)
    parent_donation = models.ForeignKey('self', null=True, blank=True, related_name="child")
    date = models.DateTimeField()
    cumulative_amt = models.DecimalField(max_digits=16, decimal_places=4)
    clicks = models.IntegerField(default=0)
    def __unicode__(self):
        return ("Amount: "+str(self.amount)+"_Campaign: "+self.campaign.name+
                "_Donor: "+self.donor.name+"_Date: "+str(self.date)+"_Cumu: "+str(self.cumulative_amt)
                +"_Clicks: "+str(self.clicks))
    def percolate_donation(self):
        self.parent_donation.cumulative_amt += self.amount
        print ("Adding %s's donation to %s's cumulative_donation. Now it's %f." % (
            self.donor.name, self.parent_donation.donor.name, self.parent_donation.cumulative_amt))
