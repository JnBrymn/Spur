from django.http import HttpResponse
from spurapp.models import Charity

def index(request):
    charity_list = Charity.objects.all();
    output = ', '.join([c.name for c in charity_list])
    return HttpResponse(output)

def charity(request, charity_id):
    return HttpResponse("You're looking at charity %s." % charity_id)

def campaign(request, charity_id):
    return HttpResponse("You're looking at the campaigns of poll %s." % charity_id)
