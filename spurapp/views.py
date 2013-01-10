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
    #TODO this is where you do something interesting with the parameters
    for k in parameters:
        print k,"-->",parameters[k]

    #import pdb; pdb.set_trace()

    try:
        donor = Donor.objects.get(email=parameters["payer_email"])
    except Donor.DoesNotExist:
        donor = Donor(name=parameters["first_name"]+" "+parameters["last_name"], email=
                  parameters["payer_email"])
        donor.save()
    
    # get all fields possible
##    try:
##        donation = Donation.objects.get(donor=donor, campaign
    donation = Donation(amount=parameters["mc_gross"], donor=donor,
                        date=datetime.datetime.now(),
                        transaction_id=parameters["txn_id"])
    donation.save()

@csrf_exempt
def ipn(request):
    ## import pdb; pdb.set_trace()
    return PayPal.ipn(request,transaction_complete)

def index(request):
    charity_list = Charity.objects.all();
##    t = loader.get_template('charities/index.html')
##    c = Context({
##        'charity_list': charity_list,
##    })
    # output = ', '.join([c.name for c in charity_list])
    return render_to_response('charities/index.html', {'charity_list': charity_list})

def charity_detail(request, charity_id):
##    try:
##        c = Charity.objects.get(pk=charity_id)
##    except Charity.DoesNotExist:
##        raise Http404
    c = get_object_or_404(Charity, pk=charity_id)
    return render_to_response('charities/detail.html', {'charity': c}, context_instance=RequestContext(request))

##def charity(request, charity_id):
##    return HttpResponse("You're looking at charity %s." % charity_id)

def campaign(request, charity_id):
    return HttpResponse("You're looking at the campaigns of charity %s." % charity_id)
	
def redirect(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)
    context = Context({'website': donation.campaign.website,})
    resp = HttpResponse(loader.get_template('redirect.html').render(context))
    resp.set_cookie('parentID', donation.id)
    return resp

def share(request, charity_id):
    c = get_object_or_404(Charity, pk=charity_id)
    return render_to_response('share/index.html', {'charity': c}, context_instance=RequestContext(request))

def complete_donation(request):
    return HttpResponse("Complete donation")
