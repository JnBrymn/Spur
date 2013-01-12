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
    #delete this printout eventually TODO
    for k in parameters:
        print k,"-->",parameters[k]

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
    context = Context({'website': donation.campaign.website,})
    resp = HttpResponse(loader.get_template('redirect.html').render(context))
    resp.set_cookie('parentID', donation.id)
    #TODO: redirect to website straight from here
    return resp

def share(request, campaign_id):
    c = get_object_or_404(Campaign, pk=campaign_id)
    #TODO: eventually this will be a custom page for that campaign rather than the same page for everybody
    return render_to_response('share.html')

def complete_donation(request):
    tx = request.POST["tx"]
    donation = Donation.objects.get(transaction_id=tx)
    if donation:
        if donation.parent_donation is None: #prevent abusing percolation
            parentID = request.COOKIES["parentID"]
            if parentID:
                parent_donation = Donation.objects.get(id=parentID)
                donation.parent_donation = parent_donation
                donation.save()
                donation.percolate_donation()    
    else:
        print "Donation doesn't exist"
    return HttpResponse("Complete donation")
