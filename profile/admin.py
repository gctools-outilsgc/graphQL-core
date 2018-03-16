from django.contrib import admin
from .models import Profile, Address, OrgTier, Organization

# Register your models here.

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(OrgTier)
admin.site.register(Organization)