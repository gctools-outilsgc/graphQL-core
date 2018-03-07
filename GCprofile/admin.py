from django.contrib import admin
from .models import Profile, Address, OrgTier, Department

# Register your models here.

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(OrgTier)
admin.site.register(Department)