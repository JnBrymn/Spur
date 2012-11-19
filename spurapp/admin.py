from spurapp.models import *
from django.contrib import admin


class CampaignInline(admin.StackedInline):
    model = Campaign
    extra = 5

class DonationInline(admin.StackedInline):
    model = Donation
    extra = 5

class CharityAdmin(admin.ModelAdmin):
    inlines = [CampaignInline]

class DonorAdmin(admin.ModelAdmin):
    inlines = [DonationInline]

admin.site.register(Charity,CharityAdmin)
admin.site.register(Campaign)
admin.site.register(Donor,DonorAdmin)
admin.site.register(Donation)
