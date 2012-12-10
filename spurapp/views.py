import urllib
import urllib2
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from spurapp.models import Charity

from lib.paypal import PayPal


def transaction_complete(parameters):
    #TODO this is where you do something interesting with the parameters
    for k in parameters:
        print k,"-->",parameters[k]

@csrf_exempt
def ipn(request):
    return PayPal.ipn(request,transaction_complete)

def index(request):
    charity_list = Charity.objects.all();
    output = ', '.join([c.name for c in charity_list])
    return HttpResponse(output)

def charity(request, charity_id):
    return HttpResponse("You're looking at charity %s." % charity_id)

def campaign(request, charity_id):
    return HttpResponse("You're looking at the campaigns of poll %s." % charity_id)
