import urllib
import urllib2
import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from spurapp.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from lib.paypal import PayPal


def transaction_complete(parameters):
    try:
        donor = Donor.objects.get(email=parameters["payer_email"])
    except Donor.DoesNotExist:
        donor = Donor(name=parameters["first_name"]+" "+parameters["last_name"], email=
                  parameters["payer_email"])
        donor.save()

    donation = Donation(amount=parameters["mc_gross"], donor=donor,
                        date=timezone.now(),
                        transaction_id=parameters["txn_id"])
    donation.save()

@csrf_exempt
def ipn(request):
    ## import pdb; pdb.set_trace()
    return PayPal.ipn(request,transaction_complete)

def index(request):
    charity_list = Charity.objects.all();
    return render_to_response('charities/index.html', {'charity_list': charity_list})

def campaign(request, charity_id):
    return HttpResponse("You're looking at the campaigns of charity %s." % charity_id)
	
def redirect(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)
    (donation.clicks)+=1
    donation.save()
    resp = HttpResponseRedirect(donation.campaign.website)
    resp.set_cookie('parent_donation_for_campaign'+str(donation.campaign.id), donation.id, max_age=1000)
    return resp

def share(request, campaign_id):
    tx = request.GET["tx"]
    donation = Donation.objects.get(transaction_id=tx) #add try/except to "get" lines
    parentID = request.COOKIES["parent_donation_for_campaign"+str(campaign_id)]
    if parentID:
        parent_donation = Donation.objects.get(id=parentID)
        donation.parent_donation = parent_donation
        donation.save()
        donation.percolate_donation()
    c = get_object_or_404(Campaign, pk=campaign_id)
    #TODO: eventually this will be a custom page for that campaign rather than the same page for everybody
    return render_to_response('share.html')
