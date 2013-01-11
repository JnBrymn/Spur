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
    website = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name+"_Charity: "+self.charity.name

class Donor(models.Model):
    name = models.CharField(null=True, max_length=200)
    email = models.CharField(null=True, max_length=200)
    def __unicode__(self):
        return self.name

class Donation(models.Model):
    amount = models.DecimalField(max_digits=16, decimal_places=4)
    campaign = models.ForeignKey(Campaign, null=True)
    donor = models.ForeignKey(Donor)
    parent_donation = models.ForeignKey('self', null=True, blank=True, related_name="child")
    date = models.DateTimeField()
    cumulative_amt = models.DecimalField(max_digits=16, decimal_places=4, null=True)
    clicks = models.IntegerField(default=0)
    transaction_id = models.CharField(max_length=100, null=True)
    def __unicode__(self):
        return ("Amount: "+str(self.amount)+
                "_Campaign: "+str(self.campaign.name if self.campaign else "CAMPAIGN UNSPECIFIED")+
                "_Donor: "+self.donor.name+
                "_Date: "+str(self.date)+
                "_Cumu: "+str(self.cumulative_amt)+
                "_Clicks: "+str(self.clicks))
    def percolate_donation(self):
        if self.parent_donation:
            self.parent_donation.cumulative_amt += self.amount
            self.parent_donation.save()
            self.parent_donation.percolate_donation()
        #TODO remove this print statement
        #print ("Adding %s's donation to %s's cumulative_donation. Now it's %f." % (
        #    self.donor.name, self.parent_donation.donor.name, self.parent_donation.cumulative_amt))
    def save(self, *args, **kwargs):
        if self.cumulative_amt is None:
            self.cumulative_amt = self.amount
        super(Donation, self).save(*args, **kwargs)
