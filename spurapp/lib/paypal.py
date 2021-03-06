import urllib
import urllib2
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError

class PayPal:
    @staticmethod
    def ipn(request, callback):
        print "in PayPal.ipn"
        #import pdb; pdb.set_trace()
        NOTIFY_EMAIL = 'your@email.com'
        # real url
        #PP_URL = "https://www.paypal.com/cgi-bin/webscr"
        # sandbox url
        PP_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"; print "WARNING: USING SANDBOX PAYPAL"

        # post back to paypal for verification
        parameters = request.POST.copy()
        parameters['cmd']='_notify-validate'
        params = urllib.urlencode(parameters)
        req = urllib2.Request(PP_URL, params)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError:
            # Network problem. Responding with a HTTP 500 will make PayPal try
            # again later
            print "Network problem. Responding with a HTTP 500 will make PayPal try again later"
            return HttpResponseServerError("Error")

        # Does paypal think the IPN is legit?
        res = response.read().strip()
        if res == "INVALID":
            # fraud logic goes here
            print "response INVALID"
            send_mail('Fraudster', str(parameters), NOTIFY_EMAIL, [NOTIFY_EMAIL])
            return HttpResponse("")
        elif res == "":
            print "response empty"
            # PayPal claims the only other possible value for the response is
            # "VERIFIED" but in my experience, PayPal will also respond with the
            # empty string.  And in that case, you need to respond with a 500 HTTP
            # status code so PayPal resends the IPN message
            return HttpResponseServerError("Error")

        # Ok, so we got a valid IPN message...
        print "Ok, so we got a valid IPN message..."

        status = parameters['payment_status']
        # For easy reference...possible statuses
        # Canceled_Reversal: A reversal has been canceled. For example, you won a
        # dispute with the customer, and the funds for the transaction that was reversed
        # have been returned to you.
        #
        # Completed: The payment has been completed, and the funds have been added
        # successfully to your account balance.
        #
        # Created: A German ELV payment is made using Express Checkout.
        #
        # Denied: You denied the payment. This happens only if the payment was previously
        # pending because of possible reasons described for the pending_reason variable
        # or the Fraud_Management_Filters_x variable.
        #
        # Expired: This authorization has expired and cannot be captured.
        #
        # Failed: The payment has failed. This happens only if the payment was made from
        # your customer's bank account.
        #
        # Pending: The payment is pending. See pending_reason for more information.
        #
        # Refunded: You refunded the payment.
        #
        # Reversed: A payment was reversed due to a chargeback or other type of reversal.
        # The funds have been removed from your account balance and returned to the
        # buyer. The reason for the reversal is specified in the ReasonCode element.
        #
        # Processed: A payment has been accepted.
        #
        # Voided: This authorization has been voided.

        if status in ['Pending', 'Completed']:
            callback(parameters)

        elif status in ['Denied', 'Failed', 'Reversed']:
            pass
        else:
            pass
            #Strange payment status - handle it manually

        return HttpResponse("Ok")


 
